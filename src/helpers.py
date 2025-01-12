import shlex
import subprocess
from pathlib import Path
import re
from openai.types.chat import ChatCompletion

# znajduje kod PYTHON lub LATEX w podanym tekście i go zwraca
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
# znajduje obliczoną funkcje celu pomiędzy <OBJ></OBJ> w podanym tekście
def extract_objective_from_text(input_text: str) -> float | None:
    try:
        obj_given = re.search(
            "<OBJ>(.*?)</OBJ>", input_text, flags=re.RegexFlag.MULTILINE
        ).group(1)
        return float(obj_given)
    except Exception:
        return None
# uruchamia wskazany kod python za pomocą wybranego interpretera Python
def run_python_code(abs_python_interpreter_path: Path, abs_code_path: Path) -> tuple[str, str, str]:
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
# na podstawie odpowiedzi udzielonej przez czat LLM zwraca sam jej tekst
def chat_completion_to_text(chat_completion: ChatCompletion) -> str:
    return chat_completion.choices[0].message.content
# znajduje kod Python w odpowiedzi z czatu i zapisuje go do osobnego pliku
def chat_completion_to_python_file(abs_path: Path, chat_completion: ChatCompletion) -> None:
    if ".py" not in abs_path.name:
        raise ValueError(f"{abs_path.name=} should has '.py'!")

    text = chat_completion_to_text(chat_completion)

    abs_path.write_text(extract_code_from_text(text))
# znajduje kod LATEX w odpowiedzi z czatu i zwraca go jako odpowiedź funkcji
def chat_completion_to_latex_text(chat_completion: ChatCompletion) -> str:
    text = chat_completion_to_text(chat_completion)
    if "```latex" not in text:
        raise ValueError("```latex not found in text")
    # return chat_completion.choices[0].message.content
    return extract_code_from_text(text)
# znajduje kod LATEX w odpowiedzi z czatu i zapisuje go do osobnego pliku
def chat_completion_to_latex_file(abs_path: Path, chat_completion: ChatCompletion) -> None:
    text = chat_completion_to_text(chat_completion)
    if "```latex" not in text:
        raise ValueError("```latex not found in text")
    abs_path.write_text(extract_code_from_text(text))




# not used
def text_to_python_file(abs_path: Path, context: str) -> None:
    if ".py" not in abs_path.name:
        raise ValueError(f"{abs_path.name=} should has '.py'!")

    abs_path.write_text(extract_code_from_text(context))