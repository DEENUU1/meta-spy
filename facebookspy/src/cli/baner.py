BANNER = """
        ███████╗ █████╗  ██████╗███████╗██████╗  ██████╗  ██████╗ ██╗  ██╗    ███████╗██████╗ ██╗   ██╗
        ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗██╔═══██╗██║ ██╔╝    ██╔════╝██╔══██╗╚██╗ ██╔╝
        █████╗  ███████║██║     █████╗  ██████╔╝██║   ██║██║   ██║█████╔╝     ███████╗██████╔╝ ╚████╔╝ 
        ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗██║   ██║██║   ██║██╔═██╗     ╚════██║██╔═══╝   ╚██╔╝  
        ██║     ██║  ██║╚██████╗███████╗██████╔╝╚██████╔╝╚██████╔╝██║  ██╗    ███████║██║        ██║   
        ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚══════╝╚═╝        ╚═╝   
    """


import os
from platform import system

from rich.align import Align
from rich.panel import Panel
from rich.text import Text

from .version import VERSION


def get_terminal_width() -> int:
    """
    Gets the width of the terminal.

    Returns:
        int: width of the terminal.
    """
    try:
        width, _ = os.get_terminal_size()
    except OSError:
        width = 80

    if system().lower() == "windows":
        width -= 1

    return width


def print_banner(console) -> None:
    width = get_terminal_width()
    height = 10

    panel = Panel(
        Align(
            Text(BANNER, style="green"),
            vertical="middle",
            align="center",
        ),
        width=width,
        height=height,
        subtitle=f"[bold blue]v.{VERSION}[/bold blue]",
    )
    console.print(panel)
