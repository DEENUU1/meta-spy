from time import sleep
from typing import List
from .config import Config
import youtube_dl
import os
import random
import string
from .logs import Logs
from rich import print as rprint
from .repository import get_person

logs = Logs("downloader.py")


class Downloader:
    """
    Download videos from facebook
    """

    def __init__(self, video_url: str, person_facebook_id: str = None) -> None:
        self.person_facebook_id = person_facebook_id
        self.video_url = video_url
        self.video_path = Config.VIDEO_PATH

    @staticmethod
    def generate_random_video_title() -> str:
        """Generate random video title"""
        chars = string.ascii_letters
        return "".join(random.choice(chars) for _ in range(12))

    @staticmethod
    def download_video(path: str, video_url: str):
        try:
            ydl_opts = {"outtmpl": os.path.join(path)}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        except Exception as e:
            logs.log_error(f"An Error occurred while downloading videos: {e}")

    def save_person_video(self):
        """Download videos/reels from specified account"""
        if not os.path.exists(self.video_path):
            os.makedirs(self.video_url)

        person_video_path = os.path.dirname(
            f"{self.video_path}/{self.person_facebook_id}/"
        )
        if not os.path.exists(person_video_path):
            os.makedirs(person_video_path)

        video_filename = self.generate_random_video_title()
        video_full_path = os.path.join(person_video_path, video_filename)

        self.download_video(video_full_path, self.video_url)

    def save_single_video(self):
        """Download single video/reel just by passing url"""
        if not os.path.exists(self.video_path):
            os.makedirs(self.video_path)

        video_filename = self.generate_random_video_title()
        video_full_path = os.path.join(self.video_path, video_filename)

        self.download_video(video_full_path, self.video_url)
