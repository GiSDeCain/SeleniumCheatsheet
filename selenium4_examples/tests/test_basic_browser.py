"""Selenium 4 basics: opening pages and browser navigation."""

import pytest

from selenium4_examples.pages.example_page import THE_INTERNET_URL, WEB_FORM_URL


pytestmark = pytest.mark.selenium4


def test_can_open_page_and_read_title_and_url(driver):
    driver.get(WEB_FORM_URL)

    assert "Web form" in driver.title
    assert WEB_FORM_URL in driver.current_url


def test_can_use_back_forward_and_refresh(driver):
    driver.get(THE_INTERNET_URL)
    start_url = driver.current_url

    driver.get(WEB_FORM_URL)
    assert WEB_FORM_URL in driver.current_url

    driver.back()
    # Porównanie przez `in` zamiast `==`, bo serwer może dopisać/zmienić trailing slash
    # albo zrobić redirect — porównanie literalne bywa niestabilne.
    assert start_url in driver.current_url

    driver.forward()
    assert WEB_FORM_URL in driver.current_url

    driver.refresh()
    assert "Web form" in driver.title
