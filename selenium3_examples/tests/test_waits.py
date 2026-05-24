"""Selenium 3 waits: WebDriverWait and expected_conditions."""

import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium3_examples.pages.example_page import (
    SUBMIT_BUTTON_CSS,
    TEXT_INPUT_ID,
    WEB_FORM_URL,
    ExamplePage,
)


pytestmark = pytest.mark.selenium3


def test_can_wait_until_element_is_visible(driver):
    page = ExamplePage(driver)
    page.open_web_form()

    # Tu kuszące byłoby napisać `time.sleep(2)` przed znalezieniem elementu,
    # ale to antywzorzec — patrz test_anti_pattern_time_sleep_instead_of_wait
    # niżej i `docs/waits_cheatsheet.md`.
    text_input = page.wait.until(
        EC.visibility_of_element_located((By.ID, TEXT_INPUT_ID))
    )

    assert text_input.is_displayed()


def test_can_wait_until_element_is_clickable(driver):
    page = ExamplePage(driver)
    page.open_web_form()

    submit_button = page.wait_until_clickable_by_css(SUBMIT_BUTTON_CSS)

    assert submit_button.is_enabled()


def test_can_wait_until_url_changes_after_submit(driver):
    driver.get(WEB_FORM_URL)

    wait = WebDriverWait(driver, 10)
    driver.find_element_by_id(TEXT_INPUT_ID).send_keys("wait example")
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, SUBMIT_BUTTON_CSS))
    ).click()

    wait.until(EC.url_contains("submitted-form.html"))
    assert "submitted-form.html" in driver.current_url


@pytest.mark.skip(
    reason="ANTYWZORZEC: time.sleep zamiast WebDriverWait. Pokazany dydaktycznie. "
    "Zdejmij @skip lokalnie, żeby zobaczyć działanie, ale nie wzoruj się na tym."
)
def test_anti_pattern_time_sleep_instead_of_wait(driver):
    """Pokazuje, dlaczego `time.sleep` to zły mechanizm synchronizacji.

    Dwa problemy naraz:
    1. Jeśli strona odpowie wolniej niż założony sleep — test losowo padnie.
    2. Jeśli strona odpowie szybciej — test bez powodu marnuje czas.

    WebDriverWait + expected_conditions czeka dokładnie tyle, ile trzeba,
    i kończy w momencie spełnienia warunku.
    """
    driver.get(WEB_FORM_URL)

    # Sztywny sleep "na oko". Działa albo nie, zależnie od tego, jak akurat
    # zachowa się sieć i przeglądarka.
    time.sleep(2)

    text_input = driver.find_element_by_id(TEXT_INPUT_ID)
    assert text_input.is_displayed()

    # Wariant poprawny — czeka dokładnie tyle, ile trzeba, i tylko na to, na czym nam zależy:
    #     WebDriverWait(driver, 10).until(
    #         EC.visibility_of_element_located((By.ID, TEXT_INPUT_ID))
    #     )
