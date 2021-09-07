import logging
import os
import sys
from logging.handlers import RotatingFileHandler

MAX_BYTES = 10000000
BACKUP_COUNT = 5


def init():
    os.makedirs("./logs", exist_ok=True)
    # create stream handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    # create a log file handler
    # combained_log_handler = logging.FileHandler('logs/logs.log')
    combained_log_handler = RotatingFileHandler('logs/logs.log', maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    combained_log_handler.setLevel(logging.DEBUG)
    # create an error only log file handler
    # error_log_handler = logging.FileHandler('logs/logs.err.log')
    error_log_handler = RotatingFileHandler('logs/logs.err.log', maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    error_log_handler.setLevel(logging.WARNING)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(name)s:%(funcName)s] %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        handlers=[stream_handler, combained_log_handler, error_log_handler]
    )