## Update configuration manager
from paddydoctor.constants import *
from paddydoctor.utils.common import *
from paddydoctor.entity import DataIngestionConfig


class ConfigurationManager:
    def __init__(self, config_filepath = CONFIG_FILEPATH, 
                 params_filepath = PARAMS_FILEPATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories_files([self.config.artifacts_root])

    def get_data_ingestion_config(self)->DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories_files([config.root_dir])
        data_ingestion_config = DataIngestionConfig(root_dir = config.root_dir, 
                                                    dataset_name = config.dataset_name, 
                                                    local_data_file = config.local_data_file, 
                                                    class_weight = config.class_weight)
        return data_ingestion_config
        