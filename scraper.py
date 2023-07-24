from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import logging
import pickle
from time import sleep
from typing import List, Dict
from py2neo import Graph, Node, Relationship
from main import Config

# Logging setup
logging.basicConfig(
    filename=Config.LOG_FILE_PATH,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Chrome configuration
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-default-apps")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
chrome_options.add_argument("--profile-directory=Default")


class FacebookScraper:
    """
    Scrape user's friends and their data
    """

    def __init__(self, user_id) -> None:
        self.config = Config()
        self.user_id = user_id
        self.base_url = f"https://www.facebook.com/{self.user_id}/friends"
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver = self.driver
        self.driver.get(self.base_url)
        self.cookie_term_css_selector = "._42ft._4jy0._al65._4jy3._4jy1.selected._51sy"
        self.wait = WebDriverWait(self.driver, 10)
        self.data = set()

    def load_cookies(self) -> None:
        """
        Load cookies with a log in session
        """
        try:
            self.driver.delete_all_cookies()
            with open(self.config.COOKIES_FILE_PATH, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
        except Exception as e:
            logging.error(f"Error loading cookies: {e}")

    def extract_scraped_user_data(self) -> Dict:
        """
        Extract scraped user data and return it as a dictionary
        """
        extracted_data = {}
        try:
            username_element = self.driver.find_element(
                By.CSS_SELECTOR, "h1.x1heor9g.x1qlqyl8.x1pd3egz.x1a2a7pz"
            )
            username = username_element.text.strip()
            url = f"https://www.facebook.com/{self.user_id}"
            extracted_data = {"username": username, "url": url}
        except Exception as e:
            logging.error(f"Error extracting scraped user data: {e}")
        return extracted_data

    def extract_friends_data(self) -> List[Dict[str, str]]:
        """
        Return a list of dictionaries with the usernames and the urls to the profile for every person in friends list
        """
        extracted_elements = []

        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a.x1i10hfl span")
            for element in elements:
                username = element.text.strip()
                url = element.find_element(By.XPATH, "..").get_attribute("href")
                if username == "":
                    continue
                element_data = {"username": username, "url": url}
                extracted_elements.append(element_data)

        except Exception as e:
            logging.error(f"Error extracting friends data: {e}")

        return extracted_elements

    def scroll_page(self) -> None:
        """
        Scrolls the page to load more friends from a list
        """
        try:
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            consecutive_scrolls = 0

            while consecutive_scrolls < self.config.MAX_CONSECUTIVE_SCROLLS:
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

                sleep(self.config.SCROLL_PAUSE_TIME)
                self.extract_friends_data()
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )

                if new_height == last_height:
                    consecutive_scrolls += 1
                else:
                    consecutive_scrolls = 0

                last_height = new_height
        except Exception as e:
            logging.error(f"Error occurred while scrolling: {e}")

    def save_data_to_neo4j(self, user_data) -> None:
        """
        Save data to Neo4j graph database
        """
        try:
            graph = Graph(
                uri=self.config.DATABASE_URL,
                user=self.config.GRAPH_DATABASE_USERNAME,
                password=self.config.GRAPH_DATABASE_PASSWORD,
            )
            user_node = Node(
                "User", username=user_data["username"], url=user_data["url"]
            )
            graph.create(user_node)

            for data in user_data["friends"]:
                friend_node = Node("User", username=data["username"], url=data["url"])
                graph.create(friend_node)
                relationship = Relationship(user_node, "FRIEND", friend_node)
                graph.create(relationship)

        except Exception as e:
            logging.error(f"Error occurred while saving data to Neo4j: {e}")

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            self.load_cookies()
            self.driver.refresh()
            self.scroll_page()
            sleep(5)
            user_data = self.extract_scraped_user_data()
            user_data["friends"] = self.extract_friends_data()
            self.save_data_to_neo4j(user_data)
        except Exception as e:
            logging.error(f"Error occurred while running the pipeline: {e}")
        finally:
            self.driver.quit()
