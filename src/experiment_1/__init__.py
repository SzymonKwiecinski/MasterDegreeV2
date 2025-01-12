from src.const import CORRECT_MODELS_PATH, EXPERIMENT_1_PATH, ABS_PYTHON_INTERPRETER
from src.experts import PY_C_EXPERT, PY_F_EXPERT
from src.helpers import (
    chat_completion_to_python_file,
    run_python_code,
    extract_objective_from_text,
)
from src.core import CorrectModel, Report
from src.core import ChatModel, OpenAiPrompt, Message
from src.templates import python_file_name_template
from openai import Client

TASKS_NUMBER = 18  # 18
EXP_RETRY = 10


def run(
    client: Client,
    py_c_model: ChatModel,
    py_f_model: ChatModel,
    experiment_name: str,
    fix_retries: int = 0,
):
    # Konfiguracja ścieżki do eksperymentu
    experiment_path = EXPERIMENT_1_PATH / experiment_name
    experiment_path.mkdir(exist_ok=True)

    # Pobranie poprawnych modeli
    correct_models = []
    for i in range(1, TASKS_NUMBER + 1):
        correct_models.append(
            CorrectModel.from_folder(number=i, path=CORRECT_MODELS_PATH / str(i))
        )

    # Powtarzanie eksperymentu w celu uzyskania stabilności wyników 10 razy
    for exp_retry in range(1, EXP_RETRY + 1):
        retry_experiment_path = experiment_path / str(exp_retry)
        retry_experiment_path.mkdir(exist_ok=True)

        # Iteracja po poprawnych modelach
        for correct_model in correct_models:
            print(f"START {exp_retry=}, {correct_model.number=}\n")
            model_path = retry_experiment_path / str(correct_model.number)
            model_path.mkdir(exist_ok=True)
            report = Report(
                experiment_name=experiment_name,
                experiment_iteration=exp_retry,
                task_number=correct_model.number,
                obj_expected=correct_model.obj,
            )
            # Konfiguracja promptów dla ekspertów
            py_c_prompt = OpenAiPrompt(
                client=client, expert=PY_C_EXPERT, log_dir=model_path, temperature=0.9
            )

            py_f_prompt = OpenAiPrompt(
                client=client, expert=PY_F_EXPERT, log_dir=model_path, temperature=0.9
            )

            py_c_prompt.add_messages([Message.from_correct_model(correct_model)])

            # Zapytanie o stworzenie kodu w języku Python
            chat_completion_py_c = py_c_prompt.run(model=py_c_model)
            report.update_tokens(chat_completion_py_c)
            # Zapisanie kodu do pliku
            chat_completion_to_python_file(
                abs_path=model_path
                / python_file_name_template.format(number=report.code_fix_count),
                chat_completion=chat_completion_py_c,
            )
            # Uruchomienie kodu w interpreterze Pythona
            stderr, stdout, code = run_python_code(
                ABS_PYTHON_INTERPRETER,
                model_path
                / python_file_name_template.format(number=report.code_fix_count),
            )
            # Jeżeli kod jest niepoprawny, to próbujemy go naprawić
            for fix_retry in range(fix_retries):
                # Jeżeli kod jest poprawny, to przerywamy pętlę
                if not bool(stderr):
                    break
                # Dodajemy informacje o błędzie do promptu
                py_f_prompt.add_messages(
                    [Message.from_syntax_error(wrong_code=code, code_error=stderr)]
                )
                # Zapytanie o naprawę kodu
                chat_completion_py_f = py_f_prompt.run(model=py_f_model)
                report.update_tokens(chat_completion_py_f)
                report.code_fix_count += 1
                # Zapisanie kodu do pliku
                chat_completion_to_python_file(
                    abs_path=model_path
                    / python_file_name_template.format(number=report.code_fix_count),
                    chat_completion=chat_completion_py_f,
                )
                # Uruchomienie kodu w interpreterze Pythona
                stderr, stdout, code = run_python_code(
                    ABS_PYTHON_INTERPRETER,
                    model_path
                    / python_file_name_template.format(number=report.code_fix_count),
                )
            # Jeżeli kod jest poprawny, to zapisujemy wyniki
            if not bool(stderr):
                report.code_syntax_status = True
                # Wyciągamy obliczony wynik funkcji celu z tekstu
                report.obj_given = extract_objective_from_text(stdout)

            report.save(EXPERIMENT_1_PATH)
            print(f"END {exp_retry=}, {correct_model.number=}\n\n")
