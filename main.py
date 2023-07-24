import typer
from login import FacebookLogIn
from scraper import FacebookScraper
from typing import Optional

app = typer.Typer()


@app.command()
def login():
    typer.echo("Logging in")
    facebook = FacebookLogIn()
    facebook.login_2_step()


@app.command()
def scrape(name: Optional[str] = None):
    if name:
        typer.echo(f"Start scraping friend list for {name}")
        facebook = FacebookScraper(name)
        facebook.pipeline()
    typer.echo("Invalid name")


if __name__ == "__main__":
    app()
