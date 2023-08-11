from time import sleep
from typing import List
from .config import Config
import youtube_dl
import os
import random
import string
from .logs import Logs
from rich import print as rprint


logs = Logs("downloader.py")


class Downloader:
    """
    Download videos from facebook
    """

    @staticmethod
    def generate_random_video_title() -> str:
        """Generate random video title"""
        chars = string.ascii_letters
        return "".join(random.choice(chars) for _ in range(12))

    def download_person_video(self):
        """Download videos/reels from specified account"""
        pass

    def download_single_video(self):
        """Download single video/reel just by passing url"""
        pass
