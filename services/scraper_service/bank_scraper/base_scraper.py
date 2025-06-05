import abc
import json

import requests

class Scraper:
    @abc.abstractmethod
    def get_transactions(self, start, end,credential,  *args, **kwargs):
        pass

    def get_with_requests(self, driver, url, headers, params):
        cookies = driver.get_cookies()
        s = requests.Session()
        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])
        # headers['user-agent'] = driver.execute_script("return navigator.userAgent;")
        response = s.get(url, headers=headers, params=params)
        return json.loads(response.text)

    def post_with_requests(self, driver, url, headers, data):
        cookies = driver.get_cookies()
        s = requests.Session()
        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])
        # headers['user-agent'] = driver.execute_script("return navigator.userAgent;")
        response = s.post(url, headers=headers, data=data)
        return json.loads(response.text)