from src.const import (
    CORRECT_MODELS_PATH,
    EXPERIMENT_3_PATH,
    ABS_PYTHON_INTERPRETER,
    ALL_DATA_PATH,
)
from src.experts import PY_C_EXPERT, PY_F_EXPERT, OR_C_EXPERT
from src.helpers import (
    chat_completion_to_python_file,
    run_python_code,
    extract_objective_from_text,
    chat_completion_to_latex_file,
    chat_completion_to_latex_text,
)
from src.core import CorrectModel, Report, Task
from src.core import ChatModel, OpenAiPrompt, Message
from src.templates import (
    python_file_name_template,
    description_template,
    latex_file_name_template,
)
from openai import Client

TASKS_NUMBER = 63  # 63
EXP_RETRY = 10  # 10


def run(
    client: Client,
    or_c_model: ChatModel,
    py_c_model: ChatModel,
    py_f_model: ChatModel,
    experiment_name: str,
    fix_retries: int = 0,
):
    experiment_path = EXPERIMENT_3_PATH / experiment_name
    experiment_path.mkdir(exist_ok=True)

    tasks = []
    for i in range(1, TASKS_NUMBER + 1):
        tasks.append(Task.from_folder(number=i, path=ALL_DATA_PATH / str(i)))

    for exp_retry in range(1, EXP_RETRY + 1):
        if experiment_name in ["experiment_3b2", "experiment_3b3"]:
            if exp_retry <= 7:
                continue

        if experiment_name in ["experiment_3b4"]:
            if exp_retry <= 6:
                continue

        retry_experiment_path = experiment_path / str(exp_retry)
        retry_experiment_path.mkdir(exist_ok=True)

        for task in tasks:
            print(f"START {exp_retry=}, {task.number=}\n")
            model_path = retry_experiment_path / str(task.number)
            model_path.mkdir(exist_ok=True)
            report = Report(
                experiment_name=experiment_name,
                experiment_iteration=exp_retry,
                task_number=task.number,
                obj_expected=task.obj,
            )

            or_c_prompt = OpenAiPrompt(
                client=client, expert=OR_C_EXPERT, log_dir=model_path, temperature=0.9
            )

            py_c_prompt = OpenAiPrompt(
                client=client, expert=PY_C_EXPERT, log_dir=model_path, temperature=0.9
            )

            py_f_prompt = OpenAiPrompt(
                client=client, expert=PY_F_EXPERT, log_dir=model_path, temperature=0.9
            )
            ### model
            or_c_prompt.add_messages(
                [
                    Message.from_user(
                        description_template.format(description=task.description)
                    )
                ]
            )

            chat_completion_or_c = or_c_prompt.run(model=or_c_model)
            report.update_tokens(chat_completion_or_c)

            chat_completion_to_latex_file(
                abs_path=model_path / latex_file_name_template.format(number=0),
                chat_completion=chat_completion_or_c,
            )

            ###

            py_c_prompt.add_messages(
                [
                    Message.from_or_creator(
                        latex_math_model=chat_completion_to_latex_text(
                            chat_completion_or_c
                        ),
                        task=task,
                    )
                ]
            )

            chat_completion_py_c = py_c_prompt.run(model=py_c_model)
            report.update_tokens(chat_completion_py_c)

            chat_completion_to_python_file(
                abs_path=model_path
                / python_file_name_template.format(number=report.code_fix_count),
                chat_completion=chat_completion_py_c,
            )

            stderr, stdout, code = run_python_code(
                ABS_PYTHON_INTERPRETER,
                model_path
                / python_file_name_template.format(number=report.code_fix_count),
            )

            for fix_retry in range(fix_retries):
                if not bool(stderr):
                    break

                py_f_prompt.add_messages(
                    [Message.from_syntax_error(wrong_code=code, code_error=stderr)]
                )
                chat_completion_py_f = py_f_prompt.run(model=py_f_model)
                report.update_tokens(chat_completion_py_f)
                report.code_fix_count += 1

                chat_completion_to_python_file(
                    abs_path=model_path
                    / python_file_name_template.format(number=report.code_fix_count),
                    chat_completion=chat_completion_py_f,
                )

                stderr, stdout, code = run_python_code(
                    ABS_PYTHON_INTERPRETER,
                    model_path
                    / python_file_name_template.format(number=report.code_fix_count),
                )

            if not bool(stderr):
                report.code_syntax_status = True
                report.obj_given = extract_objective_from_text(stdout)

            report.save(EXPERIMENT_3_PATH)
            print(f"END {exp_retry=}, {task.number=}\n\n")
