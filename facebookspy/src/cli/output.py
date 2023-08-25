from typing import List, Dict


def print_data_from_list_of_dict(data: List[Dict]) -> None:
    pass


def print_string(data: str) -> None:
    pass


def print_list(data: List) -> None:
    pass


def print_no_data_info() -> None:
    message = "No data found"
    print(f"[bold red] {message} [/bold red]")


def print_saving_data_info() -> None:
    message1 = "Do not close the app!"
    message2 = "Saving scraped data"

    print(f"[bold red] {message1} [/bold red] {message2}")
