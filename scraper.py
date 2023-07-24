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

SCROLL_PAUSE_TIME = 2
MAX_CONSECUTIVE_SCROLLS = 3


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
        self.wait = WebDriverWait(self.driver, 10)

    def load_cookies(self) -> None:
        """
        Load cookies with a log in session
        """
        try:
            logging.info("Start loading cookies with log in session")
            self.driver.delete_all_cookies()
            with open("cookies.json", "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            logging.info("Cookies loaded correctly")
        except Exception as e:
            logging.error(f"Error loading cookies: {e}")

    def scroll_page(self) -> None:
        """
        Scrolls the page to load more friends from a list
        """
        try:
            logging.info("Start scrolling page")
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            consecutive_scrolls = 0

            while consecutive_scrolls < MAX_CONSECUTIVE_SCROLLS:
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

                sleep(SCROLL_PAUSE_TIME)

                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )

                if new_height == last_height:
                    consecutive_scrolls += 1
                else:
                    consecutive_scrolls = 0

                last_height = new_height
            logging.info("Scrolling page finished")
        except Exception as e:
            logging.error(f"Error occurred while scrolling: {e}")

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            logging.info("Start pipeline to scrape a friend list on facebook")
            self.load_cookies()
            self.driver.refresh()
            self.scroll_page()
            logging.info("Pipeline finished")
        except Exception as e:
            logging.error(f"Error occurred while running the pipeline: {e}")
        finally:
            self.driver.quit()
