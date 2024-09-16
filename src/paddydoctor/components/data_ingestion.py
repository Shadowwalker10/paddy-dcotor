## Update Components
import os
from kaggle.api.kaggle_api_extended import KaggleApi
from paddydoctor.logging import logger
import zipfile
from paddydoctor.utils.common import *
from paddydoctor.entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.api = KaggleApi()
        self.api.authenticate()
    
    def download_files(self):
        if not os.path.exists(os.path.join(self.config.local_data_file, "train.csv")) and (get_size(Path(os.path.join(self.config.local_data_file, "train_images"))))<100:
            logger.info(f"Downloading Dataset: {self.config.dataset_name} to directory: {self.config.local_data_file}")
            ## Downloading
            self.api.competition_download_files(competition = self.config.dataset_name, 
                                            path = self.config.local_data_file)
            logger.info("Files Downloaded Successfully")

            ## Unzipping
            zipfile_path = os.path.join(self.config.local_data_file, f"{self.config.dataset_name}.zip")

            if zipfile.is_zipfile(zipfile_path):
                with zipfile.ZipFile(zipfile_path, "r") as zip_ref:
                    zip_ref.extractall(path = self.config.local_data_file)
                    logger.info(f"Files Successfully unzipped to {self.config.local_data_file}")
                os.remove(zipfile_path)
                
            
            else:
                logger.error(f"{zipfile_path} is not a valid zip file")
        else:
            logger.info("File already Downloaded")
            return