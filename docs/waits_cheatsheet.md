# Waits Cheatsheet

## Dlaczego czekanie jest ważne

Frontend działa asynchronicznie. Element może istnieć w DOM, ale jeszcze nie być widoczny albo klikalny. Dlatego test powinien czekać na konkretny warunek, a nie na arbitralną liczbę sekund.

## Dobry wzorzec

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

wait = WebDriverWait(driver, 10)
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button")))
button.click()
```

## Częste expected conditions

- `presence_of_element_located` - element jest w DOM.
- `visibility_of_element_located` - element jest w DOM i jest widoczny.
- `element_to_be_clickable` - element jest widoczny i włączony.
- `url_contains` - adres strony zawiera oczekiwany fragment.
- `title_contains` - tytuł strony zawiera oczekiwany fragment.
- `staleness_of` - poprzedni element został odłączony od DOM.
- `text_to_be_present_in_element` - element zawiera oczekiwany tekst.
- `invisibility_of_element_located` - loader, modal albo overlay zniknął.
- `alert_is_present` - pojawił się alert JavaScript.
- `number_of_windows_to_be` - otworzyła się oczekiwana liczba okien lub kart.

## Czego nie robić

```python
import time

time.sleep(5)
```

`sleep` spowalnia testy i nie rozwiązuje problemu stabilności. Jeżeli aplikacja odpowie po 6 sekundach, test nadal będzie losowo padał. Jeżeli odpowie po 0.5 sekundy, test niepotrzebnie czeka.

## Kiedy `sleep` jest akceptowalny

Rzadko: do demonstracji, debugowania lokalnego albo bardzo krótkiego obejścia problemu animacji. Nie powinien być głównym mechanizmem synchronizacji testów.
