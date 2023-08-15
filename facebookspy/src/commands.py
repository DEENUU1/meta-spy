from dotenv import load_dotenv
from .facebook.login import FacebookLogIn
from .facebook.account.account_basic import AccountBasic
from .facebook.account.account_friend import AccountFriend
from .facebook.account.account_recentplace import AccountRecentPlaces
from .facebook.account.account_image import AccountImage
from .facebook.account.account_reel import AccountReel
from .facebook.account.account_videos import AccountVideo
from .facebook.account.account_review import AccountReview
from .facebook.downloader import Downloader
from .facebook.account.account_post import AccountPost
from .facebook.post_detail import PostDetail
from typing import Optional
import typer
from src.cli.home import display_start_menu
from src.cli.version import return_version_info
import subprocess
from .logs import Logs
from rich import print as rprint
from .server.backend.app import app as fastapi_app

logs = Logs()

load_dotenv()
app = typer.Typer()


""" Fastapi """


def server():
    """Run local server to browse scraped data"""
    try:
        build_command = ["docker-compose", "build"]
        subprocess.run(build_command, check=True)

        run_command = ["docker-compose", "up", "-d"]
        subprocess.run(run_command, check=True)

    except subprocess.CalledProcessError as e:
        logs.log_error(f"An error occurred while starting local server {e}")
        rprint(f"An error occurred {e}")


def server_backend():
    """Run only backend (fastapi) local app"""
    import uvicorn

    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)


""" Project commands """


def home():
    """Display basic information about the project"""

    display_start_menu()


def version():
    """Display data about the project version"""

    return_version_info()


""" Log In commands """


def login_2_step():
    """Log in to facebook account with 2-step authentication"""

    facebook = FacebookLogIn()
    facebook.login_2_step_pipeline()

    if facebook.is_pipeline_successful:
        rprint("✅Logging successful✅")
    else:
        rprint("❌Logging failed❌")


def login():
    """Log in to facebook account without 2-step authentication"""

    facebook = FacebookLogIn()
    facebook.login_no_verification_pipeline()

    if facebook.is_pipeline_successful:
        rprint("✅Logging successful✅")
    else:
        rprint("❌Logging failed❌")


""" Account basic data commands """


def scrape_full_account(name: Optional[str] = None):
    """Scrape data from facebook account:
    - full name
    - places
    - family members
    - work and education
    """

    rprint(f"Start scraping all data from {name} account")
    scraper = AccountBasic(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


def scrape_work_and_education(name: Optional[str] = None):
    """Scrape work and education history data"""

    rprint(f"Start scraping work and education data from {name} account")
    scraper = AccountBasic(name)
    scraper.work_and_education_pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


def scrape_localization(name: Optional[str] = None):
    """Scrape visited places"""

    rprint(f"Start scraping localization data from {name} account")
    scraper = AccountBasic(name)
    scraper.localization_pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


def scrape_family_member(name: Optional[str] = None):
    """Scrape family member data"""

    rprint(f"Start scraping family member data from {name} account")
    scraper = AccountBasic(name)
    scraper.family_member_pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


def scrape_full_name(name: Optional[str] = None):
    """Scrape full name from facebook account"""

    rprint(f"Start scraping full name data from {name} account")
    scraper = AccountBasic(name)
    scraper.full_name_pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


""" Friend list commands """


def scrape_friend_list(name: Optional[str] = None):
    """Scrape friend list from facebook account"""

    rprint(f"Start scraping friend list for {name}")
    scraper = AccountFriend(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


""" Image scraper commands """


def scrape_images(name: Optional[str] = None):
    """Scrape images from facebook account"""

    rprint(f"Start scraping images for {name}")
    scraper = AccountImage(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


""" Recent place scraper commands """


def scrape_recent_places(name: Optional[str] = None):
    """Scrape recent places from facebook account"""

    rprint(f"Start scraping recent places for {name}")
    scraper = AccountRecentPlaces(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


""" Reels scraper commands """


def scrape_reels(name: Optional[str] = None):
    """Scrape reels urls from facebook account"""

    rprint(f"Start scraping reels for {name}")
    scraper = AccountReel(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


""" Reviews scraper commands """


def scrape_reviews(name: Optional[str] = None):
    """Scrape written reviews from facebook account"""

    rprint(f"Start scraping reviews for {name}")
    scraper = AccountReview(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


""" Videos scraper commands """


def scrape_videos_urls(name: Optional[str] = None):
    """Scrape videos urls from facebook account"""

    rprint(f"Start scraping videos urls for {name}")
    scraper = AccountVideo(name)
    scraper.save_video_urls_to_database_pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


""" Downloader commands """


def download_all_person_videos(name: Optional[str] = None):
    """Download all reels for specified facebook account based on the scraped URLs"""

    rprint(f"Start downloading all videos for {name}")
    scraper = Downloader(name)
    scraper.download_all_person_videos_pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


def download_new_person_videos(name: Optional[str] = None):
    """Download all videos with 'downloaded' field with value False for specified
    facebook account based on the scraped URLs"""

    rprint(f"Start downloading all new videos for {name}")
    scraper = Downloader(name)
    scraper.download_new_person_videos_pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


def download_video(url: Optional[str] = None):
    """Download single video"""

    rprint(f"Start downloading video")
    scraper = Downloader()
    scraper.download_single_video_pipeline(url)

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


""" Posts """


def scrape_posts(name: Optional[str] = None):
    """Scrape urls for posts from facebook account"""

    rprint(f"Start scraping posts for {name}")
    scraper = AccountPost(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")


def scrape_post_details(name: Optional[str] = None):
    """Scrape detail of user's posts"""

    rprint(f"Start scraping posts detail for {name}")
    scraper = PostDetail(name)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        rprint("✅Scraping successful✅")
    else:
        rprint("❌Scraping failed❌")
