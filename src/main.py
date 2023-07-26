from dotenv import load_dotenv
from login import FacebookLogIn
from account import AccountScraper, FriendListScraper
from typing import Optional
import typer
from home import display_start_menu
from rich import print
from version import return_version_info


load_dotenv()
app = typer.Typer()


@app.command()
def home():
    display_start_menu()


@app.command()
def version():
    return_version_info()


@app.command()
def login_2_step():
    """
    Log in to facebook account with 2-step authentication
    """
    print("Logging in")
    facebook = FacebookLogIn()
    facebook.login_2_step()
    # TODO add method to check if login was successful and return bool value


@app.command()
def login():
    """
    Log in to facebook account without 2-step authentication
    """
    print("Logging in")
    facebook = FacebookLogIn()
    facebook.login_no_verification()


@app.command()
def scrape(name: Optional[str] = None):
    try:
        print(f"Start scraping friend list for {name}")
        scraper = AccountScraper(name)
        scraper.pipeline()
    except Exception as e:
        print(e)


@app.command()
def scrape_friend_list(name: Optional[str] = None):
    try:
        typer.echo(f"Start scraping friend list for {name}")
        scraper = FriendListScraper(name)
        scraper.pipeline()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app()
