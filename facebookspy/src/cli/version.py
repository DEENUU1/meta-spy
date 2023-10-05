from rich import print as rprint
from rich.console import Console

from .baner import print_banner

VERSION = "1.1"


def return_version_info() -> None:
    """
    Return the version of the package.
    """

    console = Console()
    print_banner(console)

    text = f"You are using {VERSION} version of the facebook spy. For more info visit https://github.com/DEENUU1/facebook-spy"
    rprint(text)
