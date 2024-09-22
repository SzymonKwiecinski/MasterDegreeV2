from src.const import ALL_DATA_PATH, EXPERIMENT_2_PATH, ABS_PYTHON_INTERPRETER
from src.experts import PY_C_EXPERT, PY_F_EXPERT, OnePrompt
from src.helpers import (
    chat_completion_to_python_file,
    run_python_code,
    extract_objective_from_text,
)
from src.core import CorrectModel, Report, Task
from src.core import ChatModel, OpenAiPrompt, Message
from src.templates import python_file_name_template, code_error_template
from openai import Client

TASKS_NUMBER = 60  # 63
EXP_RETRY = 1  # 10


def run(
    client: Client,
    one_prompt_model: ChatModel,
    experiment_name: str,
    fix_retries: int = 0,
):
    experiment_path = EXPERIMENT_2_PATH / experiment_name
    experiment_path.mkdir(exist_ok=True)

    tasks = []
    for i in range(1, TASKS_NUMBER + 1):
        tasks.append(Task.from_folder(number=i, path=ALL_DATA_PATH / str(i)))

    for exp_retry in range(1, EXP_RETRY + 1):
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

            one_prompt = OpenAiPrompt(
                client=client, expert=OnePrompt, log_dir=model_path, temperature=0.9
            )

            one_prompt.add_messages([Message.from_task(task)])

            chat_completion_one_prompt = one_prompt.run(model=one_prompt_model)
            report.update_tokens(chat_completion_one_prompt)

            chat_completion_to_python_file(
                abs_path=model_path
                / python_file_name_template.format(number=report.code_fix_count),
                chat_completion=chat_completion_one_prompt,
            )

            stderr, stdout, code = run_python_code(
                ABS_PYTHON_INTERPRETER,
                model_path
                / python_file_name_template.format(number=report.code_fix_count),
            )

            for fix_retry in range(fix_retries):
                if not bool(stderr):
                    break

                one_prompt.add_messages(
                    [
                        Message.from_user(content="Fix the code based on the error"),
                        Message.from_user(
                            content=code_error_template.format(error=stderr)
                        ),
                    ]
                )
                chat_completion_one_prompt = one_prompt.run(model=one_prompt_model)
                report.update_tokens(chat_completion_one_prompt)
                report.code_fix_count += 1

                chat_completion_to_python_file(
                    abs_path=model_path
                    / python_file_name_template.format(number=report.code_fix_count),
                    chat_completion=chat_completion_one_prompt,
                )

                stderr, stdout, code = run_python_code(
                    ABS_PYTHON_INTERPRETER,
                    model_path
                    / python_file_name_template.format(number=report.code_fix_count),
                )

            if not bool(stderr):
                report.code_syntax_status = True
                report.obj_given = extract_objective_from_text(stdout)

            report.save(EXPERIMENT_2_PATH)
            print(f"END {exp_retry=}, {task.number=}\n\n")
