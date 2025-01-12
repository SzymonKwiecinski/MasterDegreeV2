from enum import Enum
from pathlib import Path
from typing import Any, Optional

from openai.types.chat import ChatCompletion

from src.templates import (
    data_template,
    latex_math_model_template,
    wrong_code_template,
    code_error_template,
    description_template,
)
import csv
import json
from math import fabs

from pydantic import BaseModel


















# Modele LLM, jakich używamy w danej pracy
class ChatModel(str, Enum):
    GPT_4O = "gpt-4o-2024-08-06"
    GPT_4O_MINI = "gpt-4o-mini-2024-07-18"
# Dostępne role używane w konwersacji
#  z czatem LLM
class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
# Klasa na dane do eksperymentów 2, 3
class Task(BaseModel):
    number: int
    description: str
    data: dict
    obj: float

    @classmethod
    def from_folder(cls, number: int, path: Path | str) -> "Task":
        if isinstance(path, str):
            path = Path(path)

        description_path = path / "description.txt"
        data_path = path / "data.json"
        obj_path = path / "obj.txt"

        return cls(
            number=number,
            description=description_path.read_text(),
            data=json.loads(data_path.read_text()),
            obj=float(obj_path.read_text().replace("OBJ: ", "")),
        )

# Klasa na dane do eksperymentu 1
class CorrectModel(BaseModel):
    number: int
    latex_math_model: str
    data: dict
    obj: float

    @classmethod
    def from_folder(
        cls, number: int, path: Path | str, latex_file: str
    ) -> "CorrectModel":
        if isinstance(path, str):
            path = Path(path)

        latex_math_model_path = path / latex_file
        data_path = path / "data.json"
        obj_path = path / "obj.txt"

        return cls(
            number=number,
            latex_math_model=latex_math_model_path.read_text(),
            data=json.loads(data_path.read_text()),
            obj=float(obj_path.read_text().replace("OBJ: ", "")),
        )

# Warstwa abstrakcji, aby łatwiej
#  manipulować wiadomościami do i z czatu
class Message:
    def __init__(self, role: Role, content: str) -> None:
        self.role = role
        self.content = content

    @classmethod
    def from_system(cls, content: str) -> "Message":
        return cls(role=Role.SYSTEM, content=content)

    @classmethod
    def from_user(cls, content: str) -> "Message":
        return cls(role=Role.USER, content=content)

    @classmethod
    def from_assistant(cls, content: str) -> "Message":
        return cls(role=Role.ASSISTANT, content=content)

    @classmethod
    def from_openai_chat(cls, completion: ChatCompletion) -> "Message":
        _message = completion.choices[0].message
        return cls(role=Role(_message.role), content=_message.content)

    @classmethod
    def from_correct_model(cls, correct_model: CorrectModel) -> "Message":
        return cls.from_user(
            latex_math_model_template.format(model=correct_model.latex_math_model)
            + data_template.format(data=correct_model.data)
        )

    @classmethod
    def from_or_creator(cls, latex_math_model: str, task: Task) -> "Message":
        return cls.from_user(
            latex_math_model_template.format(model=latex_math_model)
            + data_template.format(data=task.data)
        )

    @classmethod
    def from_syntax_error(cls, wrong_code: str, code_error: str) -> "Message":
        return cls.from_user(
            wrong_code_template.format(code=wrong_code)
            + code_error_template.format(error=code_error)
        )

    @classmethod
    def from_task(cls, task: Task) -> "Message":
        return cls.from_user(
            description_template.format(description=task.description)
            + data_template.format(data=task.data)
        )

    def dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}
# Klasa na dane dla Ekspertów
class Expert:
    def __init__(
        self,
        name: str,
        background: str,
        role: Role = Role.SYSTEM,
    ) -> None:
        self.name = name
        self.background = background
        self.role = role

    def __repr__(self):
        return f"{self.background} | {self.role}"
# Warstwa abstrakcji pozwalająca łatwiej
#  korzystać z API openai
class OpenAiPrompt:
    def __init__(
        self,
        client: Any,
        expert: Expert,
        log_dir: Path | None = None,
        temperature: float = 0,
    ):
        self.client = client
        self.expert = expert
        self.log_dir = log_dir
        self.temperature = temperature

        self.messages: list[Message] = []
        self.raw_message_response: Optional[Any] = None
        self.message_response: Optional[Message] = None

    def add_messages(self, messages: list[Message]) -> None:
        for message in messages:
            self.messages.append(message)

    def clear_messages(self) -> None:
        self.messages = None
        self.raw_message_response = None
        self.message_response = None

    def run(self, model: ChatModel) -> ChatCompletion:
        _messages: list[dict[str, str]] = [
            {"role": self.expert.role, "content": self.expert.background}
        ]
        for message in self.messages:
            _messages.append(message.dict())

        self.raw_message_response: ChatCompletion = self.client.chat.completions.create(
            model=model.value, messages=_messages, temperature=self.temperature
        )

        self.add_messages([Message.from_openai_chat(self.raw_message_response)])

        self.log()
        return self.raw_message_response

    def log(self) -> None:
        _log_file_name = "logs.md"
        _log_file = self.log_dir / _log_file_name

        with open(_log_file, "a") as f:
            f.write(f"# START: {self.expert.name} \n")
            f.write(f"## START ROLE MESSAGE | {self.expert.role} \n")
            f.write(f"Background: {self.expert.background} \n")
            for i, _msg in enumerate(self.messages):
                f.write(f"## START MESSAGE {i} \n")
                f.write(f"### ROLE: {_msg.role}\n")
                _content = _msg.content
                for _ in reversed(["# ", "## ", "### "]):
                    if _ in _content:
                        _content = _content.replace(_, "#### ")
                f.write(f"{_content}\n\n")
# Warstwa abstrakcji pozwalająca dodawać
#  w łatwy sposób tworzyć raport na podstawie
#  przebiegu eksperymentu dla jednego zadania
class Report(BaseModel):
    experiment_name: str
    experiment_iteration: int
    task_number: int  # folder name
    code_fix_count: int = 0  # how many times code was fixed , can be 0
    code_syntax_status: bool = False  #
    obj_expected: Any | None = None
    obj_given: Any | None = None
    obj_status: bool = False  # 0.1% far from correct value:)
    sum_prompt_tokens: int = 0
    sum_completion_tokens: int = 0
    sum_prompt_tokens_price: float = 0.0
    sum_completion_tokens_price: float = 0.0
    sum_price: float = 0.0

    def update_tokens(self, chat_completion: ChatCompletion) -> None:
        self.sum_prompt_tokens += chat_completion.usage.prompt_tokens
        self.sum_completion_tokens += chat_completion.usage.completion_tokens
        model = ChatModel(chat_completion.model)

        self.sum_prompt_tokens_price += (
            PRICE_MAPPER_PROMPT_PER_MILION_TOKENS[model]
            * chat_completion.usage.prompt_tokens
            / (10**6)
        )

        self.sum_completion_tokens_price += (
            PRICE_MAPPER_COMPLETION_PER_MILION_TOKENS[model]
            * chat_completion.usage.completion_tokens
            / (10**6)
        )

    def save(self, path: Path, file_name: str = "report.csv") -> None:
        _report_path = path / file_name
        _headers = [_ for _ in self.dict().keys()]

        if isinstance(self.obj_expected, float) and isinstance(self.obj_given, float):
            if self.obj_given == 0:
                self.obj_status = False
            elif (
                int(fabs((self.obj_given - self.obj_expected) / self.obj_given) * 100)
                <= 0.1
            ):
                self.obj_status = True

        self.sum_price = self.sum_prompt_tokens_price + self.sum_completion_tokens_price

        if not _report_path.exists():
            with open(_report_path, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=_headers)
                writer.writeheader()

        with open(_report_path, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=_headers)
            writer.writerow(self.dict())


PRICE_MAPPER_PROMPT_PER_MILION_TOKENS: dict[ChatModel, float] = {
    ChatModel.GPT_4O: 2.50,
    ChatModel.GPT_4O_MINI: 0.15,
}

PRICE_MAPPER_COMPLETION_PER_MILION_TOKENS: dict[ChatModel, float] = {
    ChatModel.GPT_4O: 10.0,
    ChatModel.GPT_4O_MINI: 0.60,
}

