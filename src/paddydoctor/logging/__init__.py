import os
import sys
import logging
from pathlib import Path

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
logging_filepath = "./logs/running_logs.log"

os.makedirs(str(Path(logging_filepath).parent), exist_ok = True)
Path(logging_filepath).touch(exist_ok = True)

logging.basicConfig(level = logging.INFO, 
                    format = logging_str, handlers = [logging.FileHandler(logging_filepath), 
                                                      logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("paddylogger")

