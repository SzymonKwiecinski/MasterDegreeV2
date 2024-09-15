from src.const import CORRECT_MODELS_PATH, EXPERIMENT_5_PATH, ABS_PYTHON_INTERPRETER
from src.experts import PY_C_EXPERT
from src.helpers import (
    chat_completion_to_python_file,
    run_python_code,
    extract_objective_from_text,
)
from src.core import CorrectModel, Report
from src.core import ChatModel, OpenAiPrompt, Message
from src.templates import file_name_template
from openai import Client


def run(
    client: Client,
    py_c_model: ChatModel,
    py_f_model: ChatModel,
    experiment_name: str,
    retries: int = 0,
):
    experiment_path = EXPERIMENT_5_PATH / experiment_name
    experiment_path.mkdir(exist_ok=True)

    correct_models = []
    for i in range(1, 19):  # range(1, 19):
        correct_models.append(
            CorrectModel.from_folder(number=i, path=CORRECT_MODELS_PATH / str(i))
        )

    for exp_retry in range(1, 2):
        retry_experiment_path = experiment_path / str(exp_retry)
        retry_experiment_path.mkdir(exist_ok=True)

        for correct_model in correct_models:
            model_path = retry_experiment_path / str(correct_model.number)
            model_path.mkdir(exist_ok=True)
            report = Report(
                task_number=correct_model.number, obj_expected=correct_model.obj
            )

            py_c_prompt = OpenAiPrompt(
                client=client, expert=PY_C_EXPERT, log_dir=model_path
            )

            py_c_prompt.add_messages([Message.from_correct_model(correct_model)])

            chat_completion_py_c = py_c_prompt.run(model=py_c_model)

            chat_completion_to_python_file(
                dir=model_path,
                file_name=file_name_template.format(number=report.code_fix_count),
                chat_completion=chat_completion_py_c,
            )

            stderr, stdout = run_python_code(
                ABS_PYTHON_INTERPRETER,
                model_path / file_name_template.format(number=report.code_fix_count),
            )
            if bool(stderr):
                report.code_syntax_status = False
            else:
                report.code_syntax_status = True
                report.obj_given = extract_objective_from_text(stdout)

            report.update_tokens(chat_completion_py_c)
            report.save(retry_experiment_path)

            # TODO: add retry!!
            # for fix_retry in range(retries):
            #     # chat_completion = py_c_prompt.run(model=py_c_model)

            # chat_completion_to_python_file(
            #     dir=retry_experiment_path,
            #     file_name=file_name_template.format(number=1),
            #     chat_completion=py_c_prompt.run(model=py_c_model),
            # )
