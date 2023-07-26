from rich.console import Console
from rich.table import Table
from rich.text import Text


def display_start_menu():
    console = Console()

    # Application information
    project_name = Text("🕵️Facebook SPY🕵️", justify="center")
    description = (
        "[cyan]This project allows you to log in using Selenium to your Facebook account "
        "(even if you have 2-step verification enabled). You can also scrape user data "
        "based on a given URL address.[/cyan]"
    )
    key_features = [
        "[yellow]Feature 1:[/yellow] Login on Facebook (even with 2-step verification).",
        "[yellow]Feature 2:[/yellow] Save cookies to maintain the login session.",
        "[yellow]Feature 3:[/yellow] Scrape user's friend list.",
        "[yellow]Feature 4:[/yellow] Scrape user's information about work and education.",
        "[yellow]Feature 5:[/yellow] Scrape user's information about places.",
    ]

    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(justify="left")

    table.add_row(project_name)
    table.add_row(description)
    table.add_row("[bold]Key Features:")
    for feature in key_features:
        table.add_row(feature)

    console.print(table)
