"""
A simple selenium test example written by python
"""
import logging
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from bank_scraper import selenium_api


class TestTemplate(unittest.TestCase):
    """Include test cases on a given url"""

    def setUp(self):
        """Start web driver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        """Stop web driver"""
        self.driver.quit()

    def test_case_1(self):
        """Find and click top-left logo button"""
        try:
            self.driver.get('https://www.oursky.com/')
            el = self.driver.find_element(By.CLASS_NAME,'header__logo')
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_case_2(self):
        """Find and click top-right Start your project button"""
        try:
            self.driver.get('https://www.oursky.com/')
            el = self.driver.find_element(By.CLASS_NAME, "header__cta")
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplate)
    unittest.TextTestRunner(verbosity=2).run(suite)


class GoogleSearchTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()


    def test_driver(self):
        driver = selenium_api.get_selenium_driver(grid=False, headless=True)
        driver.implicitly_wait(10)
        self._google_search(driver)
        driver.quit()

    def test_wire(self):
        wire_driver = selenium_api.get_selenium_driver(grid=False, headless=True, wire=True)
        wire_driver.implicitly_wait(10)
        self._google_search(wire_driver)
        wire_driver.quit()

    def test_grid(self):
        logging.info("Testing grid")
        grid_driver = selenium_api.get_selenium_driver(grid=True, headless=True)
        grid_driver.implicitly_wait(10)
        self._google_search(grid_driver)
        grid_driver.quit()

    def _google_search(self,driver):
        driver.get("https://www.google.com")
        self.assertIn("Google", driver.title)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
