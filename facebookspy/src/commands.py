import subprocess
import threading
from time import time
from typing import Annotated

import inquirer
import typer
from dotenv import load_dotenv
from rich import print as rprint
from src.cli.version import return_version_info

from .facebook.account.account_basic import AccountBasic
from .facebook.account.account_events import AccountEvents
from .facebook.account.account_friend import AccountFriend
from .facebook.account.account_group import AccountGroup
from .facebook.account.account_image import AccountImage
from .facebook.account.account_like import AccountLike
from .facebook.account.account_post import AccountPost
from .facebook.account.account_recentplace import AccountRecentPlaces
from .facebook.account.account_reel import AccountReel
from .facebook.account.account_review import AccountReview
from .facebook.account.account_videos import AccountVideo
from .facebook.downloader import Downloader
from .facebook.login import FacebookLogIn
from .facebook.post_detail import PostDetail
from .logs import Logs
from .runfastapi import run_fastapi
from .runreact import run_react
from .graph import create_relationship_graph

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
        # thread_react = threading.Thread(target=run_react)
        thread_fastapi = threading.Thread(target=run_fastapi)

        # thread_react.start()
        thread_fastapi.start()

        # thread_react.join()
        thread_fastapi.join()


@app.command()
def graph():
    """Create a graph of connections between Person objects based on their Friends"""

    create_relationship_graph()


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


def prompt_account_options():
    questions = [
        inquirer.Checkbox(
            "options",
            message="Select what you want to scrape",
            choices=[
                ("Scrape work and education history data", "a"),
                ("Scrape email and phone number", "b"),
                ("Scrape visited places", "c"),
                ("Scrape family member data", "d"),
                ("Scrape full name from facebook account", "e"),
            ],
        )
    ]
    answers = inquirer.prompt(questions)
    return answers["options"]


@app.command()
def scrape_basic_data(name: Annotated[str, typer.Argument(help="Facebook user id")]):
    """Command to scrape work and education history, contact data, visited places, family member and full name"""
    selected_options = prompt_account_options()

    if "a" in selected_options:
        rprint(f"Start scraping work and education data from {name} account")
        scraper = AccountBasic(name)

        time_start = time()
        scraper.work_and_education_pipeline()
        time_end = time()

        if scraper.is_pipeline_successful:
            rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
        else:
            rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")

    if "b" in selected_options:
        rprint(f"Start scraping personal data from {name} account")
        scraper = AccountBasic(name)

        time_start = time()
        scraper.contact_pipeline()
        time_end = time()

        if scraper.is_pipeline_successful:
            rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
        else:
            rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")

    if "c" in selected_options:
        rprint(f"Start scraping localization data from {name} account")
        scraper = AccountBasic(name)

        time_start = time()
        scraper.localization_pipeline()
        time_end = time()

        if scraper.is_pipeline_successful:
            rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
        else:
            rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")

    if "d" in selected_options:
        rprint(f"Start scraping family member data from {name} account")
        scraper = AccountBasic(name)

        time_start = time()
        scraper.family_member_pipeline()
        time_end = time()

        if scraper.is_pipeline_successful:
            rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
        else:
            rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")

    if "e" in selected_options:
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


def download_person_videos_options():
    questions = [
        inquirer.Checkbox(
            "options",
            message="Select options",
            choices=[
                (
                    "Download all videos for specified facebook account based on the scraped URLs",
                    "a",
                ),
                (
                    "Download all videos with 'downloaded' field with value False for specified facebook account based on the scraped URLs",
                    "b",
                ),
            ],
        )
    ]
    answers = inquirer.prompt(questions)
    return answers["options"]


@app.command()
def download_person_videos(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
):
    """Download videos for specified facebook account"""
    selected_options = download_person_videos_options()

    if "a" in selected_options:
        rprint(f"Start downloading all videos for {name}")
        scraper = Downloader(name)

        time_start = time()
        scraper.download_all_person_videos_pipeline()
        time_end = time()

        if scraper.is_pipeline_successful:
            rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
        else:
            rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")

    if "b" in selected_options:
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
            message="Select options",
            choices=[
                (
                    "Scrape basic information like full name, history of employement and school, localization etc.",
                    "a",
                ),
                ("Scrape a list of user's friends", "b"),
                ("Scrape and download images", "c"),
                ("Scrape url for user's reels", "d"),
                ("Scrape user's reviews", "e"),
                ("Scrape user's videos urls", "f"),
                ("Download videos based on scraped urls", "g"),
                ("Scrape urls for user's posts", "h"),
                ("Scrape post details based on scraped urls", "i"),
                ("Scrape all user's likes", "j"),
                ("Scrape all user's groups", "k"),
                ("Scrape all user's events", "l"),
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
    if "a" in selected_options:
        basic_scraper = AccountBasic(name)
        basic_scraper.pipeline()

    if "b" in selected_options:
        friends_scraper = AccountFriend(name)
        friends_scraper.pipeline()

    if "c" in selected_options:
        images_scraper = AccountImage(name)
        images_scraper.pipeline()

    if "d" in selected_options:
        reels_scraper = AccountReel(name)
        reels_scraper.pipeline()

    if "e" in selected_options:
        reviews_scraper = AccountReel(name)
        reviews_scraper.pipeline()

    if "f" in selected_options:
        videos_scraper = AccountVideo(name)
        videos_scraper.save_video_urls_to_database_pipeline()

    if "g" in selected_options:
        video_downloader = Downloader(name)
        video_downloader.download_all_person_videos_pipeline()

    if "h" in selected_options:
        posts_scraper = AccountPost(name)
        posts_scraper.pipeline()

    if "i" in selected_options:
        post_detail_scraper = PostDetail(name)
        post_detail_scraper.pipeline()

    if "j" in selected_options:
        likes_scraper = AccountLike(name)
        likes_scraper.pipeline()

    if "k" in selected_options:
        groups_scraper = AccountGroup(name)
        groups_scraper.pipeline()

    if "l" in selected_options:
        events_scraper = AccountEvents(name)
        events_scraper.pipeline()


if __name__ == "__main__":
    app()
