import json
from typing import List, Dict, Any
from datetime import datetime

INDENT = 4
ENSURE_ASCII = False


class SaveJSON:
    def __init__(self, facebook_id: str, data: List[Dict[str, Any]] | List[str], ):
        self.facebook_id = facebook_id
        self.data = data

    @staticmethod
    def get_timestamp() -> str:
        """ Generate timestamp """
        dt = datetime.now()
        timestamp = datetime.timestamp(dt)
        return str(timestamp).replace(" ", "_")

    def generate_file_name(self) -> str:
        """ Generate filename including module name, facebook id and timestamp """
        filename = f"{self.facebook_id}_{self.get_timestamp()}.json"
        return filename

    def save(self) -> None:
        """ Save scraped data to JSON file """
        with open(self.generate_file_name(), "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=INDENT, ensure_ascii=ENSURE_ASCII)

