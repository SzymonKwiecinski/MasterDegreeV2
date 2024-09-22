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
    try:
        obj_given = re.search(
            "<OBJ>(.*?)</OBJ>", input_text, flags=re.RegexFlag.MULTILINE
        ).group(1)
        return float(obj_given)
    except Exception:
        return None


def run_python_code(
    abs_python_interpreter_path: Path, abs_code_path: Path
) -> tuple[str, str, str]:
    """

    :param abs_python_interpreter_path:
    :param abs_code_path:
    :return: stderror, stdoutput, code
    """
    if not abs_python_interpreter_path.is_absolute() or not abs_code_path.is_absolute():
        raise ValueError(
            f"Provide absolute path?? {abs_python_interpreter_path=}, {abs_code_path=}"
        )
    if ".py" not in abs_code_path.name:
        raise ValueError(f"{abs_code_path.name=} should has '.py'!")

    try:
        response = subprocess.run(
            shlex.split(f"{abs_python_interpreter_path} {abs_code_path}"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=6,
        )
        return (
            response.stderr.decode(),
            response.stdout.decode(),
            abs_code_path.read_text(),
        )
    except subprocess.TimeoutExpired:
        return (
            "subprocess.TimeoutExpired timed out after 6 seconds. In code can be infinitive loop",
            "",
            abs_code_path.read_text(),
        )


def chat_completion_to_text(chat_completion: ChatCompletion) -> str:
    return chat_completion.choices[0].message.content


def chat_completion_to_python_text(chat_completion: ChatCompletion) -> str:
    return chat_completion.choices[0].message.content


def text_to_python_file(abs_path: Path, context: str) -> None:
    if ".py" not in abs_path.name:
        raise ValueError(f"{abs_path.name=} should has '.py'!")

    abs_path.write_text(extract_code_from_text(context))


def chat_completion_to_python_file(
    abs_path: Path, chat_completion: ChatCompletion
) -> None:
    if ".py" not in abs_path.name:
        raise ValueError(f"{abs_path.name=} should has '.py'!")

    text = chat_completion_to_text(chat_completion)

    abs_path.write_text(extract_code_from_text(text))


#
# def string_to_latex_file(abs_path: Path, context: str):
#     if ".lex" not in abs_path.name:
#         raise ValueError(f"{abs_path.name=} should has '.lex'!")
#
#     abs_path.write_text(extract_code_from_text(context))
#
#
# def chat_completion_to_latex_file(
#     dir: Path, file_name: str, chat_completion: ChatCompletion
# ):
#     with open(dir.joinpath(file_name + ".tex"), "w") as f:
#         f.write(extract_code_from_text(chat_completion.choices[0].message.content))
