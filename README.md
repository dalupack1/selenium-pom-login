# Selenium E2E Login Suite — Page Object Model

End-to-end automated login test suite built with **Python + Selenium WebDriver** using the **Page Object Model (POM)** design pattern. Tests run against [SauceDemo](https://www.saucedemo.com) — a public QA practice site.

## What's tested
- ✅ Successful login with valid credentials
- ✅ Login failure with invalid password
- ✅ Login failure with locked-out user
- ✅ Empty field validation
- ✅ Full checkout E2E flow (login → add to cart → checkout)
- ✅ Logout flow

## Tech stack
| Tool               | Purpose |
|--------------------|---|
| Python 3.13        | Language |
| Selenium WebDriver | Browser automation |
| PyTest             | Test runner |
| Allure             | HTML reports |
| Page Object Model  | Design pattern |
| ChromeDriver       | Browser driver |

## Project structure
```
01-selenium-pom-login/
├── pages/
│   ├── base_page.py          # Base class with shared methods
│   ├── login_page.py         # Login page object
│   ├── inventory_page.py     # Products page object
│   └── checkout_page.py      # Checkout page object
├── tests/
│   ├── conftest.py           # PyTest fixtures (driver setup/teardown)
│   ├── test_login.py         # Login test cases
│   └── test_checkout.py      # E2E checkout test cases
├── utils/
│   └── config.py             # Base URL, credentials, timeouts
├── requirements.txt
└── README.md
```

## Setup & run
```bash
# 1. Clone and install
git clone https://github.com/YOUR_USERNAME/01-selenium-pom-login.git
cd 01-selenium-pom-login
pip install -r requirements.txt

# 2. Run all tests
pytest tests/ -v

# 3. Run with Allure report
pytest tests/ -v --alluredir=allure-results
allure serve allure-results
```

## Sample output
```
tests/test_login.py::test_valid_login PASSED
tests/test_login.py::test_invalid_password PASSED
tests/test_login.py::test_locked_out_user PASSED
tests/test_login.py::test_empty_username PASSED
tests/test_checkout.py::test_full_checkout_flow PASSED
5 passed in 14.32s
```