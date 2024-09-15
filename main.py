import os

from dotenv import load_dotenv

from src.core import ChatModel
from src.experiment_5 import run
from openai import Client

load_dotenv()

run.run(
    client=Client(api_key=os.environ["OPENAI_API_KEY"]),
    py_c_model=ChatModel.GPT_4O_MINI,
    py_f_model=ChatModel.GPT_4O_MINI,
    experiment_name="1",
)
