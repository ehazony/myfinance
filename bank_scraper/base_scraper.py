import abc
import json

import requests


class Scraper:
    @abc.abstractmethod
    def get_transactions(self, start, end,  *args, **kwargs):
        pass

    def get_with_requests(self, driver, url, headers, params):
        cookies = driver.get_cookies()
        s = requests.Session()
        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])
        response = s.get(url, headers=headers, params=params)
        return json.loads(response.text)