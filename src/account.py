import logging
import pickle
from time import sleep
from typing import List, Dict
import os

from config import Config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import database
import models
from scraper import Scraper
import requests
from PIL import Image
from io import BytesIO
import random
import string


# Logging setup
logging.basicConfig(
    filename=Config.LOG_FILE_PATH,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

models.Base.metadata.create_all(database.engine)


class FacebookBaseScraper(Scraper):
    def __init__(self, user_id) -> None:
        super().__init__()
        self._user_id = user_id
        self._base_url = f"https://www.facebook.com/{self._user_id}"
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self._driver.get(self._base_url)
        self._wait = WebDriverWait(self._driver, 10)

    def _load_cookies(self) -> None:
        """
        Load cookies with a log in session
        """
        try:
            self._driver.delete_all_cookies()
            with open(Config.COOKIES_FILE_PATH, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    try:
                        self._driver.add_cookie(cookie)
                    except Exception as e:
                        logging.error(f"Error adding cookie: {cookie}, Exception: {e}")
        except Exception as e:
            logging.error(f"Error loading cookies: {e}")


class AccountScraper(Scraper):
    """
    Scrape user's personal information
    """

    def __init__(self, user_id) -> None:
        super().__init__()
        self._user_id = user_id
        self._base_url = f"https://www.facebook.com/{self._user_id}"
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self._driver.get(self._base_url)
        self._wait = WebDriverWait(self._driver, 10)

    def _load_cookies(self) -> None:
        """
        Load cookies with a log in session
        """
        try:
            self._driver.delete_all_cookies()
            with open(Config.COOKIES_FILE_PATH, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    try:
                        self._driver.add_cookie(cookie)
                    except Exception as e:
                        logging.error(f"Error adding cookie: {cookie}, Exception: {e}")
        except Exception as e:
            logging.error(f"Error loading cookies: {e}")

    def extract_work_and_education(self) -> List[Dict[str, str]]:
        """Scrape for history of employment and school"""

        extracted_work_data = []
        try:
            self._driver.get(f"{self._base_url}/{Config.WORK_AND_EDUCATION_URL}")

            work_entries = self._driver.find_elements(
                By.CSS_SELECTOR,
                "div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.x1nhvcw1.x1qjc9v5.xozqiw3.x1q0g3np.xexx8yu.xykv574.xbmpl8g.x4cne27.xifccgj.xs83m0k",
            )
            for entry in work_entries:
                owner_element = entry.find_element(By.XPATH, ".//span[@dir='auto']")
                owner = owner_element.text.strip()

                if owner.startswith("http") or owner.startswith("www"):
                    work_entry_data = {"name": owner}
                else:
                    work_entry_data = {"name": owner}

                extracted_work_data.append(work_entry_data)

        except Exception as e:
            logging.error(f"Error extracting work data: {e}")

        return extracted_work_data

    def extract_places(self) -> List[Dict[str, str]]:
        """Return history of places"""
        places = []
        try:
            self._driver.get(f"{self._base_url}/{Config.PLACES_URL}")

            div_elements = self._driver.find_elements(
                By.CSS_SELECTOR, "div.x13faqbe.x78zum5"
            )

            for div_element in div_elements:
                name_element = div_element.find_element(
                    By.CSS_SELECTOR, "a[class*='x1i10hfl']"
                )
                name = name_element.text.strip()

                date_element = div_element.find_element(
                    By.CSS_SELECTOR, "div span[class*='xi81zsa']"
                )
                date = date_element.text.strip()

                places.append({"name": name, "date": date})

        except Exception as e:
            logging.error(f"Error extracting localization data: {e}")

        return places

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        self._load_cookies()
        self._driver.refresh()
        y = self.extract_places()
        print(y)
        x = self.extract_work_and_education()
        print(x)
        self._driver.quit()


class FacebookImageScraper(Scraper):
    """
    Scrape user's pictures
    """

    def __init__(self, user_id) -> None:
        super().__init__()
        self._user_id = user_id
        self._base_url = f"https://www.facebook.com/{self._user_id}/photos"
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self._driver.get(self._base_url)
        self._wait = WebDriverWait(self._driver, 10)

    def _load_cookies(self) -> None:
        """
        Load cookies with a log in session
        """
        try:
            self._driver.delete_all_cookies()
            with open(Config.COOKIES_FILE_PATH, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    try:
                        self._driver.add_cookie(cookie)
                    except Exception as e:
                        logging.error(f"Error adding cookie: {cookie}, Exception: {e}")
        except Exception as e:
            logging.error(f"Error loading cookies: {e}")

    def scroll_page(self) -> None:
        """
        Scrolls the page to load more friends from a list
        """
        try:
            last_height = self._driver.execute_script(
                "return document.body.scrollHeight"
            )
            consecutive_scrolls = 0

            while consecutive_scrolls < Config.MAX_CONSECUTIVE_SCROLLS:
                self._driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

                sleep(Config.SCROLL_PAUSE_TIME)
                new_height = self._driver.execute_script(
                    "return document.body.scrollHeight"
                )

                if new_height == last_height:
                    consecutive_scrolls += 1
                else:
                    consecutive_scrolls = 0

                last_height = new_height
        except Exception as e:
            logging.error(f"Error occurred while scrolling: {e}")

    def extract_image_urls(self) -> List[str]:
        """
        Return a list of all the image urls
        """
        extracted_image_urls = []
        try:
            img_elements = self._driver.find_elements(
                By.CSS_SELECTOR,
                "img.xzg4506.xycxndf.xua58t2.x4xrfw5.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x9f619.x5yr21d.xl1xv1r.xh8yej3",
            )
            for img_element in img_elements:
                src_attribute = img_element.get_attribute("src")
                if src_attribute:
                    extracted_image_urls.append(src_attribute)

        except Exception as e:
            logging.error(f"Error extracting image URLs: {e}")

        return extracted_image_urls

    @staticmethod
    def generate_image_file_name() -> str:
        """
        Generate a random image file name
        """
        random_name = "".join(random.choice(string.ascii_letters) for _ in range(10))
        return f"{random_name}.jpg"

    @staticmethod
    def check_image_type(image_content) -> bool:
        """
        Check if file is an image
        """
        try:
            _ = Image.open(BytesIO(image_content))
            return True
        except Exception as e:
            logging.error(f"Skipping image, Exception: {e}")
            return False

    def save_images(self, image_urls: List[str]) -> None:
        """
        Download and save images from url
        """
        try:
            for url in image_urls:
                response = requests.get(url)
                response.raise_for_status()

                image_content = response.content

                image_type = self.check_image_type(image_content)
                if not image_type:
                    continue

                image_directory = os.path.dirname(Config.IMAGE_PATH)
                if not os.path.exists(image_directory):
                    os.makedirs(image_directory)

                user_image_directory = os.path.dirname(
                    f"{Config.IMAGE_PATH}/{self._user_id}/"
                )
                if not os.path.exists(user_image_directory):
                    os.makedirs(user_image_directory)

                image_filename = self.generate_image_file_name()
                image_path = os.path.join(user_image_directory, image_filename)
                with open(image_path, "wb") as file:
                    file.write(image_content)

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Request error: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request error: {req_err}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        self._load_cookies()
        self._driver.refresh()
        self.scroll_page()
        x = self.extract_image_urls()
        self.save_images(x)
        self._driver.quit()


class FriendListScraper(Scraper):
    """
    Scrape user's friends list
    """

    def __init__(self, user_id) -> None:
        super().__init__()
        self._user_id = user_id
        self._base_url = f"https://www.facebook.com/{self._user_id}/friends"
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self._driver.get(self._base_url)
        self._wait = WebDriverWait(self._driver, 10)

    def _load_cookies(self) -> None:
        """
        Load cookies with a log in session
        """
        try:
            self._driver.delete_all_cookies()
            with open(Config.COOKIES_FILE_PATH, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    try:
                        self._driver.add_cookie(cookie)
                    except Exception as e:
                        logging.error(f"Error adding cookie: {cookie}, Exception: {e}")
        except Exception as e:
            logging.error(f"Error loading cookies: {e}")

    def extract_friends_data(self) -> List[Dict[str, str]]:
        """
        Return a list of dictionaries with the usernames and the urls to the profile for every person in friends list
        """
        extracted_elements = []

        try:
            elements = self._driver.find_elements(By.CSS_SELECTOR, "a.x1i10hfl span")
            for element in elements:
                username = element.text.strip()
                url = element.find_element(By.XPATH, "..").get_attribute("href")
                if username == "":
                    continue
                element_data = {"username": username, "url": url}
                extracted_elements.append(element_data)

        except Exception as e:
            logging.error(f"Error extracting friends data: {e}")

        return extracted_elements

    def scroll_page(self) -> None:
        """
        Scrolls the page to load more friends from a list
        """
        try:
            last_height = self._driver.execute_script(
                "return document.body.scrollHeight"
            )
            consecutive_scrolls = 0

            while consecutive_scrolls < Config.MAX_CONSECUTIVE_SCROLLS:
                self._driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

                sleep(Config.SCROLL_PAUSE_TIME)
                self.extract_friends_data()
                new_height = self._driver.execute_script(
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
        self._load_cookies()
        self._driver.refresh()
        self.scroll_page()
        self._driver.quit()
