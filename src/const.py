from pathlib import Path

ABS_PYTHON_INTERPRETER = Path(
    "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/bin/python"
)

MAIN_PATH = Path(__file__).parent.parent

ALL_DATA_PATH = MAIN_PATH / "data" / "all"
CORRECT_MODELS_PATH = MAIN_PATH / "data" / "correct_models"

CONFIGS_PATH = MAIN_PATH / "configs"

SRC_PATH = MAIN_PATH / "src"

EXPERIMENT_1_PATH = SRC_PATH / "experiment_1"
EXPERIMENT_2_PATH = SRC_PATH / "experiment_2"
EXPERIMENT_3_PATH = SRC_PATH / "experiment_3"
EXPERIMENT_4_PATH = SRC_PATH / "experiment_4"
EXPERIMENT_5_PATH = SRC_PATH / "experiment_5"
