import subprocess
from time import time
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
from .facebook.post_detail import pipeline
from .logs import Logs
from .analytics.graph import create_relationship_graph
from .repository import crawlerqueue_repository
from .scripts.urlid import get_account_id
from .facebook.search import search_post, search as search_scraper
from .instagram.instagram_profile import ProfileScraper
from .utils.check_instagram_sessionid import check_instagram_sessionid
from typing_extensions import Annotated

load_dotenv()
logs = Logs()
app = typer.Typer(
    # Default Error message without Rich effect
    pretty_exceptions_enable=False,
)


@app.command()
def version() -> None:
    """Display data about the project version"""
    return_version_info()


""" Server """


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


""" Crawler """


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


""" Analytics """


@app.command()
def graph() -> None:
    """Create a graph of connections between Person objects based on their Friends"""
    create_relationship_graph()


""" Facebook Login """


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


""" Video downloader """


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


""" Facebook Accounts & Pages """


@app.command()
def post_details(url: Annotated[str, typer.Argument(help="Facebook post url")]) -> None:
    """Scrape detail of specified post"""

    rprint(f"Start scraping posts details")

    time_start = time()

    scraper_pipeline = pipeline(post_url=url)
    print(scraper_pipeline)

    time_end = time()

    rprint(f"Scraping finished after {time_end - time_start} seconds")


@app.command()
def fb_account(
    id: Annotated[str, typer.Argument(help="Facebook account id")],
    work: Annotated[
        bool,
        typer.Option(
            help="Scrape work and education information from the given facebook account"
        ),
    ] = False,
    contact: Annotated[
        bool, typer.Option(help="Scrape contact data from the given facebook account")
    ] = False,
    location: Annotated[
        bool, typer.Option(help="Scrape location data from the given facebook account")
    ] = False,
    family: Annotated[
        bool,
        typer.Option(help="Scrape family members data from the given facebook account"),
    ] = False,
    name: Annotated[
        bool, typer.Option(help="Scrape full name from the given facebook account")
    ] = False,
    friends: Annotated[
        bool, typer.Option(help="Scrape friends list from the given facebook account")
    ] = False,
    images: Annotated[
        bool, typer.Option(help="Scrape images from the given facebook account")
    ] = False,
    recent: Annotated[
        bool, typer.Option(help="Scrape recent places from the given facebook account")
    ] = False,
    reels: Annotated[
        bool, typer.Option(help="Scrape urls for reels from the given facebook account")
    ] = False,
    reviews: Annotated[
        bool, typer.Option(help="Scrape reviews from the given facebook account")
    ] = False,
    videos: Annotated[
        bool,
        typer.Option(help="Scrape urls for videos from the given facebook account"),
    ] = False,
    da: Annotated[
        bool, typer.Option(help="Download all videos from the given facebook account")
    ] = False,
    dn: Annotated[
        bool,
        typer.Option(help="Download only new videos from the given facebook account"),
    ] = False,
    posts: Annotated[
        bool, typer.Option(help="Scrape all posts from the given facebook account")
    ] = False,
    details: Annotated[
        bool,
        typer.Option(help="Scrape details of posts from the given facebook account"),
    ] = False,
    likes: Annotated[
        bool, typer.Option(help="Scrape likes from the given facebook account")
    ] = False,
    groups: Annotated[
        bool, typer.Option(help="Scrape groups from the given facebook account")
    ] = False,
    events: Annotated[
        bool, typer.Option(help="Scrape events from the given facebook account")
    ] = False,
) -> None:
    time_start = time()

    if work:
        wae = AccountBasic(id)
        wae.work_and_education_pipeline()
    if contact:
        c = AccountBasic(id)
        c.contact_pipeline()
    if location:
        l = AccountBasic(id)
        l.localization_pipeline()
    if family:
        fm = AccountBasic(id)
        fm.family_member_pipeline()
    if name:
        fn = AccountBasic(id)
        fn.full_name_pipeline()
    if friends:
        friend_scraper = AccountFriend(id)
        friend_scraper.pipeline()
    if images:
        images_scraper = AccountImage(id)
        images_scraper.pipeline()
    if recent:
        recent_scraper = AccountRecentPlaces(id)
        recent_scraper.pipeline()
    if reels:
        reels_scraper = AccountReel(id)
        reels_scraper.pipeline()
    if reviews:
        reviews_scraper = AccountReview(id)
        reviews_scraper.pipeline()
    if videos:
        videos_scraper = AccountVideo(id)
        videos_scraper.save_video_urls_to_database_pipeline()
    if dn or da:
        downloader = Downloader(id)
        if da:
            downloader.download_all_person_videos_pipeline()
        if dn:
            downloader.download_new_person_videos_pipeline()
    if posts:
        posts_scraper = AccountPost(id)
        posts_scraper.pipeline()
    if details:
        pipeline(name=id)
    if likes:
        likes_scraper = AccountLike(id)
        likes_scraper.pipeline()
    if groups:
        groups_scraper = AccountGroup(id)
        groups_scraper.pipeline()
    if events:
        events_scraper = AccountEvents(id)
        events_scraper.pipeline()

    time_end = time()
    print(f"Scraping finished after {time_end - time_start} seconds")


""" Facebook search """


@app.command()
def fb_search(
    query: Annotated[str, typer.Argument(help="Facebook account id")],
    results: Annotated[int, typer.Argument(help="Number of results")],
    post: Annotated[
        bool, typer.Option(help="Search for posts based on given query")
    ] = False,
    people: Annotated[
        bool, typer.Option(help="Search for people based on given query")
    ] = False,
    group: Annotated[
        bool, typer.Option(help="Search for groups based on given query")
    ] = False,
    place: Annotated[
        bool, typer.Option(help="Search for places based on given query")
    ] = False,
    event: Annotated[
        bool, typer.Option(help="Search for events based on given query")
    ] = False,
    page: Annotated[
        bool, typer.Option(help="Search for pages based on given query")
    ] = False,
) -> None:
    time_start = time()

    if post:
        post_scraper = search_post.SearchPost(query, results)
        post_scraper.pipeline()
    if people:
        people_scraper = search_scraper.SearchPerson(query, results)
        people_scraper.pipeline()
    if group:
        group_scraper = search_scraper.SearchGroup(query, results)
        group_scraper.pipeline()
    if place:
        places_scraper = search_scraper.SearchPlaces(query, results)
        places_scraper.pipeline()
    if event:
        event_scraper = search_scraper.SearchEvents(query, results)
        event_scraper.pipeline()
    if page:
        page_scraper = search_scraper.SearchPage(query, results)
        page_scraper.pipeline()

    time_end = time()
    print(f"Scraping finished after {time_end - time_start} seconds")


""" Instagram """


@app.command()
def insta_account(
    id: Annotated[str, typer.Argument(help="Facebook account id")],
    images: Annotated[
        bool, typer.Option(help="Scrape image urls from the given instagram account")
    ] = False,
    stats: Annotated[
        bool, typer.Option(help="Scrape stats from the given instagram account")
    ] = False,
) -> None:
    """Scrape instagram account"""

    time_start = time()

    session = check_instagram_sessionid()
    if not session:
        rprint(
            "Add sessionId to .env file. Check documentation for more details: "
            "https://deenuu1.github.io/meta-spy/installation/"
        )
        return
    else:
        if images:
            scraper = ProfileScraper(id)
            scraper.pipeline_images()

        if stats:
            scraper = ProfileScraper(id)
            scraper.pipeline_stats()

    time_end = time()
    rprint(f"Scraping finished after {time_end - time_start} seconds")


if __name__ == "__main__":
    app()
