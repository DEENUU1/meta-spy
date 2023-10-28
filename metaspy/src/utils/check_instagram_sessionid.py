import os

from ..config import Config
from rich import print as rprint
from dotenv import load_dotenv


load_dotenv()


def check_instagram_sessionid() -> bool:
    """Check if sessionid is added do .env file"""

    if not os.getenv("INSTAGRAM_SESSIONID_VALUE"):
        rprint(
            "[bold red]\n\nPlease set the Instagram session ID in the .env file.\n\n[/bold red]"
        )
        return False
    else:
        return True
