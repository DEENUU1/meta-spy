import logging

from .config import Config


class Logs(logging.Logger):
    """Logs class"""

    def __init__(self, name="logger", level=logging.ERROR):
        super().__init__(name, level=level)
        file_handler = logging.FileHandler(Config.LOG_FILE_PATH)
        file_handler.setLevel(level)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.addHandler(file_handler)

    def log_error(self, message):
        """Logs error message"""
        self.error(message)
