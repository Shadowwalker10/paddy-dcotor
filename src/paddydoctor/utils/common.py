from paddydoctor.logging import logger
import os
import yaml
import json
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
import base64
import zipfile
from typing import Any, List, Tuple
from box.exceptions import BoxValueError

@ensure_annotations
def read_yaml(path_to_yaml_file: Path)->ConfigBox:
    try:
        with open(path_to_yaml_file, "r") as file:
            content = yaml.safe_load(file)
            logger.info(f"{path_to_yaml_file} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("Yaml file is empty")
    except Exception as e:
        logger.exception(e)
        raise e
    
@ensure_annotations
def create_directories_files(lst_path: List, verbose = True):
    directories = [str(Path(p)) for p in lst_path]
    [os.makedirs(dir, exist_ok = True) for dir in directories]

    ## creating files inside directories
    [Path(p).touch(exist_ok = True) for p in lst_path]
    if verbose:
        logger.info("Directories and Files successfully created")


@ensure_annotations
def save_json(save_file_path: Path, content:dict):
    with open(save_file_path, "w") as f:
        json.dump(content, f, indent = 4)
    logger.info(f"Data Saved Successfully to {save_file_path}")

@ensure_annotations
def load_json(file_to_load:Path, verbose = True):
    with open(file_to_load, "r") as file:
        content = json.load(file)
    if verbose: logger.info(f"{file_to_load} loaded successfully")
    return ConfigBox(content)

@ensure_annotations
def decodeImage(Imgstring, filename):
    imgdata = base64.b64decode(Imgstring)
    with open(filename, "wb") as file:
        file.write(imgdata)
    logger.info(f"{filename} updated successfully")

@ensure_annotations
def encode_image_b64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())
    
@ensure_annotations
def extract_zipfile(zipfile_path:Path, output_path: Path):
    logger.info(f"Extracting {zipfile_path} to {output_path}")
    with zipfile.ZipFile(zipfile_path, "r") as zip_ref:
        zip_ref.extractall(output_path)
    logger.info("Files Extracted Successfully")

@ensure_annotations
def get_size(path: Path) -> int:
    try:
        size = os.path.getsize(path)
        return round(size / 1024)  # Return size in kilobytes
    except FileNotFoundError:
        #logger.error(f"File not found: {path}")
        return 0  # Return 0 if file is not found



    