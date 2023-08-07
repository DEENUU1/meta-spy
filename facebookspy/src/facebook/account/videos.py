from time import sleep
from typing import List

from ...config import Config
from selenium.webdriver.common.by import By
from ..facebook_base import BaseFacebookScraper
from ...repository import create_person, get_person, person_exists, create_videos
import youtube_dl
from rich.progress import Progress
import os
import random
import string
from ...logs import Logs
from rich import print as rprint


logs = Logs("videos.py")


class FacebookVideoScraper(BaseFacebookScraper):
    """
    Scrape user's pictures
    """

    def __init__(self, user_id) -> None:
        super().__init__(user_id, base_url=f"https://www.facebook.com/{user_id}/videos")
        self.success = False

    def scroll_page(self) -> None:
        """
        Scrolls the page to load more friends from a list
        """
        try:
            last_height = self._driver.execute_script(
                "return document.body.scrollHeight"
            )
            consecutive_scrolls = 0

            while consecutive_scrolls < Config.MAX_CONSECUTIVE_SCROLLS:
                self._driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

                sleep(Config.SCROLL_PAUSE_TIME)
                new_height = self._driver.execute_script(
                    "return document.body.scrollHeight"
                )

                if new_height == last_height:
                    consecutive_scrolls += 1
                else:
                    consecutive_scrolls = 0

                last_height = new_height

        except Exception as e:
            logs.log_error(f"An Error occurred while scrolling: {e}")

    def extract_videos_urls(self) -> List[str]:
        """
        Return a list of all the image urls
        """
        extracted_videos_urls = []
        try:
            videos_elements = self._driver.find_elements(
                By.CSS_SELECTOR,
                "a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv",
            )
            for video_element in videos_elements:
                src_attribute = video_element.get_attribute("href")
                if src_attribute:
                    extracted_videos_urls.append(src_attribute)

        except Exception as e:
            logs.log_error(f"An Error extracting while extracting video URL: {e}")

        return extracted_videos_urls

    @staticmethod
    def generate_random_video_title() -> str:
        """Generate random video title"""
        chars = string.ascii_letters
        return "".join(random.choice(chars) for _ in range(12))

    def download_video(self, video_url: str):
        """Download videos using youtube_dl library"""

        video_path = Config.VIDEO_PATH
        if not os.path.exists(video_path):
            os.makedirs(video_path)

        user_video_path = os.path.dirname(f"{video_path}/{self._user_id}/")
        if not os.path.exists(user_video_path):
            os.makedirs(user_video_path)

        video_filename = self.generate_random_video_title()
        video_full_path = os.path.join(user_video_path, video_filename)

        try:
            ydl_opts = {
                "outtmpl": os.path.join(video_full_path),
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        except Exception as e:
            logs.log_error(f"An Error occurred while downloading videos: {e}")

    def save_downloaded_videos(self, video_urls: List[str]):
        """Save and download scraped videos from facebook profile"""
        try:
            with Progress() as progress:
                task = progress.add_task("[cyan]Downloading...", total=len(video_urls))
                for index, url in enumerate(video_urls, 1):
                    self.download_video(url)

                    progress.update(
                        task,
                        advance=1,
                        description=f"[cyan]Downloading... {index}/{len(video_urls)}",
                    )
        except Exception as e:
            logs.log_error(f"An Error occurred while downloading videos: {e}")

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    def save_and_download_videos_pipeline(self) -> None:
        """Pipeline to save video url to database and download as a local file"""
        try:
            rprint("[bold]Step 1 of 5 - Load cookies[/bold]")
            self._load_cookies()
            rprint("[bold]Step 2 of 5 - Refresh driver[/bold]")
            self._driver.refresh()
            rprint("[bold]Step 3 of 5 - Scrolling page[/bold]")
            self.scroll_page()
            rprint("[bold]Step 4 of 5 - Extract videos urls[/bold]")
            videos = self.extract_videos_urls()
            print(videos)
            rprint("[bold]Step 5 of 5 - Extract videos urls[/bold]")
            self.save_downloaded_videos(videos)

            if not person_exists(self._user_id):
                create_person(self._user_id)

            person_id = get_person(self._user_id).id
            for video in videos:
                create_videos(video, person_id)

            self._driver.quit()
            self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")

    def save_video_urls_to_database_pipeline(self) -> None:
        """Pipeline to save video url to database"""
        try:
            rprint("[bold]Step 1 of 4 - Load cookies[/bold]")
            self._load_cookies()
            rprint("[bold]Step 2 of 4 - Refresh driver[/bold]")
            self._driver.refresh()
            rprint("[bold]Step 3 of 4 - Scrolling page[/bold]")
            self.scroll_page()
            rprint("[bold]Step 4 of 4 - Extract videos urls[/bold]")
            videos = self.extract_videos_urls()
            rprint(videos)

            if not person_exists(self._user_id):
                create_person(self._user_id)

            person_id = get_person(self._user_id).id
            for video in videos:
                create_videos(video, person_id)

            self._driver.quit()
            self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
