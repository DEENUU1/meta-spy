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
from typing import List, Dict


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
            self.driver.delete_all_cookies()
            with open("cookies.json", "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
        except Exception as e:
            logging.error(f"Error loading cookies: {e}")

    def extract_friends_data(self) -> List[Dict[str, str]]:
        extracted_elements = []

        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a.x1i10hfl")

            for element in elements:
                element_data = {
                    "username": element.text,
                    "url": element.get_attribute("href"),
                }
                print(element_data)
                extracted_elements.append(element_data)

        except Exception as e:
            logging.error(f"Error extracting friends data: {e}")

        return extracted_elements

    def scroll_page(self) -> None:
        """
        Scrolls the page to load more friends from a list
        """
        try:
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            consecutive_scrolls = 0

            while consecutive_scrolls < MAX_CONSECUTIVE_SCROLLS:
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

                sleep(SCROLL_PAUSE_TIME)
                self.extract_friends_data()
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )

                if new_height == last_height:
                    consecutive_scrolls += 1
                else:
                    consecutive_scrolls = 0

                last_height = new_height
        except Exception as e:
            logging.error(f"Error occurred while scrolling: {e}")

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            self.load_cookies()
            self.driver.refresh()
            self.scroll_page()
        except Exception as e:
            logging.error(f"Error occurred while running the pipeline: {e}")
        finally:
            self.driver.quit()
