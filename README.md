# Selenium Mentee Cheatsheet

Edukacyjny projekt demonstracyjny dla osób uczących się automatyzacji testów frontendu w Pythonie.

Projekt pokazuje podstawy Selenium na dwóch ścieżkach:

- `selenium3_examples/` - historyczny styl Selenium 3, spotykany w starszych projektach.
- `selenium4_examples/` - aktualny styl Selenium 4, rekomendowany do nowych projektów.

To nie jest framework enterprise. To ma być czytelna ściąga: krótkie testy, proste Page Objecty i komentarze tylko tam, gdzie pomagają zrozumieć mechanizm albo różnicę między wersjami.

## Wymagania

- Python 3.10+
- Google Chrome
- ChromeDriver zgodny z lokalną wersją Chrome
- Dostęp do internetu, bo testy używają publicznych stron demonstracyjnych:
  - `https://www.selenium.dev/selenium/web/web-form.html`
  - `https://the-internet.herokuapp.com/`

## Windows / PowerShell / cmd

Komendy w tym README są pisane składnią bash (macOS / Linux). Jeżeli pracujesz
na Windowsie, składnia zależy od tego, czy używasz PowerShella czy klasycznego
Command Prompta (`cmd.exe`). Mapowanie 1:1:

| bash (macOS / Linux)                  | PowerShell (Windows)                       | cmd.exe (Windows)                            |
|---------------------------------------|--------------------------------------------|----------------------------------------------|
| `python3 -m venv .venv-selenium4`     | `py -3.10 -m venv .venv-selenium4`         | `py -3.10 -m venv .venv-selenium4`           |
| `source .venv-selenium4/bin/activate` | `.\.venv-selenium4\Scripts\Activate.ps1`   | `.venv-selenium4\Scripts\activate.bat`       |
| `export VAR=val`                      | `$env:VAR = "val"`                         | `set VAR=val`                                |
| `echo "$VAR"`                         | `echo $env:VAR`                            | `echo %VAR%`                                 |
| `chmod +x drivers/chromedriver`       | (pomiń — Windows tego nie wymaga)          | (pomiń — Windows tego nie wymaga)            |
| `drivers/chromedriver`                | `drivers\chromedriver.exe`                 | `drivers\chromedriver.exe`                   |
| `"$PWD/drivers/chromedriver"`         | `"$PWD\drivers\chromedriver.exe"`          | `"%CD%\drivers\chromedriver.exe"`            |
| `ls -l "$CHROMEDRIVER_PATH"`          | `Get-Item $env:CHROMEDRIVER_PATH`          | `dir "%CHROMEDRIVER_PATH%"`                  |

Jeżeli pracujesz w **Git Bash** (dostarczanym razem z Git for Windows), używaj
składni z kolumny bash, ale z dwoma wyjątkami: aktywacja venv to
`source .venv-selenium4/Scripts/activate` (nie `bin/activate`), a driver to
`chromedriver.exe`.

Dwie rzeczy, które łapią początkujących na Windowsie (niezależnie od shella):

1. Jeżeli używasz PowerShella i `Activate.ps1` zwróci błąd o execution policy,
   jednorazowo odblokuj skrypty dla swojego użytkownika:
   `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. W `cmd.exe` ten temat
   nie istnieje — `activate.bat` odpala się bez ceregieli.
2. `python` w świeżym Windowsie potrafi otworzyć zaślepkę Microsoft Store
   zamiast Pythona. Najpewniejszy jest `py -3.10` (launcher Pythona z
   python.org) — działa zarówno w PowerShellu, jak i w `cmd.exe`.

Driver w Selenium 3 nazywa się na Windowsie `chromedriver.exe`. `CHROMEDRIVER_PATH`
musi wskazywać konkretny plik z rozszerzeniem `.exe`, np.:

```powershell
# PowerShell
$env:CHROMEDRIVER_PATH = "$PWD\drivers\chromedriver.exe"
```

```bat
:: cmd.exe
set CHROMEDRIVER_PATH=%CD%\drivers\chromedriver.exe
```

W Selenium 4 zazwyczaj nic nie musisz robić — Selenium Manager sam pobierze
`chromedriver.exe`.

W PyCharm Community uruchamianie testów idzie przez wbudowany runner pytest, nie
przez shell, więc cała powyższa składnia jest tam nieistotna — wystarczy, że w
ustawieniach projektu wybrany jest interpreter z odpowiedniego venv. Jeżeli
korzystasz z okna "Terminal" w PyCharmie, sprawdź w jego ustawieniach, czy jest
to PowerShell czy `cmd.exe`, i dobierz składnię z odpowiedniej kolumny.

## Ważne: osobne środowiska

Selenium 3 i Selenium 4 to różne wersje tego samego pakietu `selenium`, dlatego najczytelniej uruchamiać je w osobnych virtualenvach.

## Instalacja dla Selenium 3

Selenium 3 nie ma Selenium Managera. Musisz ręcznie pobrać lokalny
`chromedriver` zgodny z wersją Chrome, a potem mieć go dostępnego w `PATH` albo
wskazać go przez `CHROMEDRIVER_PATH`.

> Uwaga o kompatybilności: `selenium==3.141.0` realnie współpracuje z Chrome / ChromeDriverem do mniej więcej wersji 114. Na świeżym Chrome 115+ pojawiają się błędy startu sesji albo niedopasowania protokołu. Jeżeli masz nowszego Chrome'a zainstalowanego systemowo, do ścieżki Selenium 3 użyj pinowanej pary Chrome + ChromeDriver z [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) (np. 114) i wskaż ją przez `CHROMEDRIVER_PATH`. Selenium 4 nie ma tego problemu.
>
> Sam `CHROMEDRIVER_PATH` to za mało, jeżeli systemowy Chrome jest nowszy: ChromeDriver 114 i tak uruchomi systemowego Chrome'a i sesja padnie. Musisz dodatkowo wskazać binarkę Chrome z tej samej paczki Chrome for Testing. W `selenium3_examples/conftest.py`, w funkcji `build_chrome_options()`, dorzuć linijkę: `options.binary_location = "/sciezka/do/chrome-for-testing/Google Chrome for Testing"`. To jest świadomy kompromis dydaktyczny — nie chcieliśmy chować tej zmiennej w jeszcze jednym env var, żeby mentee nie czytał dwóch poziomów konfiguracji naraz.

```bash
python3 -m venv .venv-selenium3
source .venv-selenium3/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-selenium3.txt
```

Najprostszy wariant projektowy:

```bash
mkdir -p drivers
# skopiuj pobrany plik chromedriver do: drivers/chromedriver
chmod +x drivers/chromedriver
export CHROMEDRIVER_PATH="$PWD/drivers/chromedriver"
```

Plik `drivers/chromedriver` jest ignorowany przez git. To lokalna binarka
narzędziowa, nie część kodu szkoleniowego.

Jeżeli trzymasz driver w innym miejscu:

```bash
export CHROMEDRIVER_PATH=/sciezka/do/chromedriver
```

### Selenium 3 nie startuje? Krótka checklista

1. Sprawdź aktywne środowisko: `python -c "import selenium; print(selenium.__version__)"` powinno pokazać `3.141.0`.
2. Sprawdź, czy `CHROMEDRIVER_PATH` wskazuje istniejący plik: `ls -l "$CHROMEDRIVER_PATH"`.
3. Sprawdź, czy driver ma prawo uruchomienia: `chmod +x "$CHROMEDRIVER_PATH"`.
4. Sprawdź zgodność wersji Chrome i ChromeDrivera. Dla tej ścieżki najlepiej użyć pary Chrome/ChromeDriver około wersji 114.
5. Jeżeli testy importują się w PyCharmie, ale nie w terminalu, uruchamiaj je przez `python -m pytest ...` z aktywnego virtualenv.

Uruchomienie testów Selenium 3:

```bash
python -m pytest selenium3_examples/tests
```

## Instalacja dla Selenium 4

Selenium 4 potrafi użyć Selenium Managera, który w nowszych wersjach automatycznie dobiera i pobiera driver przeglądarki.

```bash
python3 -m venv .venv-selenium4
source .venv-selenium4/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-selenium4.txt
```

Uruchomienie testów Selenium 4:

```bash
python -m pytest selenium4_examples/tests
```

Jeżeli chcesz wymusić konkretny ChromeDriver:

```bash
export CHROMEDRIVER_PATH=/sciezka/do/chromedriver
python -m pytest selenium4_examples/tests
```

## Skąd uruchamiać `pytest`

Najprościej uruchamiać testy z katalogu głównego repo, tam gdzie leży
`pytest.ini`. Projekt ma jednak też `pythonpath = .` w `pytest.ini` oraz pliki
`__init__.py` w katalogach przykładów, więc importy działają również przy
typowym uruchomieniu z terminala przez `python -m pytest ...`, a nie tylko z
konfiguracji PyCharma.

## Markery pytest

Każdy plik testowy jest oznaczony markerem (`selenium3` albo `selenium4`) — zarejestrowane w `pytest.ini`. Można dzięki temu uruchomić tylko jedną grupę:

```bash
python -m pytest -m selenium4
python -m pytest -m selenium3
```

Bez `-m` pytest puszcza wszystko, co znajdzie w `testpaths`.

## Skipowany test antywzorca

W `selenium3_examples/tests/test_waits.py` i `selenium4_examples/tests/test_waits.py` znajdziesz po jednym teście z `@pytest.mark.skip`. To nie jest popsuty test — to celowo pokazany **antywzorzec z `time.sleep`**, żeby mentee zobaczył, jak nie pisać oczekiwań. Output `pytest` pokaże go jako `skipped`, to jest oczekiwane.

## Mechanizm "skip drugiej wersji" w `conftest.py`

W obu `conftest.py` jest funkcja `pytest_collection_modifyitems`. To jest hook pytest — uruchamia się raz po zebraniu listy testów i sprawdza, którą wersję `selenium` masz aktywną w virtualenvie. Jeżeli aktywne jest Selenium 4, a próbujesz odpalić testy z `selenium3_examples/`, hook automatycznie skipuje je z czytelnym komunikatem (i odwrotnie). To jest "pytest-magic", **nie musisz rozumieć tego kodu, żeby używać projektu** — wystarczy że wiesz, czemu czasem widzisz `skipped`.

## Headless Chrome

Domyślnie testy otwierają normalne okno Chrome, co jest wygodne podczas nauki. Tryb headless można włączyć tak:

```bash
export HEADLESS=1
python -m pytest selenium4_examples/tests
```

## Różnice Selenium 3 vs Selenium 4 w skrócie

Selenium 3 pokazuje historyczne API:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")

driver = webdriver.Chrome(executable_path="chromedriver", options=options)
element = driver.find_element_by_css_selector("button")
```

Selenium 4 używa aktualnego API:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(options=options)
element = driver.find_element(By.CSS_SELECTOR, "button")
```

W Selenium 4 lokatory są jawnie przekazywane przez klasę `By`, a konfigurację ścieżki do drivera robi się przez `Service`.
W Selenium 4 metody `find_element_by_*` są usunięte, a `executable_path` nie jest
już obsługiwany w konstruktorze `webdriver.Chrome`.

## Rekomendowana kolejność nauki

1. Inicjalizacja drivera.
2. Nawigacja: `get`, `title`, `current_url`, `back`, `forward`, `refresh`.
3. `find_element` i `find_elements`.
4. Lokatory: ID, name, CSS, XPath, link text.
5. Akcje na elementach: `click`, `send_keys`, `clear`.
6. Odczyt stanu: `text`, `get_attribute`, `is_displayed`, `is_enabled`, `is_selected`.
7. `WebDriverWait`.
8. `expected_conditions`.
9. Typowe wyjątki Selenium.
10. Page Object Pattern.

## Struktura

```text
.
  README.md
  requirements-selenium3.txt
  requirements-selenium4.txt
  pytest.ini

  selenium3_examples/
    __init__.py
    conftest.py
    pages/
      __init__.py
      base_page.py
      example_page.py
    tests/
      __init__.py
      test_basic_browser.py
      test_find_elements.py
      test_waits.py
      test_error_handling.py

  selenium4_examples/
    __init__.py
    conftest.py
    pages/
      __init__.py
      base_page.py
      example_page.py
    tests/
      __init__.py
      test_basic_browser.py
      test_find_elements.py
      test_waits.py
      test_error_handling.py

  docs/
    selenium3_vs_4.md
    locators_cheatsheet.md
    waits_cheatsheet.md
    common_exceptions.md
```

## Dokumentacja

- `docs/selenium3_vs_4.md` - główne różnice między Selenium 3 i 4.
- `docs/locators_cheatsheet.md` - ściąga z lokatorów.
- `docs/waits_cheatsheet.md` - jawne czekanie i expected conditions.
- `docs/common_exceptions.md` - typowe wyjątki i sposoby reagowania.
