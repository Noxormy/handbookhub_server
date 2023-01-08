"""
    This module init logging classes, state format for messages and provide interfaces for creating the new ones
"""

from typing import Callable
import logging

COMMON_FORMAT = "%(levelname)s: (%(filename)s:%(lineno)d): %(message)s"

logger = logging.getLogger("common")
logger.setLevel(logging.DEBUG)


class CustomHandler(logging.Handler):
    """
    CustomHandler class allows easily create new handler via providing log function
            Constructor parameters:
                    log (Callable[[str], None]) - callback function which will be called for every log message
    """
    def __init__(self, log: Callable[[str], None]):
        super().__init__()
        self.log = log

    def emit(self, record) -> None:
        log_entry = self.format(record)
        self.log(log_entry)


def init_logger():
    """
    Init logger with two standard log handlers: FileHandler and StreamHandler
    FileHandler will write logs to "log.txt" file in the root directory
    StreamHandler will write logs to the terminal output
    """
    fh = logging.FileHandler("log.txt")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: (%(filename)s:%(lineno)d %(threadName)s): %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S"
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    formatter = logging.Formatter(COMMON_FORMAT)
    sh.setFormatter(formatter)
    logger.addHandler(sh)


def add_handler(cb: Callable[[str], None], level=logging.ERROR, logs_format=COMMON_FORMAT) -> None:
    """
    Add handler to current logging system
            Parameters:
            cb: Callable[[str], None] - callback which will be used for every log message
            level - level of log messages for the handler
            logs_format - format for log messages
    """
    ch = CustomHandler(cb)
    ch.setLevel(level)
    formatter = logging.Formatter(logs_format)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


if __name__ == "logger":
    init_logger()
