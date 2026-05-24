"""Selenium 4 examples of common Selenium exceptions."""

import pytest
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium4_examples.pages.example_page import (
    PAGE_HEADING,
    SUBMIT_BUTTON,
    WEB_FORM_URL,
)


pytestmark = pytest.mark.selenium4


def test_no_such_element_exception_when_locator_does_not_match(driver):
    driver.get(WEB_FORM_URL)

    with pytest.raises(NoSuchElementException):
        driver.find_element(By.ID, "missing-element-id")


def test_timeout_exception_when_wait_condition_is_not_met(driver):
    driver.get(WEB_FORM_URL)

    with pytest.raises(TimeoutException):
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "missing-element-id"))
        )


def test_stale_element_reference_after_page_refresh(driver):
    driver.get(WEB_FORM_URL)
    heading = driver.find_element(*PAGE_HEADING)

    driver.refresh()

    # Po refresh DOM jest budowany od nowa. Zmienna `heading` wciąż wskazuje
    # na starą referencję, której już nie ma — pierwsza próba odczytu rzuci wyjątek.
    # Reakcja w prawdziwym teście: znaleźć element ponownie po zmianie DOM.
    with pytest.raises(StaleElementReferenceException):
        _ = heading.text


def test_element_click_intercepted_when_overlay_covers_button(driver):
    driver.get(WEB_FORM_URL)
    button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(SUBMIT_BUTTON)
    )

    # The overlay simulates a common UI problem: modal, banner or loader covering the target.
    # UWAGA dydaktyczna: `driver.execute_script(...)` wstrzykuje kod JavaScript w
    # przeglądarkę. Robimy to TYLKO po to, żeby deterministycznie odtworzyć
    # sytuację "coś przykryło przycisk". W normalnych testach Selenium to nie
    # jest wzorzec, którym warto się posługiwać — nie kopiuj tej techniki do
    # swoich testów. Twoje prawdziwe testy mają korzystać z UI tak, jak robi to
    # użytkownik (klik, wpisz, poczekaj na warunek).
    driver.execute_script(
        """
        const overlay = document.createElement('div');
        overlay.id = 'training-overlay';
        overlay.style.position = 'fixed';
        overlay.style.inset = '0';
        overlay.style.zIndex = '999999';
        overlay.style.background = 'rgba(0, 0, 0, 0.01)';
        document.body.appendChild(overlay);
        """
    )

    try:
        with pytest.raises(ElementClickInterceptedException):
            button.click()
    finally:
        driver.execute_script("document.getElementById('training-overlay')?.remove();")
