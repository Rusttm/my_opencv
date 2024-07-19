import logging
from logging.handlers import RotatingFileHandler
import os

class BOTPkgLogger(object):
    logger_name = f"{os.path.basename(__file__)}"
    logs_dir = "logs"
    logger = None

    def __init__(self):
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.DEBUG)
        if self.logger.hasHandlers(): self.logger.handlers.clear()
        logs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.logs_dir, self.logger_name)
        logger_handler = RotatingFileHandler(f"{logs_path}.log", mode="a", backupCount=0, maxBytes=2 * 1024 * 1024, delay=False)
        # logger_handler = logging.FileHandler("controller.log", mode="w")
        logger_formatter = logging.Formatter("%(asctime)s,%(msecs)d %(name)s %(levelname)s msg: %(message)s")
        logger_handler.setFormatter(logger_formatter)
        self.logger.addHandler(logger_handler)


if __name__ == '__main__':
    connector = BOTPkgLogger()
    connector.logger.info("resting")
