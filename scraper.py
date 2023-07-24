from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import json
import pickle
from time import sleep


# Logging setup
logging.basicConfig(
    filename="logs.json",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Chrome configuration
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-default-apps")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
chrome_options.add_argument("--profile-directory=Default")


class FacebookScraper:
    """
    Scrape user's friends and their data
    """

    def __init__(self, user_id) -> None:
        self.base_url = f"https://www.facebook.com/{user_id}/friends"
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver = self.driver
        self.driver.get(self.base_url)
        self.cookie_term_css_selector = "._42ft._4jy0._al65._4jy3._4jy1.selected._51sy"

    def load_cookies(self) -> None:
        try:
            self.driver.delete_all_cookies()
            with open("cookies.json", "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
        except Exception as e:
            logging.error(f"Error loading cookies: {e}")

    def scroll_page(self) -> None:
        pass

    def pipeline(self) -> None:
        self.load_cookies()
        self.driver.refresh()
        self.scroll_page()
