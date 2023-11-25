import os
import random
import string
from io import BytesIO
from typing import List

import requests
from PIL import Image
from rich import print as rprint
from rich.progress import Progress
from selenium.webdriver.common.by import By

from ..facebook_base import BaseFacebookScraper
from ..scroll import scroll_page_callback
from ...config import Config
from ...logs import Logs
from ...repository import person_repository, image_repository
from ...utils import output, save_to_json

logs = Logs()


class AccountImage(BaseFacebookScraper):
    """
    Scrape user's pictures
    """

    def __init__(self, user_id: str) -> None:
        super().__init__(user_id, base_url=f"https://www.facebook.com/{user_id}/photos")
        self.success = False

    def _load_cookies_and_refresh_driver(self) -> None:
        """Load cookies and refresh driver"""
        self._load_cookies()
        self._driver.refresh()

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    @staticmethod
    def generate_image_file_name() -> str:
        """
        Generate a random image file name
        """
        random_name = "".join(random.choice(string.ascii_letters) for _ in range(10))
        return f"{random_name}.jpg"

    def extract_image_urls(self) -> List[str]:
        """
        Return a list of all the image urls
        """
        extracted_image_urls = []
        try:

            def extract_callback(driver):
                div_element = self._driver.find_element(
                    By.CLASS_NAME, "xyamay9.x1pi30zi.x1l90r2v.x1swvt13"
                )
                img_elements = div_element.find_elements(
                    By.CSS_SELECTOR,
                    "img.xzg4506.xycxndf.xua58t2.x4xrfw5.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x9f619.x5yr21d.xl1xv1r.xh8yej3",
                )
                for img_element in img_elements:
                    src_attribute = img_element.get_attribute("src")
                    if src_attribute and src_attribute not in extracted_image_urls:
                        rprint(f"Extracted image URL: {src_attribute}")
                        extracted_image_urls.append(src_attribute)

            scroll_page_callback(self._driver, extract_callback)

        except Exception as e:
            logs.log_error(f"Error extracting image URLs: {e}")

        return extracted_image_urls

    @staticmethod
    def check_image_type(image_content) -> bool:
        """
        Check if file is an image
        """
        try:
            _ = Image.open(BytesIO(image_content))
            return True
        except Exception as e:
            logs.log_error(f"Skipping image, Exception: {e}")
            return False

    def save_images(self, image_urls: List[str]) -> List[str]:
        """
        Download and save images from url
        """
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
            logs.log_error(f"Request error: {http_err}")

        except requests.exceptions.RequestException as req_err:
            logs.log_error(f"Request error: {req_err}")
        except Exception as e:
            logs.log_error(f"An error occurred: {e}")

        return downloaded_image_paths

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            rprint("[bold]Step 1 of 3 - Load cookies[/bold]")
            self._load_cookies_and_refresh_driver()

            rprint("[bold]Step 2 of 3 - Extract image urls[/bold]")
            image_urls = self.extract_image_urls()

            if not image_urls:
                output.print_no_data_info()
                self._driver.quit()
                self.success = False
            else:
                rprint("[bold]Step 3 of 3 - Downloading images[/bold]")
                image_paths = self.save_images(image_urls)

                output.print_list(image_paths)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(
                    self._user_id,
                    image_urls,
                ).save()

                if not person_repository.person_exists(self._user_id):
                    person_repository.create_person(self._user_id)

                person_object = person_repository.get_person(self._user_id).id
                for url in image_urls:
                    image_repository.create_image(url, person_object)

                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
