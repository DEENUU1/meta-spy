import logging
import pickle
from typing import List, Dict

from config import Config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from scraper import Scraper
from rich import print
import repository


# Logging setup
logging.basicConfig(
    filename=Config.LOG_FILE_PATH,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


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

    def extract_full_name(self) -> str | None:
        """Extract full name from homepage"""
        data = None
        print("🤟Extracting full name from homepage🤟")
        try:
            self._driver.get(self._base_url)
            fullname_element = self._driver.find_element(
                By.CSS_SELECTOR, "h1.x1heor9g.x1qlqyl8.x1pd3egz.x1a2a7pz"
            )
            data = fullname_element.text.strip()

        except Exception as e:
            logging.error(f"Error extracting full name: {e}")

        return data

    def extract_work_and_education(self) -> List[Dict[str, str]]:
        """Scrape for history of employment and school"""

        extracted_work_data = []
        print("🏫Extracting work and education🏫")
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
            print("❗Extracting work and education failed❗")

        return extracted_work_data

    def extract_places(self) -> List[Dict[str, str]]:
        """Return history of places"""
        places = []
        print("🖼️Extracting places🖼️")
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
            print("❗Extracting places failed❗")

        return places

    def extract_family(self) -> List[Dict[str, str]]:
        data = []
        print("☀️Extracting family members☀️")
        try:
            self._driver.get(f"{self._base_url}/{Config.FAMILY_URL}")

            elements = self._driver.find_elements(By.CSS_SELECTOR, "div.x1hq5gj4")

            for element in elements:
                name_element = element.find_element(
                    By.CSS_SELECTOR,
                    "span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u a",
                )
                name = name_element.text
                profile_url = name_element.get_attribute("href")
                relationship_element = element.find_element(
                    By.CSS_SELECTOR, "span.xi81zsa.x1nxh6w3.x1sibtaa"
                )
                relationship = relationship_element.text

                data.append(
                    {"name": name, "relationship": relationship, "url": profile_url}
                )
        except Exception as e:
            logging.error(f"Error extracting family data: {e}")
            print("❗Extracting family members failed❗")

        return data

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
            full_name = self.extract_full_name()
            print(full_name)

            if not repository.person_exists(self._user_id) and full_name is not None:
                repository.create_person(self._base_url, self._user_id, full_name)

            person_id = repository.get_person(self._user_id).id

            family_members = self.extract_family()
            print(family_members)
            if repository.person_exists(self._user_id):
                for member in family_members:
                    repository.create_family_member(
                        member["name"],
                        member["relationship"],
                        member["url"],
                        person_id,
                    )

            places = self.extract_places()
            print(places)

            if repository.person_exists(self._user_id):
                for place in places:
                    repository.create_places(place["name"], place["date"], person_id)

            work_and_education = self.extract_work_and_education()
            print(work_and_education)
            if repository.person_exists(self._user_id):
                for data in work_and_education:
                    repository.create_work_and_education(data["name"], person_id)

            self._driver.quit()

            self.success = True

        except Exception as e:
            logging.error(f"Error running pipeline: {e}")
