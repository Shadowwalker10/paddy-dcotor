import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "paddy-doctor"

lst_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/components/data_ingestion.py",
    f"src/{project_name}/components/prepare_base_model.py",
    f"src/{project_name}/components/prepare_callbacks.py",
    f"src/{project_name}/components/model_training.py",
    f"src/{project_name}/components/model_evaluation.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/pipeline/stage_01_data_ingestion.py",
    f"src/{project_name}/pipeline/stage_02_prepare_base_model.py",
    f"src/{project_name}/pipeline/stage_03_model_trainer.py",
    f"src/{project_name}/pipeline/stage_04_model_evaluation.py",
    f"src/{project_name}/pipeline/predict.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    f"src/{project_name}/logging/__init__.py",
    "config/config.yaml",
    "params/params.yaml",
    "requirements.txt",
    "setup.py",
    "app.py",
    "dvc.yaml",
    "research/trials.ipynb",
    "templates/index.html",
    "static/js/script.js",
    "static/css/style.css",
    "research/01_data_ingestion.ipynb",
    "research/02_prepare_base_model.ipynb",
    "research/03_prepare_callbacks.ipynb",
    "research/04_model_trainer.ipynb",
    "research/05_model_evaluation.ipynb"
]

directories = {str(Path(p).parent) for p in lst_of_files}
[os.makedirs(dir, exist_ok = True) for dir in directories]
logging.info("Parent Directories Created.")

## Creating files inside individual directories
[Path(p).touch(exist_ok=True) for p in lst_of_files]
logging.info("Individual Directories Created.")

