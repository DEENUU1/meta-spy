import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class for the application.
    """

    # Scrolling
    SCROLL_PAUSE_TIME = 1
    MAX_CONSECUTIVE_SCROLLS = 3

    # Facebook login
    FACEBOOK_EMAIL = os.getenv("FACEBOOK_EMAIL")
    FACEBOOK_PASSWORD = os.getenv("FACEBOOK_PASSWORD")
    COOKIES_FILE_PATH = "../cookies.json"

    # logs
    LOG_FILE_PATH = "../logs.json"

    # SQLALCHEMY DATABASE
    SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"