# Locators Cheatsheet

## Cel lokatora

Lokator powinien jednoznacznie wskazywać element i być odporny na drobne zmiany HTML.

## Selenium 4

```python
from selenium.webdriver.common.by import By

driver.find_element(By.ID, "my-text-id")
driver.find_element(By.NAME, "my-password")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
driver.find_element(By.XPATH, "//textarea[@name='my-textarea']")
driver.find_element(By.CLASS_NAME, "btn")
driver.find_element(By.TAG_NAME, "h1")
driver.find_element(By.LINK_TEXT, "About")
driver.find_element(By.PARTIAL_LINK_TEXT, "Selenium")
```

## Selenium 3

```python
driver.find_element_by_id("my-text-id")
driver.find_element_by_name("my-password")
driver.find_element_by_css_selector("button[type='submit']")
driver.find_element_by_xpath("//textarea[@name='my-textarea']")
driver.find_elements_by_css_selector(".form-control")
```

Ten styl jest historyczny. W nowych projektach używaj `find_element(By..., value)`.
W Selenium 4 metody `find_element_by_*` zostały usunięte, więc ich wywołanie
skończy się `AttributeError`.

## Rekomendowana kolejność wyboru

1. Stabilny atrybut testowy, np. `data-testid`, jeżeli aplikacja go ma.
2. `id`, jeżeli jest stabilne i czytelne.
3. `name`, szczególnie w formularzach.
4. CSS selector.
5. Krótki XPath względny, gdy CSS nie wystarcza.

## Czego unikać

- Absolutnych XPathów typu `/html/body/div[2]/div[1]/button`.
- Selektorów zależnych od kolejności elementów, jeżeli UI często się zmienia.
- Selektorów po tekście, który często trafia do tłumaczeń.
- Losowych klas generowanych przez frontend, np. `.css-1abc234`.
