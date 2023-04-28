import os
from datetime import datetime

from loguru import logger


class CustomLogger:
    def __init__(self):
        log_file = os.path.join("logs", f"mybot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        self.logger = logger
        self.logger.add(log_file, rotation='1 day', format='{time} {level} {message}')

    def debug(self, message):
        message = str(message)
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
