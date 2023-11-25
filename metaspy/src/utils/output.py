from typing import List, Dict
from rich import print as rprint


def print_data_from_list_of_dict(data: List[Dict]) -> None:
    rprint("[bold green] Scraped data: [/bold green]")

    for entry in data:
        rprint(f" - {entry}")


def print_data_from_dict(data: Dict) -> None:
    rprint(f"[bold green] Scraped data: [/bold green]")

    rprint(f" - {data}")


def print_string(data: str) -> None:
    rprint("[bold green] Scraped data: [/bold green]")
    rprint(f" - {data}")


def print_list(data: List) -> None:
    rprint("[bold green] Scraped data: [/bold green]")

    for item in data:
        rprint(f" - {item}")


def print_no_data_info() -> None:
    message = "No data found"
    rprint(f"[bold red] {message} [/bold red]")
