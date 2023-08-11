from time import sleep
from typing import List
from .config import Config
import youtube_dl
import os
import random
import string
from .logs import Logs
from rich import print as rprint
from .repository import get_videos, get_reels, get_person
from rich.progress import Progress


logs = Logs("downloader.py")


class Downloader:
    """
    Download videos from facebook
    """

    def __init__(self, person_facebook_id: str = None) -> None:
        self.person_facebook_id = person_facebook_id
        self.video_path = Config.VIDEO_PATH
        self.person = get_person(self.person_facebook_id)

    @staticmethod
    def generate_random_video_title() -> str:
        """Generate random video title"""
        chars = string.ascii_letters
        return "".join(random.choice(chars) for _ in range(12))

    @staticmethod
    def download_video(path: str, video_url: str) -> None:
        try:
            ydl_opts = {"outtmpl": os.path.join(path)}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        except Exception as e:
            logs.log_error(f"An Error occurred while downloading videos: {e}")

    def save_person_video(self, video_url: str) -> None:
        """Download videos/reels from specified account"""
        if not os.path.exists(self.video_path):
            os.makedirs(self.video_path)

        person_video_path = os.path.dirname(
            f"{self.video_path}/{self.person_facebook_id}/"
        )
        if not os.path.exists(person_video_path):
            os.makedirs(person_video_path)

        video_filename = self.generate_random_video_title()
        video_full_path = os.path.join(person_video_path, video_filename)

        self.download_video(video_full_path, video_url)

    def save_single_video(self, video_url: str) -> None:
        """Download single video/reel just by passing url"""
        if not os.path.exists(self.video_path):
            os.makedirs(self.video_path)

        video_filename = self.generate_random_video_title()
        video_full_path = os.path.join(self.video_path, video_filename)

        self.download_video(video_full_path, video_url)

    def download_person_videos_pipeline(self) -> None:
        """Download videos from specified facebook account based on the urls from the database"""
        videos = get_videos(self.person)
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

        except Exception as e:
            logs.log_error(
                f"An Error occurred while downloading videos for {self.person_facebook_id}: {e}"
            )

    def download_single_video_pipeline(self, video_url: str) -> None:
        """Download videos just by passing a URL"""
        self.save_single_video(video_url)

    def download_person_reels_pipeline(self) -> None:
        """Download reels from specified facebook account based on the urls from the database"""
        reels = get_reels(self.person)
        try:
            with Progress() as progress:
                task = progress.add_task("[cyan]Downloading...", total=len(reels))

                for idx, reel in enumerate(reels, 1):
                    self.save_person_video(reel.url)

                    progress.update(
                        task,
                        advance=1,
                        description=f"[cyan]Downloading... {idx}/{len(reels)}",
                    )

        except Exception as e:
            logs.log_error(
                f"An Error occurred while downloading reels for {self.person_facebook_id}: {e}"
            )
