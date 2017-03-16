# written by 0oSpacebaro0 2017.03.12
import logging
import sys

logger = logging.getLogger("BMP2JPG_Log")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", '%Y %m.%d %H:%M:%S')
logger_handler = logging.StreamHandler(sys.stdout)
logger_handler.setFormatter(formatter)
logger.addHandler(logger_handler)
