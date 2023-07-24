from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import json

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
        self.load_cookies()
        self.driver.get(self.base_url)

    def load_cookies(self) -> None:
        try:
            with open("cookies.json", "r") as file:
                cookies = json.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
        except Exception as e:
            logging.error(f"Error loading cookies: {e}")

    def scroll_page(self) -> None:
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script(
                    "return document.body.scrollHeight"
                )
                > last_height
            )
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            if last_height == self.driver.execute_script(
                "return document.body.scrollHeight"
            ):
                break
