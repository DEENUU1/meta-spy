from typing import List

from rich import print as rprint
from selenium.webdriver.common.by import By

from ..facebook_base import BaseFacebookScraper
from ..scroll import scroll_page
from ...logs import Logs
from ...repository import (
    person_repository,
    video_repository,
)
from ...utils import output

logs = Logs()


class AccountVideo(BaseFacebookScraper):
    """
    Scrape user's pictures
    """

    def __init__(self, user_id: str) -> None:
        super().__init__(user_id, base_url=f"https://www.facebook.com/{user_id}/videos")
        self.success = False

    def _load_cookies_and_refresh_driver(self) -> None:
        """Load cookies and refresh driver"""
        self._load_cookies()
        self._driver.refresh()

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    @staticmethod
    def extract_urls(video_elements) -> List[str]:
        extracted_videos_urls = []
        for video_element in video_elements:
            src_attribute = video_element.get_attribute("href")
            if src_attribute:
                extracted_videos_urls.append(src_attribute)
        return extracted_videos_urls

    def scrape_video_urls(self) -> List[str]:
        """
        Return a list of all the image urls
        """
        extracted_videos_urls = []
        try:
            div_element = self._driver.find_element(
                By.CLASS_NAME,
                "x1qjc9v5.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x78zum5.xdt5ytf.x1l90r2v.xyamay9.xjl7jj",
            )
            videos_elements = div_element.find_elements(
                By.CSS_SELECTOR,
                "a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv",
            )
            extracted_videos_urls = self.extract_urls(videos_elements)
        except Exception as e:
            logs.log_error(f"An Error extracting while extracting video URL: {e}")

        if not extracted_videos_urls:
            try:
                div_element = self._driver.find_element(
                    By.CLASS_NAME, "xyamay9.x1pi30zi.x1l90r2v.x1swvt13"
                )
                videos_elements = div_element.find_elements(
                    By.CSS_SELECTOR,
                    "a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.x1lliihq.x5yr21d.x1n2onr6.xh8yej3",
                )
                extracted_videos_urls = self.extract_urls(videos_elements)
            except Exception as e:
                logs.log_error(f"An Error extracting while extracting video URL: {e}")

        return extracted_videos_urls

    def save_video_urls_to_database_pipeline(self) -> None:
        """Pipeline to save video url to database"""
        try:
            rprint("[bold]Step 1 of 3 - Load cookies[/bold]")
            self._load_cookies_and_refresh_driver()

            rprint("[bold]Step 2 of 3 - Scrolling page[/bold]")
            scroll_page(self._driver)

            rprint("[bold]Step 3 of 3 - Extract videos urls[/bold]")
            videos = self.scrape_video_urls()

            if not videos:
                output.print_no_data_info()
                self._driver.quit()
                self.success = False
            else:
                output.print_list(videos)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                if not person_repository.person_exists(self._user_id):
                    person_repository.create_person(self._user_id)

                person_id = person_repository.get_person(self._user_id).id
                for data in videos:
                    if not video_repository.video_exists(data, person_id):
                        video_repository.create_videos(data, person_id)

                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
