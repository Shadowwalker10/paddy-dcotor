## Update configuration manager
from paddydoctor.constants import *
from paddydoctor.utils.common import *
from paddydoctor.entity import DataIngestionConfig, PrepareBaseModelConfig, PrepareCallbacksConfig


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
    
    def get_prepare_base_model_config(self)->PrepareBaseModelConfig:
        config = self.config.prepare_base_model
        create_directories_files([config.root_dir])
        prepare_base_model_config = PrepareBaseModelConfig(root_dir = config.root_dir, 
                                                        base_model_path = config.base_model_path, 
                                                        updated_base_model_path = config.updated_base_model_path, 
                                                        params_weights = self.params.weights,
                                                        params_input_shape=self.params.input_shape,
                                                        freeze_all = self.params.freeze_all, 
                                                        freeze_till = self.params.freeze_till, 
                                                        learning_rate = self.params.learning_rate, 
                                                        classes = self.params.classes,
                                                        dropout_rate = self.params.dropout_rate,
                                                        l2_weight_decay = self.params.l2_weight_decay,
                                                        l1_weight_decay = self.params.l1_weight_decay)
        
        return prepare_base_model_config
    
    def get_prepare_callbacks_config(self):
        config = self.config.prepare_callbacks
        
        create_directories_files([config.root_dir])
        create_directories_files([config.tensorboard_root_log_dir])
        create_directories_files([os.path.dirname(config.checkpoint_model_filepath)])


        prepare_callbacks_config = PrepareCallbacksConfig(root_dir = Path(config.root_dir), 
                                                          tensorboard_root_log_dir = Path(config.tensorboard_root_log_dir),
                                                          checkpoint_model_filepath = Path(config.checkpoint_model_filepath),
                                                          learning_rate = self.params.learning_rate,
                                                          lr_reduce_factor = self.params.lr_reduce_factor, 
                                                          lr_reduce_patience = self.params.lr_reduce_patience,
                                                          min_lr = self.params.min_lr, 
                                                          early_stopping_patience = self.params.early_stopping_patience,
                                                          early_stopping_delta = self.params.early_stopping_delta
                                                          )
        
        return prepare_callbacks_config

        