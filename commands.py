from login import FacebookLogIn
from scraper import FacebookScraper
from typing import Optional
import typer
from main import app


@app.command()
def login_2_step():
    """
    Log in to facebook account with 2-step authentication
    """
    typer.echo("Logging in")
    facebook = FacebookLogIn()
    facebook.login_2_step()


@app.command()
def login():
    """
    Log in to facebook account without 2-step authentication
    """
    typer.echo("Logging in")
    facebook = FacebookLogIn()
    facebook.login_no_verification()


@app.command()
def scrape(name: Optional[str] = None):
    if name:
        typer.echo(f"Start scraping friend list for {name}")
        facebook = FacebookScraper(name)
        facebook.pipeline()
    typer.echo("Invalid name")
