import shlex
import subprocess
from pathlib import Path
import re
from openai.types.chat import ChatCompletion


def extract_code_from_text(input_text: str) -> str:
    """Extract code from input text. Code should be between ``` and ```"""
    lines = input_text.split("\n")
    code: list[str] = []
    _flag = False
    for line in lines:
        if "```" in line:
            _flag = not _flag
            continue

        if _flag:
            code.append(line)

    return "\n".join(code)


def extract_objective_from_text(input_text: str) -> float | None:
    obj_given = re.search(
        "<OBJ>(.*?)</OBJ>", input_text, flags=re.RegexFlag.MULTILINE
    ).group(1)
    try:
        return float(obj_given)
    except Exception:
        return None


def run_python_code(
    abs_python_interpreter_path: Path, abs_code_path: Path
) -> tuple[str, str]:
    """

    :param abs_python_interpreter_path:
    :param abs_code_path:
    :return: stderror, stdoutput
    """
    if not abs_python_interpreter_path.is_absolute() or not abs_code_path.is_absolute():
        raise ValueError(
            f"Provide absolute path?? {abs_python_interpreter_path=}, {abs_code_path=}"
        )

    response = subprocess.run(
        shlex.split(f"{abs_python_interpreter_path} {abs_code_path}.py"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=4,
    )

    return response.stderr.decode(), response.stdout.decode()


def chat_completion_to_string(chat_completion: ChatCompletion) -> str:
    return chat_completion.choices[0].message.content


def string_to_python_file(dir: Path, file_name: str, context: str) -> None:
    with open(dir.joinpath(file_name + ".py"), "w") as f:
        f.write(extract_code_from_text(context))


def chat_completion_to_python_file(
    dir: Path, file_name: str, chat_completion: ChatCompletion
):
    with open(dir.joinpath(file_name + ".py"), "w") as f:
        f.write(extract_code_from_text(chat_completion.choices[0].message.content))


def string_to_latex_file(dir: Path, file_name: str, context: str):
    with open(dir.joinpath(file_name + ".tex"), "w") as f:
        f.write(extract_code_from_text(context))


def chat_completion_to_latex_file(
    dir: Path, file_name: str, chat_completion: ChatCompletion
):
    with open(dir.joinpath(file_name + ".tex"), "w") as f:
        f.write(extract_code_from_text(chat_completion.choices[0].message.content))
