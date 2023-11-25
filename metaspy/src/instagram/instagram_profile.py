from .instagram_base import BaseInstagramScraper
from ..config import Config
from ..logs import Logs
from ..facebook.scroll import scroll_page_callback
from selenium.webdriver.common.by import By
from rich import print as rprint
from typing import List, Dict, Any, Optional
import os
import random
import string
import requests
from rich.progress import Progress
from ..utils import output, save_to_json
from ..repository import instagram_image_repository, instagram_account_repository
from io import BytesIO
from PIL import Image
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logs = Logs()
config = Config()


class ProfileScraper(BaseInstagramScraper):
    def __init__(self, user_id: str) -> None:
        super().__init__(user_id, base_url=f"https://www.instagram.com/{user_id}/")
        self.success = False
        self._driver.add_cookie(
            {
                "name": "sessionid",
                "value": config.INSTAGRAM_SESSIONID_VALUE,
                "domain": ".instagram.com",
            }
        )
        self._refresh_driver()

    def _refresh_driver(self) -> None:
        """Load cookies and refresh driver"""
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

    def extract_profile_stats(self) -> Dict[str, Any]:
        data = {}
        try:
            stats_elements = WebDriverWait(self._driver, 10).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CLASS_NAME,
                        "html-span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs",
                    )
                )
            )

            stats = [stat.text for stat in stats_elements]
            print(stats)
            if len(stats) == 3:
                data["number_of_posts"] = int(stats[0])
                data["number_of_followers"] = stats[1]
                data["number_of_following"] = stats[2]

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")

        return data

    def extract_images(self):
        extracted_image_urls = []
        try:

            def extract_callback(driver):
                img_elements = self._driver.find_elements(
                    By.CLASS_NAME,
                    "x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3",
                )
                for img_element in img_elements:
                    src_attribute = img_element.get_attribute("src")
                    if src_attribute and src_attribute not in extracted_image_urls:
                        rprint(f"Extracted image URL: {src_attribute}")
                        extracted_image_urls.append(src_attribute)

            scroll_page_callback(self._driver, extract_callback)

        except Exception as e:
            logs.log_error(f"An  error occurred while extracting images: {e}")

        return extracted_image_urls

    def pipeline_stats(self) -> None:
        try:
            rprint(f"[bold]Step 1 of 2 - Loading profile page[/bold]")
            data = self.extract_profile_stats()

            if not data:
                output.print_no_data_info()
                self._driver.quit()
                self.success = False

            else:
                rprint(f"[bold]Step 2 of 2 - Saving profile stats[/bold]")
                output.print_data_from_dict(data)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                if not instagram_account_repository.account_exists(self._user_id):
                    instagram_account_repository.create_account(self._user_id)
                    instagram_account_repository.update_account(
                        self._user_id,
                        number_of_posts=data["number_of_posts"],
                        number_of_followers=data["number_of_followers"],
                        number_of_following=data["number_of_following"],
                    )
                else:
                    instagram_account_repository.update_account(
                        self._user_id,
                        number_of_posts=data["number_of_posts"],
                        number_of_followers=data["number_of_followers"],
                        number_of_following=data["number_of_following"],
                    )

                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")

    def pipeline_images(self) -> None:
        try:
            rprint(f"[bold]Step 1 of 2 - Loading profile page[/bold]")
            image_urls = self.extract_images()

            if not image_urls:
                output.print_no_data_info()
                self._driver.quit()
                self.success = False
            else:
                rprint(f"[bold]Step 2 of 2 - Downloading and saving images [/bold]")
                image_paths = self.save_images(image_urls)

                output.print_list(image_paths)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(self._user_id, image_urls).save()

                if not instagram_account_repository.account_exists(self._user_id):
                    instagram_account_repository.create_account(self._user_id)

                account_id = instagram_account_repository.get_account(self._user_id).id
                for url in image_urls:
                    instagram_image_repository.create_image(url, account_id)

                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")

        finally:
            self._driver.quit()
