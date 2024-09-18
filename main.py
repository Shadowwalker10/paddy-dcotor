from paddydoctor.logging import logger
import os
from paddydoctor.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from paddydoctor.pipeline.stage_02_prepare_base_model import PrepareBaseModelPipeline

STAGE_NAME = "DATA INGESTION STAGE"
try:
    logger.info(f"<<<<<{STAGE_NAME} Started>>>>>")
    obj = DataIngestionPipeline()
    obj.main()
    logger.info(f"<<<<<{STAGE_NAME} Successfully Completed>>>>>")

except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "PREPARE BASE MODEL"
try:
    logger.info(f"<<<<<{STAGE_NAME}>>>>>")
    obj = PrepareBaseModelPipeline()
    obj.main()
    logger.info(f"<<<<<{STAGE_NAME} Successfully Completed>>>>>")
except Exception as e:
    logger.exception(e)
    raise e