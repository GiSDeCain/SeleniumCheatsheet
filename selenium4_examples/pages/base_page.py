"""Small BasePage for Selenium 4 examples."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


DEFAULT_TIMEOUT = 10


class BasePage:
    """Common browser actions shared by simple Page Objects."""

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    # @property pozwala wywołać te metody bez nawiasów: `page.title` zamiast
    # `page.title()`. Dzięki temu z zewnątrz wyglądają jak zwykłe pola obiektu,
    # mimo że pod spodem są funkcjami. To wygodny idiom Pythona — początkujący
    # może to traktować po prostu jako "metoda do odczytu, którą wołasz bez ()".
    @property
    def title(self):
        return self.driver.title

    @property
    def current_url(self):
        return self.driver.current_url

    # `locator` to krotka w stylu (By.ID, "my-text-id"). Gwiazdka `*locator`
    # rozpakowuje krotkę na osobne argumenty, więc:
    #   self.driver.find_element(*locator)
    # jest równoznaczne z:
    #   self.driver.find_element(By.ID, "my-text-id")
    # To standardowy idiom Page Objectów w Selenium 4.
    def find(self, locator):
        return self.driver.find_element(*locator)

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def wait_until_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))
