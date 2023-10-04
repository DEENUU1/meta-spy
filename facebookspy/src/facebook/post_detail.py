import pickle
from typing import List, Dict, Tuple, Optional

from rich import print as rprint
from selenium import webdriver
from selenium.webdriver.common.by import By

from .scraper import Scraper
from ..config import Config
from ..logs import Logs
from ..repository import person_repository, post_repository
from ..cli import output
from selenium.webdriver.support.ui import WebDriverWait


logs = Logs()


class PostDetail(Scraper):
    """
    Scrape detail of Post
    """

    def __init__(self, user_id: str) -> None:
        super().__init__()
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self._user_id = user_id
        self.success = False

    @property
    def is_pipeline_successful(self) -> bool:
        """Check if pipeline is success"""
        return self.success

    def _load_cookies(self) -> None:
        """Load cookies with log in session"""
        try:
            self._driver.delete_all_cookies()
            with open(Config.COOKIES_FILE_PATH, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    try:
                        self._driver.add_cookie(cookie)
                    except Exception as e:
                        logs.log_error(f"An Error occurred adding cookies {e}")
                        rprint(f"An Error occurred while adding cookies {e}")

        except Exception as e:
            logs.log_error(f"An Error occurred while loading cookies: {e}")
            rprint(f"An Error occurred while loading cookies {e}")

    @staticmethod
    def _extract_number(text: str) -> Optional[int]:
        """Extract number from string
        2 comments -> 2
        102 shares -> 102
        """
        parts = text.split(" ", 1)
        if len(parts) > 0 and parts[0].isdigit():
            return int(parts[0])
        else:
            return None

    @staticmethod
    def _check_number_is_int(text) -> bool:
        """Check if number is integer"""
        try:
            int(text)
            return True
        except ValueError:
            return False

    def scrape_number_of_likes(
        self, post: bool = False, image: bool = False
    ) -> Optional[int]:
        result = 0

        if image:
            stats_div = self._driver.find_element(
                By.CSS_SELECTOR,
                "div.x6s0dn4.xi81zsa.x78zum5.x6prxxf.x13a6bvl.xvq8zen.xdj266r.xktsk01.xat24cr.x1d52u69.x889kno.x4uap5.x1a8lsjc.xkhd6sd.xdppsyt",
            )
            number_of_likes = stats_div.find_element(
                By.CSS_SELECTOR, "span.xt0b8zv.x1e558r4"
            ).text
            if number_of_likes is None:
                try:
                    result = stats_div.find_element(
                        By.CSS_SELECTOR, "span.x1e558r4"
                    ).text
                except Exception as e:
                    logs.log_error(f"Error occurred while getting number of likes {e}")
                    rprint(f"Error occurred while getting number of likes {e}")

            elif number_of_likes is None:
                try:
                    result = stats_div.find_element(
                        By.CSS_SELECTOR, "span.xt0b8zv.x1e558r4"
                    ).text
                except Exception as e:
                    logs.log_error(f"Error occurred while getting number of likes {e}")
                    rprint(f"Error occurred while getting number of likes {e}")

        if post:
            likes_container = self._driver.find_element(
                By.CSS_SELECTOR, "span.xt0b8zv.x2bj2ny.xrbpyxo.xl423tq"
            )
            try:
                result = likes_container.find_element(
                    By.CSS_SELECTOR, "span.x1e558r4"
                ).text
            except Exception as e:
                logs.log_error(f"Error occurred while getting number of likes {e}")
                rprint(f"Error occurred while getting number of likes {e}")

            return result

    def scrape_author(self, post, image) -> Optional[str]:
        result = None

        if image:
            try:
                author_div = self._driver.find_element(
                    By.CSS_SELECTOR,
                    "span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u",
                )
                result = author_div.text
            except Exception as e:
                logs.log_error(f"Error occurred while getting author {e}")
                rprint(f"Error occurred while getting author {e}")

        if post:
            try:
                url_element = self._driver.find_element(
                    By.CSS_SELECTOR,
                    "a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f",
                )
                result = url_element.find_element(By.TAG_NAME, "span").text
            except Exception as e:
                logs.log_error(f"Error occurred while getting author {e}")
                rprint(f"Error occurred while getting author {e}")

        return result

    def scrape_image_url(self, post, image) -> List[Optional[str]]:
        result = []

        if image:
            try:
                img_element = self._driver.find_element(
                    By.CSS_SELECTOR, "img.x85a59c.x193iq5w.x4fas0m.x19kjcj4"
                )
                img_url = img_element.get_attribute("src")
                result.append(img_url)
            except Exception as e:
                logs.log_error(f"Error occurred while getting image url {e}")
                rprint(f"Error occurred while getting image url {e}")

        if post:
            try:
                images = self._driver.find_elements(
                    By.CSS_SELECTOR,
                    "img.x1ey2m1c.xds687c.x5yr21d.x10l6tqk.x17qophe.x13vifvy.xh8yej3",
                )
                for image in images:
                    result.append(image.get_attribute("src"))
            except Exception as e:
                logs.log_error(f"Error occurred while getting image url {e}")
                rprint(f"Error occurred while getting image url {e}")

        return result

    def scrape_content(self, post, image) -> Optional[str]:
        result = None

        if image:
            try:
                text_div = self._driver.find_elements(
                    By.CSS_SELECTOR,
                    "span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u",
                )
                result = text_div[1].text
            except Exception as e:
                logs.log_error(f"Error occurred while getting content {e}")
                rprint(f"Error occurred while getting content {e}")

        if post:
            try:
                content_element = self._driver.find_element(
                    By.CSS_SELECTOR,
                    "div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.x126k92a",
                )
                result = content_element.text
            except Exception as e:
                logs.log_error(f"Error occurred while getting content {e}")
                rprint(f"Error occurred while getting content {e}")

        return result

    def scrape_post_data(self, url: str) -> List[Dict]:
        """Scrape data from post
        Content, url, number of likes, comments and shares
        """
        data = []
        number_of_likes = 0
        image_url = ""
        content = ""
        author = ""

        post = False
        image = False

        try:
            self._driver.get(url)
            self._load_cookies()
            self._driver.refresh()

            if "post" in url:
                post = True
            if "image" in url:
                image = True

            number_of_likes = self.scrape_number_of_likes(post, image)
            author = self.scrape_author(post, image)
            image_url = self.scrape_image_url(post, image)
            content = self.scrape_content(post, image)

            data.append(
                {
                    "number_of_likes": int(number_of_likes),
                    "content": content,
                    "image_url": image_url,
                    "author": author,
                }
            )

        except Exception as e:
            logs.log_error(f"Error occurred while loading post detail page: {e}")

        return data

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            # person_object = person_repository.get_person(self._user_id)
            # posts = post_repository.get_posts(person_object.id)

            # for data in posts:
            scraped_data = self.scrape_post_data("")
            print(scraped_data)
            # if not any(scraped_data):
            #     output.print_no_data_info()
            #     self._driver.quit()
            #     self.success = True
            # else:
            #     output.print_data_from_list_of_dict(scraped_data)
            # post_repository.mark_post_as_scraped(data.id)

            # for scraped_item in scraped_data:
            #     post_repository.create_post(
            #         person_id=person_object.id,
            #         url="", #data.url,
            #         number_of_likes=scraped_item.get("number_of_likes", 0),
            #         number_of_shares=scraped_item.get("number_of_shares", 0),
            #         number_of_comments=scraped_item.get(
            #             "number_of_comments", 0
            #         ),
            #         content=scraped_item.get("content", ""),
            #     )

            self._driver.quit()
            self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
