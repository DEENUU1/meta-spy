from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

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

    def __init__(self) -> None:
        self.base_url = "https://www.facebook.com/"
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver = self.driver
        self.driver.get(self.base_url)
