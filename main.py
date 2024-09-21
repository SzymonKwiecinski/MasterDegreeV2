import os

import yaml
from dotenv import load_dotenv

from src.const import CONFIGS_PATH
from src.core import ChatModel
from openai import Client

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def run_experiment_1():
    from src.experiment_1 import run

    with open(f"{CONFIGS_PATH}/experiment_1.yml", "r") as file:
        experiments_config = yaml.safe_load(file)

    for experiment_name, experiment_config in experiments_config.items():
        if experiment_name == "experiment_14":
            run(
                client=Client(api_key=OPENAI_API_KEY),
                py_c_model=ChatModel(experiment_config["py_c_model"]),
                py_f_model=ChatModel(experiment_config["py_f_model"]),
                experiment_name=experiment_name,
                fix_retries=experiment_config["fix_retries"],
            )
