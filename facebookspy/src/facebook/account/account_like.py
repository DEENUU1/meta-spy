from time import sleep
from typing import List

from ...config import Config
from selenium.webdriver.common.by import By
from ...repository import person_repository, like_repository
from ..facebook_base import BaseFacebookScraper
from ...logs import Logs
from rich import print as rprint
from ..scroll import scroll_page

logs = Logs()


class AccountLike(BaseFacebookScraper):
    """
    Scrape user's likes
    """

    def __init__(self, user_id) -> None:
        super().__init__(user_id, base_url=f"https://www.facebook.com/{user_id}/likes")
        self.success = False

    def extract_likes_data(self) -> List[str]:
        extracted_elements = []
        try:
            div_element = self._driver.find_element(
                By.CSS_SELECTOR, "div.xyamay9.x1pi30zi.x1l90r2v.x1swvt13"
            )
            elements = div_element.find_elements(
                By.CSS_SELECTOR,
                "span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.x1s688f.xzsf02u.x1yc453h",
            )
            for element in elements:
                extracted_elements.append(element.text)

        except Exception as e:
            logs.log_error(f"Error extracting friends data: {e}")

        return extracted_elements

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            rprint("[bold]Step 1 of 4 - Load cookies[/bold]")
            self._load_cookies()
            rprint("[bold]Step 2 of 3 - Refresh driver[/bold]")
            self._driver.refresh()
            rprint("[bold]Step 3 of 4 - Scrolling page[/bold]")
            # self.scroll_page()
            scroll_page(self._driver)
            rprint("[bold]Step 4 of 4 - Extracting likes data[/bold]")
            extracted_data = self.extract_likes_data()
            rprint(extracted_data)

            rprint(
                "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
            )

            if not person_repository.person_exists(self._user_id):
                person_repository.create_person(self._user_id)

            person_id = person_repository.get_person(self._user_id).id

            for data in extracted_data:
                if not like_repository.like_exists(data):
                    like_repository.create_like(person_id, data)

            self._driver.quit()
            self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
