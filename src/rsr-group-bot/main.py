import logging
import os
from datetime import datetime

from alert.alert import Alert
from database.database import Database
from database.models.favorite import Favorite
from dotenv import load_dotenv
from logger.logger import Logger
from price_parser import Price
from selenium import webdriver
from selenium.webdriver.support.ui import Select


class RsrGroupBot:
    def __init__(self):
        load_dotenv()
        Logger()

        self.logger = logging.getLogger("logger")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.driverPath = os.getenv("CHROMEDRIVER_PATH")

        self.configureDriver()

    def compareFavorites(self, currentFavorites, dbFavorites):
        newFavorites = []
        favoritesToUpdate = []

        for currentFavorite in currentFavorites:
            found = False

            for dbFavorite in dbFavorites:
                if dbFavorite.part_number == currentFavorite.part_number:
                    found = True

                    if (
                        currentFavorite.available >= 0
                        and currentFavorite.available != dbFavorite.available
                    ):
                        self.logger.info(
                            f"Stock is different for favorite {currentFavorite.title}. Updating..."
                        )
                        dbFavorite.title = currentFavorite.title
                        dbFavorite.available = currentFavorite.available
                        dbFavorite.price = currentFavorite.price
                        dbFavorite.date_modified = datetime.utcnow

                        favoritesToUpdate.append(
                            {
                                "part_number": currentFavorite.part_number,
                                "title": currentFavorite.title,
                                "available": currentFavorite.available,
                                "price": currentFavorite.price,
                                "id": dbFavorite.id,
                                "current": True,
                            }
                        )
                        break

            if not found:
                self.logger.info(f"Favorite {currentFavorite.title} Not found. Adding...")
                newFavorites.append(currentFavorite)

        Favorite.add(newFavorites)
        Favorite.update(favoritesToUpdate)

        testOld = self.getOldFavorites(currentFavorites, dbFavorites)
        Favorite.update(testOld)

    def configureDriver(self):
        self.driver = webdriver.Chrome(self.driverPath)
        self.driver.implicitly_wait(5)

    def getFavorites(self):
        self.driver.find_element_by_id("dealer-my-favorites").click()

        perPageDropDown = Select(self.driver.find_element_by_name("PerPage"))
        perPageDropDown.select_by_value("100")

        favorites = []

        products = self.driver.find_elements_by_class_name("cue-datatable-row")

        for product in products:
            favorites.append(
                Favorite(
                    partNumber=product.find_element_by_css_selector(".product-sku span").text,
                    title=product.find_element_by_css_selector(".product-title a").text,
                    price=Price.fromstring(
                        product.find_element_by_class_name("product-price").text
                    ).amount_float,
                    available=int(
                        product.find_element_by_css_selector(
                            ".product-availability span"
                        ).text.split()[0]
                    ),
                )
            )

        return favorites

    def getOldFavorites(self, currentFavorites, dbFavorites):
        oldFavorites = []

        for dbFavorite in dbFavorites:
            found = False

            for currentFavorite in currentFavorites:
                if dbFavorite.part_number == currentFavorite.part_number:
                    found = True

                    break

            if not found:
                oldFavorites.append({"id": dbFavorite.id, "current": False})

        return oldFavorites

    def launch(self):
        self.login()

        favorites = self.getFavorites()
        favoritesDb = Favorite.get()

        self.compareFavorites(favorites, favoritesDb)

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
    database = Database()
    bot = RsrGroupBot()
    bot.launch()
    bot.quit()

    # Alert.sendText([])
    # Alert.sendEmail([])
