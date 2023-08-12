import logging
from .config import Config


class Logs(logging.Logger):
    def __init__(self, level=logging.ERROR):
        super().__init__(level=level)
        file_handler = logging.FileHandler(Config.LOG_FILE_PATH)
        file_handler.setLevel(level)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.addHandler(file_handler)

    def log_error(self, message):
        self.error(message)
