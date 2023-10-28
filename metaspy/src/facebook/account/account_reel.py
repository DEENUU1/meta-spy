from typing import List

from rich import print as rprint
from selenium.webdriver.common.by import By

from ..facebook_base import BaseFacebookScraper
from ..scroll import scroll_page
from ...logs import Logs
from ...repository import person_repository, reel_repository
from ...utils import output, save_to_json

logs = Logs()


class AccountReel(BaseFacebookScraper):
    """
    Scrape user's pictures
    """

    def __init__(self, user_id: str) -> None:
        super().__init__(user_id, base_url=f"https://www.facebook.com/{user_id}/reels")
        self.success = False

    def _load_cookies_and_refresh_driver(self) -> None:
        """Load cookies and refresh driver"""
        self._load_cookies()
        self._driver.refresh()

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    def extract_reels_urls(self) -> List[str]:
        """
        Return a list of all the image urls
        """
        extracted_reels_urls = []
        try:
            div_element = self._driver.find_element(
                By.CLASS_NAME, "xyamay9.x1pi30zi.x1l90r2v.x1swvt13"
            )
            reels_elements = div_element.find_elements(
                By.CSS_SELECTOR,
                "a.x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x1lliihq.xqitzto.x1n2onr6.xh8yej3",
            )
            for reel_element in reels_elements:
                src_attribute = reel_element.get_attribute("href")
                if src_attribute:
                    extracted_reels_urls.append(src_attribute)

        except Exception as e:
            logs.log_error(f"Error extracting reels URLs: {e}")

        return extracted_reels_urls

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            rprint("[bold]Step 1 of 3 - Load cookies[/bold]")
            self._load_cookies_and_refresh_driver()

            rprint("[bold]Step 2 of 3 - Scrolling page[/bold]")
            scroll_page(self._driver)

            rprint("[bold]Step 3 of 3 - Extract reels urls[/bold]")
            reels = self.extract_reels_urls()

            if not reels:
                output.print_no_data_info()
                self._driver.quit()
                self.success = False
            else:
                output.print_list(reels)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(
                    self._user_id,
                    reels,
                ).save()

                if not person_repository.person_exists(self._user_id):
                    person_repository.create_person(self._user_id)

                person_id = person_repository.get_person(self._user_id).id

                for data in reels:
                    if not reel_repository.reels_exists(data, person_id):
                        reel_repository.create_reels(data, person_id)

                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
