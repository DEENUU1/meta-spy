from typing import List, Dict


def print_data_from_list_of_dict(data: List[Dict]) -> None:
    print("[bold green] Scraped data: [/bold green]")

    for entry in data:
        for key, value in entry.items():
            print(f" - {key}: {value}")


def print_string(data: str) -> None:
    print("[bold green] Scraped data: [/bold green]")
    print(f" - {data}")


def print_list(data: List) -> None:
    print("[bold green] Scraped data: [/bold green]")

    for item in data:
        print(f" - {item}")


def print_no_data_info() -> None:
    message = "No data found"
    print(f"[bold red] {message} [/bold red]")
