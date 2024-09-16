from paddydoctor.config.configuration import ConfigurationManager
from paddydoctor.components.data_ingestion import DataIngestion
import os
from paddydoctor.utils.common import save_json
from pathlib import Path


class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config = data_ingestion_config)
        data_ingestion.download_files()


        to_check = os.path.join(data_ingestion_config.local_data_file, "train_images")
        classes = os.listdir(to_check)
        paths = [os.path.join(to_check, c) for c in classes]
        lengths = [(c,len(os.listdir(p))) for (p,c) in zip(paths,classes)]
        total = sum([x[1] for x in lengths])
        class_weights = {c:total/count for c,count in lengths}
        save_json(Path(data_ingestion_config.class_weight), class_weights)