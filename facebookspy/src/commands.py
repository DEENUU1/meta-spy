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
from .facebook.account.account_like import AccountLike
from .facebook.account.account_group import AccountGroup
from .facebook.account.account_events import AccountEvents
from typing import Annotated
import typer
from src.cli.home import display_start_menu
from src.cli.version import return_version_info
import subprocess
from .logs import Logs
from rich import print as rprint
from time import time
import threading
from .runfastapi import run_fastapi
from .runreact import run_react
import inquirer


load_dotenv()

logs = Logs()

app = typer.Typer(
    pretty_exceptions_enable=False,  # Default Error message without Rich effect
)


@app.command()
def server(
    d: Annotated[
        bool, typer.Option(help="Run local server using Docker or with standard way")
    ] = False
):
    """Run local server to browse scraped data"""

    # Run local server using Docker
    if d:
        try:
            build_command = ["docker-compose", "build"]
            subprocess.run(build_command, check=True)

            run_command = ["docker-compose", "up", "-d"]
            subprocess.run(run_command, check=True)

        except subprocess.CalledProcessError as e:
            logs.log_error(f"An error occurred while starting local server {e}")
            rprint(f"An error occurred {e}")

    # Run local server without Docker
    else:
        thread_react = threading.Thread(target=run_react)
        thread_fastapi = threading.Thread(target=run_fastapi)

        thread_react.start()
        thread_fastapi.start()

        thread_react.join()
        thread_fastapi.join()


@app.command()
def home():
    """Display basic information about the project"""

    display_start_menu()


@app.command()
def version():
    """Display data about the project version"""

    return_version_info()


@app.command()
def login_2_step():
    """Log in to facebook account with 2-step authentication"""

    facebook = FacebookLogIn()

    time_start = time()
    facebook.login_2_step_pipeline()
    time_end = time()

    if facebook.is_pipeline_successful:
        rprint(f"✅Logging successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Logging failed after {time_end - time_start} seconds ❌")


@app.command()
def login():
    """Log in to facebook account without 2-step authentication"""

    facebook = FacebookLogIn()

    time_start = time()
    facebook.login_no_verification_pipeline()
    time_end = time()

    if facebook.is_pipeline_successful:
        rprint(f"✅Logging successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Logging failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_full_account(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape data from facebook account:
    - full name
    - places
    - family members
    - work and education
    """

    rprint(f"Start scraping all data from {name} account")
    scraper = AccountBasic(name)

    time_start = time()
    scraper.pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_work_education(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
):
    """Scrape work and education history data"""

    rprint(f"Start scraping work and education data from {name} account")
    scraper = AccountBasic(name)

    time_start = time()
    scraper.work_and_education_pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_localization(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape visited places"""

    rprint(f"Start scraping localization data from {name} account")
    scraper = AccountBasic(name)

    time_start = time()
    scraper.localization_pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_family_member(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape family member data"""

    rprint(f"Start scraping family member data from {name} account")
    scraper = AccountBasic(name)

    time_start = time()
    scraper.family_member_pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_full_name(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape full name from facebook account"""

    rprint(f"Start scraping full name data from {name} account")
    scraper = AccountBasic(name)

    time_start = time()
    scraper.full_name_pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_friend_list(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape friend list from facebook account"""

    rprint(f"Start scraping friend list for {name}")
    scraper = AccountFriend(name)

    time_start = time()
    scraper.pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_images(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape images from facebook account"""

    rprint(f"Start scraping images for {name}")
    scraper = AccountImage(name)

    time_start = time()
    scraper.pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_recent_places(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape recent places from facebook account"""

    rprint(f"Start scraping recent places for {name}")
    scraper = AccountRecentPlaces(name)

    time_start = time()
    scraper.pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_reels(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape reels urls from facebook account"""

    rprint(f"Start scraping reels for {name}")
    scraper = AccountReel(name)

    time_start = time()
    scraper.pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_reviews(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape written reviews from facebook account"""

    rprint(f"Start scraping reviews for {name}")
    scraper = AccountReview(name)

    time_start = time()
    scraper.pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_video_urls(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape video urls from facebook account"""

    rprint(f"Start scraping videos urls for {name}")
    scraper = AccountVideo(name)

    time_start = time()
    scraper.save_video_urls_to_database_pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def download_all_person_videos(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
):
    """Download all reels for specified facebook account based on the scraped URLs"""

    rprint(f"Start downloading all videos for {name}")
    scraper = Downloader(name)

    time_start = time()
    scraper.download_all_person_videos_pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def download_new_person_videos(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
):
    """Download all videos with 'downloaded' field with value False for specified
    facebook account based on the scraped URLs"""

    rprint(f"Start downloading all new videos for {name}")
    scraper = Downloader(name)

    time_start = time()
    scraper.download_new_person_videos_pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def download_video(url: Annotated[str, typer.Argument(help="Facebook video url")]):
    """Download single video"""

    rprint(f"Start downloading video")
    scraper = Downloader()

    time_start = time()
    scraper.download_single_video_pipeline(url)
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_person_posts(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape urls for posts from facebook account"""

    rprint(f"Start scraping posts for {name}")
    scraper = AccountPost(name)

    time_start = time()
    scraper.pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_person_post_details(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
):
    """Scrape detail of user's posts"""

    rprint(f"Start scraping posts detail for {name}")
    scraper = PostDetail(name)

    time_start = time()
    scraper.pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_person_likes(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape user's likes"""

    rprint(f"Start scraping likes for {name}")
    scraper = AccountLike(name)

    time_start = time()
    scraper.pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_person_groups(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape user's groups"""

    rprint(f"Start scraping groups for {name}")
    scraper = AccountGroup(name)

    time_start = time()
    scraper.pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_person_events(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Scrape user's events"""

    rprint(f"Start scraping events for {name}")
    scraper = AccountEvents(name)

    time_start = time()
    scraper.pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


def prompt_options():
    questions = [
        inquirer.Checkbox(
            "options",
            message="Select options:",
            choices=[
                "basic",
                "friends",
                "images",
                "reels",
                "reviews",
                "videos",
                "download videos",
                "posts",
                "post details",
                "likes",
                "groups",
                "events",
            ],
        )
    ]
    answers = inquirer.prompt(questions)
    return answers["options"]


@app.command()
def full_scrape(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Full scrape of user's data
    - basic information (job and school history, full name etc)
    - friends
    - images (download)
    - recent places
    - reels
    - reviews
    - videos (download)
    - posts (urls and details)
    - likes
    - groups
    - events
    """

    selected_options = prompt_options()

    if "basic" in selected_options:
        basic_scraper = AccountBasic(name)
        basic_scraper.pipeline()

    if "friends" in selected_options:
        friends_scraper = AccountFriend(name)
        friends_scraper.pipeline()

    if "images" in selected_options:
        images_scraper = AccountImage(name)
        images_scraper.pipeline()

    if "reels" in selected_options:
        reels_scraper = AccountReel(name)
        reels_scraper.pipeline()

    if "reviews" in selected_options:
        reviews_scraper = AccountReel(name)
        reviews_scraper.pipeline()

    if "videos" in selected_options:
        videos_scraper = AccountVideo(name)
        videos_scraper.save_video_urls_to_database_pipeline()

    if "download videos" in selected_options:
        video_downloader = Downloader(name)
        video_downloader.download_all_person_videos_pipeline()

    if "posts" in selected_options:
        posts_scraper = AccountPost(name)
        posts_scraper.pipeline()

    if "post details" in selected_options:
        post_detail_scraper = PostDetail(name)
        post_detail_scraper.pipeline()

    if "likes" in selected_options:
        likes_scraper = AccountLike(name)
        likes_scraper.pipeline()

    if "groups" in selected_options:
        groups_scraper = AccountGroup(name)
        groups_scraper.pipeline()

    if "events" in selected_options:
        events_scraper = AccountEvents(name)
        events_scraper.pipeline()


if __name__ == "__main__":
    app()
