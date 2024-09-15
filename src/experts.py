import yaml

from src.const import CONFIGS_PATH
from src.core import Expert

with open(f"{CONFIGS_PATH}/experts.yml", "r") as file:
    experts_config = yaml.safe_load(file)

OnePrompt = Expert(name="OnePrompt", background=experts_config["OnePrompt"])
OR_C_EXPERT = Expert(name="OR_C", background=experts_config["OR_C"])
PY_C_EXPERT = Expert(name="PY_C", background=experts_config["PY_C"])
PY_F_EXPERT = Expert(name="PY_F", background=experts_config["PY_F"])
