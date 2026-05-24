# Selenium 3 vs Selenium 4

## Cel

Ten dokument pokazuje różnice, które mentee najczęściej zobaczy przy przechodzeniu ze starszego projektu Selenium 3 do nowszego Selenium 4.

## Inicjalizacja Chrome

Selenium 3:

```python
from selenium import webdriver

driver = webdriver.Chrome(executable_path="chromedriver")
```

`executable_path` to historyczny styl. W starszych projektach jest częsty, ale w Selenium 4 został zastąpiony przez `Service`.
W Selenium 4.10+ argument `executable_path` został usunięty, więc stary snippet
rzuci `TypeError`, jeśli uruchomisz go w środowisku Selenium 4.

Selenium 4 z Selenium Managerem:

```python
from selenium import webdriver

driver = webdriver.Chrome()
```

Selenium 4 z jawną ścieżką do drivera:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service("/path/to/chromedriver"))
```

## Lokatory

Selenium 3:

```python
driver.find_element_by_id("login")
driver.find_element_by_css_selector("button[type='submit']")
driver.find_elements_by_css_selector(".item")
```

Selenium 4:

```python
from selenium.webdriver.common.by import By

driver.find_element(By.ID, "login")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
driver.find_elements(By.CSS_SELECTOR, ".item")
```

Metody `find_element_by_*` i `find_elements_by_*` nie są tylko przestarzałe.
W Selenium 4 zostały usunięte i kończą się `AttributeError`.

## Czekanie

Mechanizm `WebDriverWait` i `expected_conditions` wygląda podobnie w obu wersjach:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

wait = WebDriverWait(driver, 10)
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button")))
```

## Częste gotche migracji 3 -> 4

- `desired_capabilities` przenoś do `options.set_capability(...)`.
- Logi Chrome konfiguruj przez capability w options, np. `goog:loggingPrefs`.
- Stare przełączanie okien `driver.switch_to_window(...)` zastąp przez
  `driver.switch_to.window(...)`.
- `executable_path=...` zastąp przez `Service(...)` albo pozwól Selenium
  Managerowi dobrać driver automatycznie.
- `find_element_by_*` zastąp przez `find_element(By..., value)`.

## Praktyczna rekomendacja

- Ucz się Selenium 4 jako stylu docelowego.
- Czytaj Selenium 3, żeby rozumieć starsze projekty.
- Nie mieszaj Selenium 3 i 4 w jednym virtualenvie.
- Nie używaj `time.sleep()` jako podstawowego sposobu czekania.
- Trzymaj lokatory w Page Objectach, żeby testy były krótkie i czytelne.
