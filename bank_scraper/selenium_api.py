import os
import time

import chromedriver_autoinstaller


from seleniumwire import webdriver as seleniumwire
from selenium import webdriver
import logging
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium_stealth import stealth
logging.getLogger('seleniumwire').setLevel(logging.WARNING)
from finance import settings


def get_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--window-size=1920,1080")
    # options.add_argument('--headless')
    # options.headless = True

    # initialize driver
    driver = webdriver.Remote(
        command_executor='http://18.216.183.173:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME, options=options)
    # driver = webdriver.Chrome(options=options)
    return driver

def create_grid_driver(options):
    # Check if we're inside a Docker container
    # if 'HOSTNAME' in os.environ: # dosent work on docker linux
    #     grid_url = 'http://host.docker.internal:4444/wd/hub'
    # else:
    #     grid_url = settings.GRID_ENDPOINT  # replace with your setting variable
    grid_url = settings.GRID_ENDPOINT

    driver = webdriver.Remote(
        command_executor=grid_url,
        desired_capabilities=DesiredCapabilities.CHROME, options=options)

    # Selenium Wire options
    # wire_options = {
    #     'addr': '127.0.0.1'
    # }
    # Create a new instance of the Google Chrome driver
    # driver = seleniumwire.Remote(
    #     command_executor=grid_url,
    #     desired_capabilities=desired_cap,
    #     seleniumwire_options=wire_options
    # )

    return driver
def get_selenium_driver(grid=True, headless = True, wire = False):
    # options = uc.ChromeOptions()
    if wire:
        driver = seleniumwire
    else:
        driver = webdriver
    options = driver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    if headless:
        options.add_argument('--headless')
        options.headless = True
    if grid:

        driver = create_grid_driver(options)
    else:
        chromedriver_autoinstaller.install()
        driver = driver.Chrome(options=options)
    # driver.implicitly_wait(10)
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
    return driver




def test_selenium_chrome(driver):
    try:
        # Setup ChromeDriver
        webdriver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=webdriver_service)

        # Open a webpage
        driver.get("http://www.google.com")

        # Check if title of the opened page is correct
        assert "Google" in driver.title

        # Close the browser
        driver.quit()

        print("Selenium Chrome test passed.")
    except Exception as e:
        print("Selenium Chrome test failed.")
        print(f"Exception: {e}")




# from seleniumwire import webdriver  # Import from seleniumwire
# from seleniumwire.utils import decode
     # for request in driver.requests:
#         if request.response and 'application/json' in request.response.headers['Content-Type']:
#             print('#######################################')
#             print(
#                 request.url,
#                 request.response.status_code,
#                 request.response.headers['Content-Type'],
#                 decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
#             )

def run_process(browser):
    browser.get('https://pricebackers.com/')
    time.sleep(5)
    return {'url': browser.current_url}


if __name__ == '__main__':
    browser = get_selenium_driver()
    try:
        data = run_process(browser)
        print(data)
    except Exception as e:
        raise e
    browser.quit()
    print(f'Finished!')
