import logging
import pickle
from time import sleep
from typing import List
import os

from config import Config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from rich.progress import Progress
from scraper import Scraper
import requests
from PIL import Image
from io import BytesIO
import random
import string
from rich import print
import repository


# Logging setup
logging.basicConfig(
    filename=Config.LOG_FILE_PATH,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


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
        self.success = False

    def _load_cookies(self) -> None:
        """
        Load cookies with a log in session
        """
        print("🍪Loading cookies🍪")
        try:
            self._driver.delete_all_cookies()
            with open(Config.COOKIES_FILE_PATH, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    try:
                        self._driver.add_cookie(cookie)
                    except Exception as e:
                        logging.error(f"Error adding cookie: {cookie}, Exception: {e}")
                        print("❗Loading cookies failed❗")

        except Exception as e:
            logging.error(f"Error loading cookies: {e}")
            print("❗Loading cookies failed❗")

    def scroll_page(self) -> None:
        """
        Scrolls the page to load more friends from a list
        """
        print("🏎️Start scrolling page🏎️")
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
            print("❗Page scrolling failed❗")

    def extract_image_urls(self) -> List[str]:
        """
        Return a list of all the image urls
        """
        extracted_image_urls = []
        print("🖼️Start extracting image URLs🖼️")
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
            print("❗Extracting image URLs failed❗")

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

    def save_images(self, image_urls: List[str]) -> List[str]:
        """
        Download and save images from url
        """
        print("📝Start downloading images📝")
        downloaded_image_paths = []
        try:
            with Progress() as progress:
                task = progress.add_task("[cyan]Downloading...", total=len(image_urls))
                for index, url in enumerate(image_urls, 1):
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

                    downloaded_image_paths.append(image_path)

                    with open(image_path, "wb") as file:
                        file.write(image_content)

                    progress.update(
                        task,
                        advance=1,
                        description=f"[cyan]Downloading... ({index}/{len(image_urls)})",
                    )

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Request error: {http_err}")
            print("❗Request error while downloading images❗")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request error: {req_err}")
            print("❗Request error while downloading images❗")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            print("❗Error while downloading images❗")

        return downloaded_image_paths

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            self._load_cookies()
            self._driver.refresh()
            self.scroll_page()
            image_urls = self.extract_image_urls()
            image_paths = self.save_images(image_urls)

            if repository.person_exists(self._user_id) and len(image_paths) > 0:
                person = repository.get_person(self._user_id).id
                for image_path in image_paths:
                    repository.create_image(image_path, person)

            self._driver.quit()

            self.success = True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
