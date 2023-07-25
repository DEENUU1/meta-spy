from dotenv import load_dotenv
from login import FacebookLogIn, login_2_step, login_no_verification
from scraper import FacebookScraper
from typing import Optional
import typer


load_dotenv()
app = typer.Typer()


@app.command()
def login_2_step():
    """
    Log in to facebook account with 2-step authentication
    """
    typer.echo("Logging in")
    facebook = FacebookLogIn()
    login_2_step(facebook)


@app.command()
def login():
    """
    Log in to facebook account without 2-step authentication
    """
    typer.echo("Logging in")
    facebook = FacebookLogIn()
    login_no_verification(facebook)


@app.command()
def scrape(name: Optional[str] = None):
    if name:
        typer.echo(f"Start scraping friend list for {name}")
        facebook = FacebookScraper(name)
        facebook.pipeline()
    typer.echo("Invalid name")


if __name__ == "__main__":
    app()
