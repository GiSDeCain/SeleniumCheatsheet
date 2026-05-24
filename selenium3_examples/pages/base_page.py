"""Small BasePage for Selenium 3 examples."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


DEFAULT_TIMEOUT = 10


class BasePage:
    """Common browser actions shared by simple Page Objects.

    This file intentionally uses Selenium 3-only find_element_by_* methods.
    In Selenium 4 those methods are removed and raise AttributeError.
    """

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    # @property pozwala wywołać te metody bez nawiasów: `page.title` zamiast
    # `page.title()`. Dzięki temu z zewnątrz wyglądają jak zwykłe pola obiektu,
    # mimo że pod spodem są funkcjami. To wygodny idiom Pythona —
    # można to traktować po prostu jako "metoda do odczytu, którą wołasz bez ()".
    @property
    def title(self):
        return self.driver.title

    @property
    def current_url(self):
        return self.driver.current_url

    def find_by_css(self, selector):
        # Selenium 3 historical style. In Selenium 4 use find_element(By.CSS_SELECTOR, selector).
        return self.driver.find_element_by_css_selector(selector)

    def find_all_by_css(self, selector):
        # Selenium 3 historical style. In Selenium 4 use find_elements(By.CSS_SELECTOR, selector).
        return self.driver.find_elements_by_css_selector(selector)

    def wait_until_visible_by_css(self, selector):
        return self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )

    def wait_until_clickable_by_css(self, selector):
        return self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
