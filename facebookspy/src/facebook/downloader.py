from ..config import Config
import youtube_dl
import os
import random
import string
from ..logs import Logs
from ..repository import (
    get_videos,
    get_person,
    get_new_videos,
    update_videos_downloaded,
)
from rich.progress import Progress


logs = Logs()


class Downloader:
    """
    Download videos from facebook
    """

    def __init__(self, person_facebook_id: str = None) -> None:
        self.person_facebook_id = person_facebook_id
        self.video_path = Config.VIDEO_PATH
        self.success = False

    @staticmethod
    def generate_random_video_title() -> str:
        """Generate random video title"""
        chars = string.ascii_letters
        return "".join(random.choice(chars) for _ in range(12))

    @staticmethod
    def download_video(path: str, video_url: str) -> None:
        try:
            ydl_opts = {
                "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        except Exception as e:
            logs.log_error(f"An Error occurred while downloading videos: {e}")

    def save_person_video(self, video_url: str) -> None:
        """Download videos from specified account"""
        if not os.path.exists(self.video_path):
            os.makedirs(self.video_path)

        person_video_path = os.path.dirname(
            f"{self.video_path}/{self.person_facebook_id}/"
        )
        print(person_video_path)
        if not os.path.exists(person_video_path):
            os.makedirs(person_video_path)

        video_filename = self.generate_random_video_title()
        video_full_path = os.path.join(person_video_path, video_filename)

        self.download_video(video_full_path, video_url)

    def save_single_video(self, video_url: str) -> None:
        """Download single video just by passing url"""
        if not os.path.exists(self.video_path):
            os.makedirs(self.video_path)

        video_filename = self.generate_random_video_title()
        video_full_path = os.path.join(self.video_path, video_filename)

        self.download_video(video_full_path, video_url)

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    def download_all_person_videos_pipeline(self) -> None:
        """Download videos from specified facebook account based on the urls from the database
        This command download all videos and may create duplicates"""

        person = get_person(self.person_facebook_id)
        videos = get_videos(person.id)
        try:
            with Progress() as progress:
                task = progress.add_task("[cyan]Downloading...", total=len(videos))

                for idx, video in enumerate(videos, 1):
                    self.save_person_video(video.url)

                    progress.update(
                        task,
                        advance=1,
                        description=f"[cyan]Downloading... {idx}/{len(videos)}",
                    )
                    update_videos_downloaded(video.id)

            self.success = True

        except Exception as e:
            logs.log_error(
                f"An Error occurred while downloading videos for {self.person_facebook_id}: {e}"
            )

    def download_new_person_videos_pipeline(self) -> None:
        """Download videos from specified facebook account based on the urls from the database
        This command downloads only new not downloaded yet videos"""
        person = get_person(self.person_facebook_id)
        videos = get_new_videos(person.id)
        try:
            with Progress() as progress:
                task = progress.add_task("[cyan]Downloading...", total=len(videos))

                for idx, video in enumerate(videos, 1):
                    self.save_person_video(video.url)

                    progress.update(
                        task,
                        advance=1,
                        description=f"[cyan]Downloading... {idx}/{len(videos)}",
                    )
                    update_videos_downloaded(video.id)

            self.success = True

        except Exception as e:
            logs.log_error(
                f"An Error occurred while downloading videos for {self.person_facebook_id}: {e}"
            )

    def download_single_video_pipeline(self, video_url: str) -> None:
        """Download videos just by passing a URL"""
        try:
            self.save_single_video(video_url)

            self.success = True

        except Exception as e:
            logs.log_error(f"An Error occurred while downloading video: {e}")
