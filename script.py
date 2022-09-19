import sys
import time

from bank_scraper.selenium_api import get_driver


def run_process(browser):
    browser.get('https://pricebackers.com/')
    time.sleep(5)
    return {'url': browser.current_url}


if __name__ == '__main__':
    browser = get_driver()
    try:
        data = run_process(browser)
        print(data)
    except Exception as e:
        raise e
    browser.quit()
    print(f'Finished!')
