from dotenv import load_dotenv
from login import FacebookLogIn
from account import AccountScraper, FriendListScraper, FacebookImageScraper
from typing import Optional
import typer
from home import display_start_menu
from rich import print
from version import return_version_info

load_dotenv()
app = typer.Typer()


def home():
    display_start_menu()


def version():
    return_version_info()


def login_2_step():
    """
    Log in to facebook account with 2-step authentication
    """
    facebook = FacebookLogIn()
    facebook.login_2_step_pipeline()

    if facebook.is_pipeline_successful:
        print("✅Logging successful✅")
    else:
        print("❌Logging failed❌")


def login():
    """
    Log in to facebook account without 2-step authentication
    """
    facebook = FacebookLogIn()
    facebook.login_no_verification_pipeline()

    if facebook.is_pipeline_successful:
        print("✅Logging successful✅")
    else:
        print("❌Logging failed❌")


def scrape(name: Optional[str] = None):
    print(f"Start scraping friend list for {name}")
    scraper = AccountScraper(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        print("✅Scraping successful✅")
    else:
        print("❌Scraping failed❌")


def scrape_friend_list(name: Optional[str] = None):
    typer.echo(f"Start scraping friend list for {name}")
    scraper = FriendListScraper(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        print("✅Scraping successful✅")
    else:
        print("❌Scraping failed❌")


def scrape_images(name: Optional[str] = None):
    print(f"Start scraping images for {name}")
    scraper = FacebookImageScraper(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        print("✅Scraping successful✅")
    else:
        print("❌Scraping failed❌")
