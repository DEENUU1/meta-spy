import re
from typing import List, Dict, Optional

from rich import print as rprint
from selenium.webdriver.common.by import By

from ..facebook_base import BaseFacebookScraper
from ...config import Config
from ...logs import Logs
from ...repository import (
    person_repository,
    work_education_repository,
    family_member_repository,
    place_repository,
)
from ...utils import output, save_to_json

logs = Logs()


class AccountBasic(BaseFacebookScraper):
    """
    Scrape user's personal information
    """

    def __init__(self, user_id: str) -> None:
        super().__init__(user_id, base_url=f"https://www.facebook.com/{user_id}")
        self.success = False

    @property
    def is_pipeline_successful(self) -> bool:
        """Check if pipeline is successful"""
        return self.success

    def _load_cookies_and_refresh_driver(self) -> None:
        """Load cookies and refresh driver"""
        self._load_cookies()
        self._driver.refresh()

    def extract_full_name(self) -> Optional[str]:
        """Extract full name from homepage"""
        data = None
        try:
            self._driver.get(self._base_url)
            fullname_element = self._driver.find_element(
                By.CSS_SELECTOR, "h1.x1heor9g.x1qlqyl8.x1pd3egz.x1a2a7pz"
            )
            data = fullname_element.text.strip()

        except Exception as e:
            logs.log_error(f"Error occurred while extracting full name: {e}")

        return data

    def extract_work_and_education(self) -> List[Dict[str, str]]:
        """Return employment and education history"""

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
            logs.log_error(f"Error extracting work data: {e}")

        return extracted_work_data

    def extract_places(self) -> List[Dict[str, str]]:
        """Return history of places"""
        places = []
        unique_names = set()

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

                if name not in unique_names:
                    unique_names.add(name)
                    places.append({"name": name, "date": date})

        except Exception as e:
            logs.log_error(f"Error extracting localization data: {e}")

        return places

    def extract_contact_data(self) -> List[Dict[str, str]]:
        """Return phone number and email address"""
        data = []
        try:
            self._driver.get(f"{self._base_url}/{Config.CONTACT_URL}")

            main_div = self._driver.find_element(
                By.CSS_SELECTOR, "div.xyamay9.xqmdsaz.x1gan7if.x1swvt13"
            )
            span_elements = main_div.find_elements(
                By.CSS_SELECTOR,
                "span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u.x1yc453h[dir='auto']",
            )

            scraped_data = {}

            for span_element in span_elements:
                text = span_element.text

                # Checking for phone number
                phone_number_match = re.search(r"\b\d{3} \d{3} \d{3}\b", text)
                if phone_number_match:
                    scraped_data["phone_number"] = phone_number_match.group()

                # Checking for email address
                email_match = re.search(
                    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text
                )
                if email_match:
                    scraped_data["email"] = email_match.group()

            data.append(scraped_data)

        except Exception as e:
            logs.log_error(f"Error while extracting person data: {e}")

        return data

    def extract_family(self) -> List[Dict[str, str]]:
        """Return family members"""
        data = []
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
            logs.log_error(f"Error extracting family data: {e}")

        return data

    def work_and_education_pipeline(self) -> None:
        """
        Pipeline to run extract work and education data
        """
        try:
            rprint("[bold]Step 1 of 2 - Load cookies[/bold]")
            self._load_cookies_and_refresh_driver()

            if not person_repository.person_exists(self._user_id):
                person_repository.create_person(self._user_id)

            person_id = person_repository.get_person(self._user_id).id

            rprint("[bold]Step 2 of 2 - Extract work and education data[/bold]")
            scraped_data = self.extract_work_and_education()

            if not any(scraped_data):
                output.print_no_data_info()
                self._driver.quit()
                self.success = False
            else:
                output.print_data_from_list_of_dict(scraped_data)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(
                    self._user_id,
                    scraped_data,
                ).save()

                for data in scraped_data:
                    if not work_education_repository.work_and_education_exists(
                        data["name"], person_id
                    ):
                        work_education_repository.create_work_and_education(
                            data["name"], person_id
                        )

                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"Error running pipeline: {e}")
            rprint(f"An error occurred {e}")

    def localization_pipeline(self) -> None:
        """
        Pipeline to return localization data
        """
        try:
            rprint("[bold]Step 1 of 3 - Load cookies[/bold]")
            self._load_cookies_and_refresh_driver()

            rprint("[bold]Step 2 of 3 - Extract localization data[/bold]")
            if not person_repository.person_exists(self._user_id):
                person_repository.create_person(self._user_id)

            person_id = person_repository.get_person(self._user_id).id

            rprint("[bold]Step 3 of 3 - Extract localization data[/bold]")
            places = self.extract_places()

            if not any(places):
                output.print_no_data_info()
                self._driver.quit()
                self.success = False

            else:
                output.print_data_from_list_of_dict(places)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(
                    self._user_id,
                    places,
                ).save()

                for data in places:
                    if not place_repository.places_exists(
                        data["name"], data["date"], person_id
                    ):
                        place_repository.create_places(
                            data["name"], data["date"], person_id
                        )

                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"Error running pipeline: {e}")
            rprint(f"An error occurred {e}")

    def family_member_pipeline(self) -> None:
        """
        Pipeline to extract family members data
        """
        try:
            rprint("[bold]Step 1 of 2 - Load cookies[/bold]")
            self._load_cookies_and_refresh_driver()

            if not person_repository.person_exists(self._user_id):
                person_repository.create_person(self._user_id)

            person_id = person_repository.get_person(self._user_id).id

            rprint("[bold]Step 2 of 2 - Extract family members[/bold]")
            family_members = self.extract_family()

            if not any(family_members):
                output.print_no_data_info()
                self._driver.quit()
                self.success = False

            else:
                output.print_data_from_list_of_dict(family_members)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(
                    self._user_id,
                    family_members,
                ).save()

                for member in family_members:
                    if not family_member_repository.family_member_exists(
                        person_id, member["name"]
                    ):
                        family_member_repository.create_family_member(
                            member["name"],
                            member["relationship"],
                            member["url"],
                            person_id,
                        )

                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"Error running pipeline: {e}")
            rprint(f"An Error occurred {e}")

    def contact_pipeline(self) -> None:
        """
        Pipeline to extract phone number and email
        """
        try:
            rprint("[bold]Step 1 of 2 - Load cookies[/bold]")
            self._load_cookies_and_refresh_driver()

            rprint("[bold]Step 2 of 2 - Extract contact data[/bold]")
            scraped_data = self.extract_contact_data()

            if not any(scraped_data):
                output.print_no_data_info()
                self._driver.quit()
                self.success = False
            else:
                output.print_data_from_list_of_dict(scraped_data)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(
                    self._user_id,
                    scraped_data,
                ).save()

                if not person_repository.person_exists(self._user_id):
                    person_repository.create_person(
                        self._user_id,
                    )

                person = person_repository.get_person(self._user_id)

                for data in scraped_data:
                    if data["phone_number"]:
                        person_repository.update_phone_number(
                            person.id, data["phone_number"]
                        )

                    else:
                        rprint("[bold red]Phone number not found[/bold red]")

                    if data["email"]:
                        person_repository.update_email(person.id, data["email"])

                    else:
                        rprint("[bold red]Email not found[/bold red]")

                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"Error running pipeline: {e}")
            rprint(f"An error occurred {e}")

    def full_name_pipeline(self) -> None:
        """
        Pipeline to extract full name data
        """
        try:
            rprint("[bold]Step 1 of 2 - Load cookies[/bold]")
            self._load_cookies_and_refresh_driver()

            rprint("[bold]Step 2 of 2 - Extract full name[/bold]")
            full_name = self.extract_full_name()

            if not full_name:
                output.print_no_data_info()
                self._driver.quit()
                self.success = False

            else:
                output.print_string(full_name)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(
                    self._user_id,
                    full_name,
                ).save()

                if not person_repository.person_exists(self._user_id):
                    person_repository.create_person(self._user_id)

                # Update full name field in Person object
                person = person_repository.get_person(self._user_id)
                update_full_name = person_repository.update_full_name(
                    person.id, full_name
                )
                if update_full_name:
                    rprint("[bold green]Full name successfully updated[/bold green]")
                else:
                    rprint("[bold red]Full name not updated[/bold red]")

                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"Error running pipeline: {e}")
            rprint(f"An error occurred {e}")

    def pipeline(self) -> None:
        """
        Pipeline to run full script
        """
        try:
            rprint("[bold]Step 1 of 6 - Load cookies[/bold]")
            self._load_cookies_and_refresh_driver()

            rprint("[bold]Step 2 of 6 - Extract full name[/bold]")
            full_name = self.extract_full_name()

            if not full_name:
                output.print_no_data_info()
            else:
                output.print_string(full_name)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(
                    self._user_id,
                    full_name,
                ).save()

                if not person_repository.person_exists(self._user_id):
                    person_repository.create_person(self._user_id)

                person_id = person_repository.get_person(self._user_id).id

                update_full_name = person_repository.update_full_name(
                    person_id, full_name
                )
                if update_full_name:
                    rprint("[bold green]Full name successfully updated[/bold green]")
                else:
                    rprint("[bold red]Full name not updated[/bold red")

            rprint("[bold]Step 3 of 6 - Extract family members[/bold]")
            family_members = self.extract_family()

            if not any(family_members):
                output.print_no_data_info()
            else:
                output.print_data_from_list_of_dict(family_members)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(
                    self._user_id,
                    family_members,
                ).save()

                for member in family_members:
                    if not family_member_repository.family_member_exists(
                        person_id, member["name"]
                    ):
                        family_member_repository.create_family_member(
                            member["name"],
                            member["relationship"],
                            member["url"],
                            person_id,
                        )

            rprint("[bold]Step 4 of 6 - Extract localization data[/bold]")
            places = self.extract_places()

            if not any(places):
                output.print_no_data_info()
            else:
                output.print_data_from_list_of_dict(places)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(
                    self._user_id,
                    places,
                ).save()

                for data in places:
                    if not place_repository.places_exists(
                        data["name"], data["date"], person_id
                    ):
                        place_repository.create_places(
                            data["name"], data["date"], person_id
                        )

            rprint("[bold]Step 5 of 6 - Extract work and education data[/bold]")
            scraped_data = self.extract_work_and_education()

            if not any(scraped_data):
                output.print_no_data_info()
            else:
                output.print_data_from_list_of_dict(scraped_data)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(
                    self._user_id,
                    scraped_data,
                ).save()

                save_to_json.SaveJSON(
                    self._user_id,
                    scraped_data,
                ).save()

                for data in scraped_data:
                    if not work_education_repository.work_and_education_exists(
                        data["name"], person_id
                    ):
                        work_education_repository.create_work_and_education(
                            data["name"], person_id
                        )

            rprint("[bold]Step 6 of 6 - Extract phone number and email[/bold]")
            scraped_contact_data = self.extract_contact_data()

            if not any(scraped_contact_data):
                output.print_no_data_info()
            else:
                output.print_data_from_list_of_dict(scraped_contact_data)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(
                    self._user_id,
                    scraped_contact_data,
                ).save()

                for data in scraped_contact_data:
                    if data["phone_number"]:
                        person_repository.update_phone_number(
                            person_id, data["phone_number"]
                        )

                    else:
                        rprint("[bold red]Phone number not found[/bold red]")

                    if data["email"]:
                        person_repository.update_email(person_id, data["email"])

                    else:
                        rprint("[bold red]Email not found[/bold red]")

            self._driver.quit()
            self.success = True

        except Exception as e:
            logs.log_error(f"Error running pipeline: {e}")
            rprint(f"An Error occurred {e}")
