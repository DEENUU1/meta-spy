from dotenv import load_dotenv
from login import FacebookLogIn
from account import AccountScraper, FriendListScraper
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
        scraper = AccountScraper(name)
        scraper.pipeline()
    typer.echo("Invalid name")


@app.command()
def scrape_friend_list(name: Optional[str] = None):
    if name:
        typer.echo(f"Start scraping friend list for {name}")
        scraper = FriendListScraper(name)
        scraper.pipeline()
    typer.echo("Invalid name")


if __name__ == "__main__":
    app()
