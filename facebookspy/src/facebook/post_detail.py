import pickle
from typing import List, Dict, Optional, Any

from rich import print as rprint
from selenium import webdriver
from selenium.webdriver.common.by import By

from .scraper import Scraper
from ..config import Config
from ..logs import Logs
from ..repository import person_repository, post_repository
from ..utils import output

logs = Logs()


class PostDetail(Scraper):
    """
    Scrape detail of Post
    """

    def __init__(self, url: str) -> None:
        super().__init__()
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self._url = url
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

            elif number_of_likes is None:
                try:
                    result = stats_div.find_element(
                        By.CSS_SELECTOR, "span.xt0b8zv.x1e558r4"
                    ).text
                except Exception as e:
                    logs.log_error(f"Error occurred while getting number of likes {e}")

        if post:
            try:
                likes_container = self._driver.find_element(
                    By.CSS_SELECTOR, "span.xt0b8zv.x2bj2ny.xrbpyxo.xl423tq"
                )
                result = likes_container.find_element(
                    By.CSS_SELECTOR, "span.x1e558r4"
                ).text
            except Exception as e:
                logs.log_error(f"Error occurred while getting number of likes {e}")

        if not self._check_number_is_int(result):
            return 0
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

        if post:
            try:
                url_element = self._driver.find_element(
                    By.CSS_SELECTOR,
                    "a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f",
                )
                result = url_element.find_element(By.TAG_NAME, "span").text
            except Exception as e:
                logs.log_error(f"Error occurred while getting author {e}")

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

        if post:
            try:
                content_element = self._driver.find_element(
                    By.CSS_SELECTOR,
                    "div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.x126k92a",
                )
                result = content_element.text
            except Exception as e:
                logs.log_error(f"Error occurred while getting content {e}")

        return result

    @staticmethod
    def image_url_list_to_dict(image_urls: List[str] = None) -> Dict[str, str]:
        image_urls_dict = {}
        for image_url in image_urls:
            image_urls_dict[image_url] = image_url
        return image_urls_dict

    def scrape_post_data(self) -> List[Dict[str, Any]]:
        """Scrape data from post
        Content, url, number of likes, comments and shares
        """
        data = []
        number_of_likes = 0
        image_url = []
        content = ""
        author = ""

        post = False
        photo = False

        try:
            self._driver.get(self._url)
            self._load_cookies()
            self._driver.refresh()

            if "post" in self._url:
                post = True
            if "photo" in self._url:
                photo = True

            number_of_likes = self.scrape_number_of_likes(post, photo)
            author = self.scrape_author(post, photo)
            image_url = self.scrape_image_url(post, photo)
            content = self.scrape_content(post, photo)
            # print(f"Number of likes: {number_of_likes}")
            # print(f"Content: {content}")
            # print(f"Image url: {image_url}")
            # print(f"Author: {author}")
            data.append(
                {
                    "number_of_likes": int(number_of_likes),
                    "content": content,
                    "image_url": self.image_url_list_to_dict(image_url),
                    "author": author,
                    "url": self._url,
                }
            )

        except Exception as e:
            logs.log_error(f"Error occurred while loading post detail page: {e}")

        return data


def pipeline(name: str = None, post_url: str = None):
    if name:
        if not person_repository.person_exists(name):
            print(
                "This person does not exist in database, at first you should scrape post urls"
            )
            return

        person_object = person_repository.get_person(name)
        posts = post_repository.get_posts(person_object.id)

        if not posts:
            rprint("This person does not have any posts!")
            return

        for post in posts:
            if "pages" in post.url:
                continue

            scraper = PostDetail(post.url)
            scraped_data = scraper.scrape_post_data()

            if not any(scraped_data):
                output.print_no_data_info()
            else:
                output.print_list(scraped_data)
                post_repository.mark_post_as_scraped(post.id)

                for data in scraped_data:
                    post_repository.create_post(
                        person_id=person_object.id,
                        url=data["url"],
                        number_of_likes=data["number_of_likes"],
                        image_urls=data["image_url"],
                        content=data["content"],
                        author=data["author"],
                    )

    if post_url:
        if "pages" in post_url:
            rprint("Invalid post url")
            return

        scraper = PostDetail(post_url)
        scraped_data = scraper.scrape_post_data()

        if not any(scraped_data):
            output.print_no_data_info()
        else:
            output.print_list(scraped_data)

            if not person_repository.person_exists("Anonymous"):
                person_repository.create_person(
                    facebook_id="Anonymous",
                )

            person_object = person_repository.get_person("Anonymous")

            for data in scraped_data:
                post_repository.create_post(
                    url=data["url"],
                    number_of_likes=data["number_of_likes"],
                    image_urls=data["image_url"],
                    content=data["content"],
                    author=data["author"],
                    person_id=person_object.id,  # Anonymous user
                )

                created_post = post_repository.get_post_by_url(data["url"])
                post_repository.mark_post_as_scraped(created_post.id)
