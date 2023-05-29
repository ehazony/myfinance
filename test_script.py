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
        self.plain_driver = selenium_api.get_selenium_driver(grid=False, headless=True)
        self.wire_driver = selenium_api.get_selenium_driver(grid=False, headless=True, wire=True)
        self.grid_driver = selenium_api.get_selenium_driver(grid=True, headless=True)

        self.plain_driver.implicitly_wait(10)
        self.wire_driver.implicitly_wait(10)
        self.grid_driver.implicitly_wait(10)

    def tearDown(self):
        """Stop web driver"""
        self.plain_driver.quit()
        self.wire_driver.quit()
        self.grid_driver.quit()

    def test_case_1_plain_driver(self):
        """Find and click top-left logo button with plain driver"""
        self._test_page_navigation(self.plain_driver, 'https://www.oursky.com/', 'header__logo')

    def test_case_1_wire_driver(self):
        """Find and click top-left logo button with wire driver"""
        self._test_page_navigation(self.wire_driver, 'https://www.oursky.com/', 'header__logo')

    def test_case_1_grid_driver(self):
        """Find and click top-left logo button with grid driver"""
        self._test_page_navigation(self.grid_driver, 'https://www.oursky.com/', 'header__logo')

    def test_case_2_plain_driver(self):
        """Find and click top-right Start your project button with plain driver"""
        self._test_page_navigation(self.plain_driver, 'https://www.oursky.com/', 'header__cta')

    def test_case_2_wire_driver(self):
        """Find and click top-right Start your project button with wire driver"""
        self._test_page_navigation(self.wire_driver, 'https://www.oursky.com/', 'header__cta')

    def test_case_2_grid_driver(self):
        """Find and click top-right Start your project button with grid driver"""
        self._test_page_navigation(self.grid_driver, 'https://www.oursky.com/', 'header__cta')

    def _test_page_navigation(self, driver, url, element_class):
        """General method for testing page navigation"""
        try:
            driver.get(url)
            el = driver.find_element(By.CLASS_NAME, element_class)
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplate)
    unittest.TextTestRunner(verbosity=2).run(suite)
