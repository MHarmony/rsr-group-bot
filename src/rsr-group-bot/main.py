import logging
import os

from dotenv import load_dotenv
from logger.logger import Logger
from price_parser import Price
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# from selenium.webdriver.support.ui import WebDriverWait


class RsrGroupBot:
    def __init__(self):
        load_dotenv()
        Logger()

        self.logger = logging.getLogger("logger")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.driverPath = os.getenv("CHROMEDRIVER_PATH")

        self.configureDriver()

    def configureDriver(self):
        self.driver = webdriver.Chrome(self.driverPath)
        self.driver.implicitly_wait(10)
        # self.wait = WebDriverWait(self.driver, 10)

    def getFavorites(self):
        self.driver.find_element_by_id("dealer-my-favorites").click()

        perPageDropDown = Select(self.driver.find_element_by_name("PerPage"))
        perPageDropDown.select_by_value("100")

        favorites = []

        products = self.driver.find_elements_by_class_name("cue-datatable-row")

        for product in products:
            favorites.append(
                {
                    "title": product.find_element_by_css_selector(".product-title a").text,
                    "available": int(
                        product.find_element_by_css_selector(
                            ".product-availability span"
                        ).text.split()[0]
                    ),
                    "price": Price.fromstring(
                        product.find_element_by_class_name("product-price").text
                    ).amount_float,
                }
            )

        return favorites

    def launch(self):
        self.login()

        favorites = self.getFavorites()

        for favorite in favorites:
            print(favorite)

    def login(self):
        self.driver.get("https://rsrgroup.com")
        self.driver.find_element_by_css_selector("#quick-login input[name=Login]").send_keys(
            self.username
        )
        self.driver.find_element_by_css_selector("#quick-login input[name=Password]").send_keys(
            self.password
        )
        self.driver.find_element_by_css_selector("#quick-login form").submit()

    def quit(self):
        self.driver.quit()


if __name__ == "__main__":
    bot = RsrGroupBot()
    bot.launch()
    bot.quit()
