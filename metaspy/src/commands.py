import subprocess
from time import time
from typing import Annotated
import concurrent
import inquirer
import typer
from dotenv import load_dotenv
from rich import print as rprint
from rich.prompt import Prompt

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
from .analytics.ai import get_person_summary
from .analytics.report import generate_pdf_report
from .repository import crawlerqueue_repository, post_repository, person_repository
from .scripts.urlid import get_account_id
from .analytics import classification
from typing import List
from .facebook.search import search_post, search as search_scraper
from .instagram.instagram_profile import ProfileScraper
from .instagram.instagram_login import InstagramLogIn

load_dotenv()
logs = Logs()
app = typer.Typer(
    pretty_exceptions_enable=False,  # Default Error message without Rich effect
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


""" Analitics """


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


""" Login """


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


""" Facebook Accounts & Pages """


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


def run_scraper(scraper_name, name):
    rprint(f"Start scraping {scraper_name} data from {name} account")
    scraper = AccountBasic(name)

    time_start = time()
    if scraper_name == "work_and_education":
        scraper.work_and_education_pipeline()
    elif scraper_name == "contact":
        scraper.contact_pipeline()
    elif scraper_name == "localization":
        scraper.localization_pipeline()
    elif scraper_name == "family_member":
        scraper.family_member_pipeline()
    elif scraper_name == "full_name":
        scraper.full_name_pipeline()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def scrape_basic_data(
    name: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
    """Command to scrape work and education history, contact data, visited places, family member and full name"""
    selected_options = prompt_account_options()

    scraper_names_mapping = {
        "a": "work_and_education",
        "b": "contact",
        "c": "localization",
        "d": "family_member",
        "e": "full_name",
    }

    selected_scrapers = [scraper_names_mapping[option] for option in selected_options]

    if not selected_scrapers:
        rprint("No scrapers selected. Exiting.")
        return

    # Create a thread pool to run the selected scrapers concurrently
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(selected_scrapers)
    ) as executor:
        futures = []

        for scraper_name in selected_scrapers:
            futures.append(executor.submit(run_scraper, scraper_name, name))

        # Wait for all futures to complete
        concurrent.futures.wait(futures)


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
        while True:
            user_decision = Prompt.ask(
                "Do you want to download videos❔ (Y/n)  (q - exit) "
            )
            if user_decision == "Y":
                rprint(f"Start downloading all videos for {name}")
                scraper = Downloader(name)

                time_start = time()
                scraper.download_all_person_videos_pipeline()
                time_end = time()

                if scraper.is_pipeline_successful:
                    rprint(
                        f"✅Scraping successful after {time_end - time_start} seconds ✅"
                    )
                else:
                    rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")

            elif user_decision == "n":
                rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
            elif user_decision == "q":
                break
            else:
                rprint("Invalid input")

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
    rprint(scraper_pipeline)

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

    selected_options = prompt_options()

    def run_scraper(name, option):
        if option == "a":
            basic_scraper = AccountBasic(name)
            basic_scraper.pipeline()
        elif option == "b":
            friends_scraper = AccountFriend(name)
            friends_scraper.pipeline()
        elif option == "c":
            images_scraper = AccountImage(name)
            images_scraper.pipeline()
        elif option == "d":
            reels_scraper = AccountReel(name)
            reels_scraper.pipeline()
        elif option == "e":
            reviews_scraper = AccountReel(name)
            reviews_scraper.pipeline()
        elif option == "f":
            videos_scraper = AccountVideo(name)
            videos_scraper.save_video_urls_to_database_pipeline()
        elif option == "g":
            video_downloader = Downloader(name)
            video_downloader.download_all_person_videos_pipeline()
        elif option == "h":
            posts_scraper = AccountPost(name)
            posts_scraper.pipeline()
        elif option == "i":
            scraper_pipeline = pipeline(name=name)
            rprint(scraper_pipeline)
        elif option == "j":
            likes_scraper = AccountLike(name)
            likes_scraper.pipeline()
        elif option == "k":
            groups_scraper = AccountGroup(name)
            groups_scraper.pipeline()
        elif option == "l":
            events_scraper = AccountEvents(name)
            events_scraper.pipeline()

    if len(names) == 1:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=len(selected_options)
        ) as executor:
            for option in selected_options:
                executor.submit(run_scraper, names[0], option)
    else:
        # If multiple users are specified, run their scrapers concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(names)) as executor:
            for name in names:
                for option in selected_options:
                    executor.submit(run_scraper, name, option)


def prompt_search_options() -> List[str]:
    questions = [
        inquirer.Checkbox(
            "options",
            message="Select search options",
            choices=[
                ("Search for posts", "a"),
                ("Search for people", "b"),
                ("Search for groups", "c"),
                ("Search for places", "d"),
                ("Search for events", "e"),
                ("Search for pages", "f"),
            ],
        )
    ]
    answers = inquirer.prompt(questions)
    return answers["options"]


@app.command()
def search(
    query: Annotated[str, typer.Argument(help="Query search")],
    max_result: Annotated[int, typer.Argument(help="The number of results")],
) -> None:
    """Command to search and scraper for posts, person, pages, events, groups and places"""
    selected_options = prompt_search_options()

    def run_scraper(name, query: str, max_result: int):
        if name == "a":
            post_scraper = search_post.SearchPost(query, max_result)
            post_scraper.pipeline()
        elif name == "b":
            person_scraper = search_scraper.SearchPerson(query, max_result)
            person_scraper.pipeline()
        elif name == "c":
            group_scraper = search_scraper.SearchGroup(query, max_result)
            group_scraper.pipeline()
        elif name == "d":
            places_scraper = search_scraper.SearchPlaces(query, max_result)
            places_scraper.pipeline()
        elif name == "e":
            event_scraper = search_scraper.SearchEvents(query, max_result)
            event_scraper.pipeline()
        elif name == "f":
            page_scraper = search_scraper.SearchPage(query, max_result)
            page_scraper.pipeline()

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(selected_options)
    ) as executor:
        for option in selected_options:
            executor.submit(run_scraper, option, query, max_result)


@app.command()
def instagram_profile_images(
    name: Annotated[str, typer.Argument(help="Instagram user id")]
) -> None:
    """Scrape images from instagram profile"""

    rprint(f"Start scraping images for {name}")
    scraper = ProfileScraper(name)

    time_start = time()
    scraper.pipeline_images()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Scraping successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Scraping failed after {time_end - time_start} seconds ❌")


@app.command()
def instagram_login_fb() -> None:
    """Log in to instagram account using facebook auth"""

    rprint(f"Start logging in to instagram account")
    scraper = InstagramLogIn()

    time_start = time()
    scraper.login_with_facebook()
    time_end = time()

    if scraper.is_pipeline_successful:
        rprint(f"✅Login successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Login failed after {time_end - time_start} seconds ❌")


if __name__ == "__main__":
    app()
