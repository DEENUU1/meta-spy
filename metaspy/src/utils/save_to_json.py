import json
from typing import List, Dict, Any
from datetime import datetime
from ..config import Config
import os

config = Config()


class SaveJSON:
    def __init__(
        self,
        facebook_id: str,
        data: List[Dict[str, Any]] | List[str],
    ):
        self.facebook_id = facebook_id
        self.data = data

    @staticmethod
    def get_timestamp() -> str:
        """Generate timestamp"""
        dt = datetime.now()
        timestamp = datetime.timestamp(dt)
        return str(timestamp).replace(" ", "_")

    def generate_file_name(self) -> str:
        """Generate filename including module name, facebook id and timestamp"""
        filename = f"{self.facebook_id}_{self.get_timestamp()}.json"
        return filename

    def save(self) -> None:
        """Save scraped data to JSON file"""
        dir = Config.JSON_FILE_PATH
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(f"{dir}/{self.generate_file_name()}", "w", encoding="utf-8") as f:
            json.dump(
                self.data, f, indent=config.INDENT, ensure_ascii=config.ENSURE_ASCII
            )
