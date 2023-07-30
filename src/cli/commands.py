from dotenv import load_dotenv
from facebook.login import FacebookLogIn
from facebook.account import AccountScraper
from facebook.friends import FriendListScraper
from facebook.place_recent import FacebookRecentPlaces
from facebook.image import FacebookImageScraper
from facebook.reels import FacebookReelsScraper
from facebook.videos import FacebookVideoScraper
from facebook.reviews import FacebookReviewsScraper
from typing import Optional
import typer
from .home import display_start_menu
from rich import print
from .version import return_version_info

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


def scrape_reels(name: Optional[str] = None):
    print(f"Start scraping reels for {name}")
    scraper = FacebookReelsScraper(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        print("✅Scraping successful✅")
    else:
        print("❌Scraping failed❌")


def scrape_videos(name: Optional[str] = None):
    print(f"Start scraping reels for {name}")
    scraper = FacebookVideoScraper(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        print("✅Scraping successful✅")
    else:
        print("❌Scraping failed❌")


def scrape_recent_places(name: Optional[str] = None):
    print(f"Start scraping recent places for {name}")
    scraper = FacebookRecentPlaces(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        print("✅Scraping successful✅")
    else:
        print("❌Scraping failed❌")


def scrape_reviews(name: Optional[str] = None):
    print(f"Start scraping reviews for {name}")
    scraper = FacebookReviewsScraper(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        print("✅Scraping successful✅")
    else:
        print("❌Scraping failed❌")
