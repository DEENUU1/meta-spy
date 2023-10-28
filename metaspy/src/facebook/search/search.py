from rich import print as rprint
from ...logs import Logs
from selenium.webdriver.common.by import By
from typing import List, Optional
from ..scroll import scroll_page_callback
from .search_post import SearchBase
from enum import Enum


logs = Logs()


class SOURCE(Enum):
    PERSON = "people"
    PAGE = "pages"
    GROUP = "groups"
    PLACES = "places"
    EVENTS = "events"


class Search(SearchBase):
    def __init__(self, query: str, max_result: int, source: str):
        super().__init__(query, max_result)
        self.source = source

    def scrape_data(self) -> Optional[List[str]]:
        """
        Return a list of urls of people
        """
        extracted_urls = []

        url = self.get_url(self.source)

        try:
            self.load_driver(url)

            def extract_callback(driver):
                elements = driver.find_elements(
                    By.CSS_SELECTOR,
                    "a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f",
                )
                for element in elements:
                    url = element.get_attribute("href")
                    if len(extracted_urls) + 1 >= self.max_result:
                        self._driver.quit()
                        self.success = True

                    if url not in extracted_urls:
                        rprint(f"Extracted {self.source}: {url}")
                        extracted_urls.append(url)

            scroll_page_callback(self._driver, extract_callback)

        except Exception as e:
            logs.log_error(f"An error occurred {e}")

        return extracted_urls


class SearchPerson(Search):
    def __init__(self, query: str, max_result: int):
        super().__init__(query, max_result, SOURCE.PERSON.value)


class SearchPage(Search):
    def __init__(self, query: str, max_result: int):
        super().__init__(query, max_result, SOURCE.PAGE.value)


class SearchGroup(Search):
    def __init__(self, query: str, max_result: int):
        super().__init__(query, max_result, SOURCE.GROUP.value)


class SearchPlaces(Search):
    def __init__(self, query: str, max_result: int):
        super().__init__(query, max_result, SOURCE.PLACES.value)


class SearchEvents(Search):
    def __init__(self, query: str, max_result: int):
        super().__init__(query, max_result, SOURCE.EVENTS.value)
