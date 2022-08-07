import undetected_chromedriver as uc
from selenium import webdriver


def get_selenium_driver():
    # options = uc.ChromeOptions()
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--headless')
    options.headless = True
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver
