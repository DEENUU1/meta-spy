from typing import List, Dict

from rich import print as rprint
from selenium.webdriver.common.by import By

from ..facebook_base import BaseFacebookScraper
from ..scroll import scroll_page
from ...logs import Logs
from ...repository import person_repository, review_repository

logs = Logs()


class AccountReview(BaseFacebookScraper):
    """
    Scrape user's pictures
    """

    def __init__(self, user_id) -> None:
        super().__init__(
            user_id, base_url=f"https://www.facebook.com/{user_id}/reviews_written"
        )
        self.success = False

    def _load_cookies_and_refresh_driver(self) -> None:
        """Load cookies and refresh driver"""
        self._load_cookies()
        self._driver.refresh()

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    def extract_reviews(self) -> List[Dict[str, str]]:
        """
        Return data about recent places
        """
        extracted_reviews = []
        try:
            div_elements = self._driver.find_elements(
                By.CSS_SELECTOR,
                "div.x6s0dn4.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x1olyfxc.x9f619.x78zum5.x1e56ztr.xyamay9.x1pi30zi.x1l90r2v.x1swvt13",
            )

            for div_element in div_elements:
                data = {}
                company_element = div_element.find_element(
                    By.CSS_SELECTOR,
                    "span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x676frb.x1lkfr7t.x1lbecb7.x1s688f.xzsf02u",
                )
                data["company"] = company_element.text

                div_inside_elements = div_element.find_elements(
                    By.CSS_SELECTOR, "div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs"
                )

                opinions = [
                    opinion_element.text for opinion_element in div_inside_elements
                ]
                data["opinions"] = opinions

                extracted_reviews.append(data)
        except Exception as e:
            logs.log_error(f"Error extracting image URLs: {e}")

        return extracted_reviews

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            rprint("[bold]Step 1 of 3 - Load cookies[/bold]")
            self._load_cookies_and_refresh_driver()

            rprint("[bold]Step 2 of 3 - Scrolling page[/bold]")
            scroll_page(self._driver)

            rprint("[bold]Step 3 of 3 - Extract reviews[/bold]")
            reviews = self.extract_reviews()
            rprint(reviews)

            rprint(
                "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
            )

            if not person_repository.person_exists(self._user_id):
                person_repository.create_person(self._user_id)

            person_id = person_repository.get_person(self._user_id).id

            for review_data in reviews:
                opinion = "".join([data for data in review_data["opinions"]])
                if not review_repository.review_exists(
                    review_data["company"], opinion, person_id
                ):
                    review_repository.create_reviews(
                        review_data["company"], opinion, person_id
                    )

            self._driver.quit()
            self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
