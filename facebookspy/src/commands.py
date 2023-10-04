import subprocess
from time import time
from typing import Annotated

import inquirer
import typer
from dotenv import load_dotenv
from rich import print as rprint
from .cli.version import return_version_info

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
from .facebook.post_detail import PostDetail, pipeline
from .logs import Logs
from .analytics.graph import create_relationship_graph
from .analytics.ai import get_person_summary
from .analytics.report import generate_pdf_report
from .repository import crawlerqueue_repository, post_repository, person_repository
from .scripts.urlid import get_account_id
from .analytics import classification
from typing import List


load_dotenv()

logs = Logs()

app = typer.Typer(
    pretty_exceptions_enable=False,  # Default Error message without Rich effect
)


@app.command()
def server() -> None:
    import uvicorn
    from .server.app import app

    """Run local server using docker to browse scraped data"""

    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except subprocess.CalledProcessError as e:
        logs.log_error(f"An error occurred while starting local server {e}")
        rprint(f"An error occurred {e}")


@app.command()
def friend_crawler(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
    # At first the function is scraping a list of friends for specified user
    # Create Person and Friend objects just like in a standard friend scraper
    # But also it create CrawlerQueue objects with url to friend facebook accounts

    rprint(f"Start crawler from {name}")

    scraper = AccountFriend(name, crawler=True)
    scraper.pipeline()

    if scraper.is_pipeline_successful:
        # Return a list of users from queue with status False
        # Which means this user wasn't scraped yet
        users = crawlerqueue_repository.get_crawler_queues_status_false()
        while len(users) > 0:
            for user in users:
                user_id = get_account_id(user.url)
                scraper = AccountFriend(user_id, crawler=True)
                scraper.pipeline()

                if scraper.is_pipeline_successful:
                    crawlerqueue_repository.delete_crawler_queue(user.id)

    else:
        rprint(f"❌Failed to scrape friends from the main user❌")


@app.command()
def display_queue() -> None:
    """
    Display queue objects
    """

    queue_data = crawlerqueue_repository.get_crawler_queues_status_false()
    if len(queue_data) == 0:
        rprint("[bold] Queue is empty. [/bold]")
    else:
        rprint(
            f"[bold] Found {len(queue_data)} queue objects with status False: [/bold]"
        )
        for queue in queue_data:
            rprint(f"- [bold] ID: {queue.id} [/bold] {queue.url}")


@app.command()
def delete_queue_object(
    id: Annotated[int, typer.Argument(help="CrawlerQueue id")]
) -> None:
    """
    Delete a specified queue object based on id from db
    """

    if crawlerqueue_repository.delete_crawler_queue(id):
        rprint("✅ Queue object deleted ✅")
    else:
        rprint("❌Failed to delete Queue object from database. Please try again.❌")


@app.command()
def clear_queue() -> None:
    """
    Clear the queue of crawler
    """
    delete = crawlerqueue_repository.delete_all()
    if delete:
        rprint("✅ Queue cleared ✅")
    else:
        rprint("❌Queue not cleared, please try again❌")


@app.command()
def graph() -> None:
    """Create a graph of connections between Person objects based on their Friends"""
    create_relationship_graph()


@app.command()
def summary(name: Annotated[str, typer.Argument(help="Facebook user id")]) -> None:
    """Create a summary of a specified person by using AI and scraped data"""
    get_person_summary(name)


@app.command()
def report(name: Annotated[str, typer.Argument(help="Facebook user id")]) -> None:
    """
    Generate and save PDF file with scraped data for specified person.
    """
    generate_pdf_report(name)


@app.command()
def version() -> None:
    """Display data about the project version"""
    return_version_info()


@app.command()
def posts(
    display_all: Annotated[
        bool, typer.Option(help="Display all posts from the database")
    ] = False,
    id: Annotated[
        int, typer.Option(help="Display a specified post from the database")
    ] = None,
    person_id: Annotated[
        str, typer.Option(help="Display posts for a specified person from the database")
    ] = None,
) -> None:
    """Print a list of all posts in database, all post for specified user or specified post"""

    if display_all:
        posts = post_repository.get_all_posts()
        if len(posts) == 0:
            rprint("[bold]No posts found[/bold]")
        else:
            rprint(f"[bold]Found {len(posts)} posts[/bold]")

            for post in posts:
                rprint(
                    f"""ID: {post.id} Person ID: {post.person_id} Content: {post.content} Source: {post.source} 
                    Classification: {post.classification} Score: {post.score} Is scraped: {post.scraped} 
                    Number of likes/shares/comments: {post.number_of_likes} {post.number_of_shares} 
                    {post.number_of_comments}
                    """
                )

    if id:
        post = post_repository.get_post(id)
        if post is None:
            rprint("[bold]Post not found[/bold]")
        else:
            rprint(
                f"""ID: {post.id} Person ID: {post.person_id} Content: {post.content} Source: {post.source} 
                Classification: {post.classification} Score: {post.score} Is scraped: {post.scraped} 
                Number of likes/shares/comments: {post.number_of_likes} {post.number_of_shares} 
                {post.number_of_comments}"""
            )

    if person_id:
        person_object = person_repository.get_person(person_id)
        posts = post_repository.get_posts(person_object.id)
        if len(posts) == 0:
            rprint("[bold]No posts found[/bold]")
        else:
            rprint(f"[bold]Found {len(posts)} posts[/bold]")

            for post in posts:
                rprint(
                    f"""ID: {post.id} Person ID: {post.person_id} Content: {post.content} 
                    Source: {post.source} Classification: {post.classification} Score: {post.score} 
                    Is scraped: {post.scraped} Number of likes/shares/comments: {post.number_of_likes} 
                    {post.number_of_shares} {post.number_of_comments}"""
                )


@app.command()
def post_classifier(
    all_posts: Annotated[
        bool,
        typer.Option(help="Run post classification for all posts from the database"),
    ] = False,
    id: Annotated[
        int,
        typer.Option(
            help="Run post classification for specified post from the database"
        ),
    ] = None,
    person_id: Annotated[
        str,
        typer.Option(
            help="Run post classification for a specified person from the database"
        ),
    ] = None,
) -> None:
    """Run post classification for all posts from the database, all posts for specified user or specified post"""

    if all_posts:
        posts = post_repository.get_all_posts()
        if len(posts) == 0:
            rprint("[bold]No posts found[/bold]")
        else:
            rprint(f"[bold]Found {len(posts)} posts[/bold]")

            for post in posts:
                if post.content != "":
                    status, score = classification.text_classifier(post.content)
                    post_repository.update_classification(post.id, status, score)
                else:
                    rprint(f"[bold]Post {post.id} has no content[/bold]")
    if id:
        post = post_repository.get_post(id)
        if post is None:
            rprint("[bold]Post not found[/bold]")
        else:
            if post.content != "":
                status, score = classification.text_classifier(post.content)
                post_repository.update_classification(post.id, status, score)
            else:
                rprint(f"[bold]Post {post.id} has no content[/bold]")

    if person_id:
        person_object = person_repository.get_person(person_id)
        posts = post_repository.get_posts(person_object.id)
        if len(posts) == 0:
            rprint("[bold]No posts found[/bold]")
        else:
            rprint(f"[bold]Found {len(posts)} posts[/bold]")

            for post in posts:
                if post.content != "":
                    status, score = classification.text_classifier(post.content)
                    post_repository.update_classification(post.id, status, score)
                else:
                    rprint(f"[bold]Post {post.id} has no content[/bold]")


@app.command()
def login_2_step() -> None:
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
def login() -> None:
    """Log in to facebook account without 2-step authentication"""

    facebook = FacebookLogIn()

    time_start = time()
    facebook.login_no_verification_pipeline()
    time_end = time()

    if facebook.is_pipeline_successful:
        rprint(f"✅Logging successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Logging failed after {time_end - time_start} seconds ❌")


def prompt_account_options() -> List[str]:
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
def scrape_basic_data(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
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
def scrape_friend_list(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
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
def scrape_images(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
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
def scrape_recent_places(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
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
def scrape_reels(name: Annotated[str, typer.Argument(help="Facebook user id")]) -> None:
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
def scrape_reviews(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
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
def scrape_video_urls(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
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


def download_person_videos_options() -> List[str]:
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
                    "Download all videos with 'downloaded' field with value False for specified facebook account based "
                    "on the scraped URLs",
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
) -> None:
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
def download_video(
    url: Annotated[str, typer.Argument(help="Facebook video url")]
) -> None:
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
def scrape_person_posts(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
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
) -> None:
    """Scrape detail of user's posts"""

    rprint(f"Start scraping posts detail for {name}")

    time_start = time()

    scraper_pipeline = pipeline(name=name)
    print(scraper_pipeline)

    time_end = time()

    rprint(f"Scraping finished after {time_end - time_start} seconds")


@app.command()
def scrape_post_details(
    url: Annotated[str, typer.Argument(help="Facebook post url")]
) -> None:
    """Scrape detail of specified post"""

    rprint(f"Start scraping posts details")

    time_start = time()

    scraper_pipeline = pipeline(post_url=url)
    print(scraper_pipeline)

    time_end = time()

    rprint(f"Scraping finished after {time_end - time_start} seconds")


@app.command()
def scrape_person_likes(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
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
def scrape_person_groups(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
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
def scrape_person_events(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
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


def prompt_options() -> List[str]:
    questions = [
        inquirer.Checkbox(
            "options",
            message="Select options",
            choices=[
                (
                    "Scrape basic information like full name, history of employment and school, localization etc.",
                    "a",
                ),
                ("Scrape a list of user's friends", "b"),
                ("Scrape and download images", "c"),
                ("Scrape url for user's reels", "d"),
                ("Scrape user's reviews", "e"),
                ("Scrape user's videos urls", "f"),
                ("Download videos based on scraped urls", "g"),
                ("Scrape urls for user's posts", "h"),
                # ("Scrape post details based on scraped urls", "i"),
                ("Scrape all user's likes", "j"),
                ("Scrape all user's groups", "k"),
                ("Scrape all user's events", "l"),
            ],
        )
    ]
    answers = inquirer.prompt(questions)
    return answers["options"]


@app.command()
def full_scrape(
    names: Annotated[List[str], typer.Argument(help="Facebook user id")]
) -> None:
    """Full scrape of user's data
    - basic information (job and school history, full name etc.)
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
    rprint(f"Run scraper for {len(names)} users: {names}")

    for name in names:
        rprint(f"Scraping data for user: {name}")
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

        # if "i" in selected_options:
        #     post_detail_scraper = PostDetail(name)
        #     post_detail_scraper.pipeline()

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
