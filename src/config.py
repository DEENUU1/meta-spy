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

    # Graph database
    DATABASE_URL = os.getenv("DATABASE_URL")
    GRAPH_DATABASE_USERNAME = os.getenv("GRAPHDATABASE_USERNAME")
    GRAPH_DATABASE_PASSWORD = os.getenv("GRAPHDATABASE_PASSWORD")

    # Facebook login
    FACEBOOK_EMAIL = os.getenv("FACEBOOK_EMAIL")
    FACEBOOK_PASSWORD = os.getenv("FACEBOOK_PASSWORD")
    COOKIES_FILE_PATH = "../cookies.json"

    # logs
    LOG_FILE_PATH = "../logs.json"

    # SQLALCHEMY DATABASE
    SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"
