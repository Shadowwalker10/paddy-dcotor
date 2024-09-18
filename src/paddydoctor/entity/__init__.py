## Update Entity for Data Ingestion
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen = True)
class DataIngestionConfig:
    root_dir: Path
    dataset_name: str
    local_data_file: Path
    class_weight: Path


@dataclass
class PrepareBaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    params_weights: str
    params_input_shape: list
    freeze_all: bool
    freeze_till: int
    learning_rate: float
    classes: int
    dropout_rate:float
    l2_weight_decay: float
    l1_weight_decay: float
