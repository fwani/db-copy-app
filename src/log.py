import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_custom_logger():
    path = os.environ.get('LOG_PATH', "log")
    os.makedirs(path, exist_ok=True)

    logging.basicConfig(level=logging.INFO)

    _formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    trfh = TimedRotatingFileHandler(os.path.join(path, "db_copy_app.log"), when='midnight', interval=1, backupCount=31)
    trfh.setLevel(level=logging.INFO)
    trfh.setFormatter(_formatter)

    logger = logging.getLogger()
    logger.addHandler(trfh)
