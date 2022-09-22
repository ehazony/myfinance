# import asyncio
import datetime
import json
import logging
import os
import time

import django
import requests

# from pyppeteer import launch
# from pyppeteer_stealth import stealth
from bank_scraper.base_scraper import Scraper

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")
django.setup()
from selenium.webdriver.common.by import By

from bank_scraper.selenium_api import get_selenium_driver

from myFinance import models
from django.contrib.auth.models import User


def _get_data(cookies, start_date, end_date):
    url = "https://start.telebank.co.il/Titan/gatewayAPI/lastTransactions/transactions/0142181635/ByDate"

    params = {"FromDate": start_date.strftime('%Y%m%d'), "ToDate": end_date.strftime('%Y%m%d'),
              "IsTransactionDetails": True, "IsFutureTransactionFlag": True,
              "IsEventNames": True, "IsCategoryDescCode": True}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
        'BusinessProcessID': 'OSH_LENTRIES_ALTAMIRA',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'If-Modified-Since': 'Mon, 26 Jul 1997 05:00:00 GMT',
        'Pragma': 'no-cache',
        'Referer': 'https://start.telebank.co.il/apollo/retail/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        # 'UUID': '0b719193-d869-4cf5-a352-8517d360714b',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'accountNumber': '0142181635',
        'language': 'HEBREW',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'site': 'retail'
    }

    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    response = s.get(url, headers=headers, params=params)
    return json.loads(response.text)


class DiscountScraper(Scraper):

    def get_transactions(self, start, end, username=None, password=None, user_id=None, *args, **kwargs):
        driver = get_selenium_driver(headless=True, grid=True)
        driver.get('https://start.telebank.co.il/login/#/LOGIN_PAGE')
        time.sleep(2)
        inputs = driver.find_elements(By.XPATH, '//input')
        inputs[0].send_keys(user_id)
        inputs[1].send_keys(password)
        inputs[2].send_keys(username)
        driver.find_element(By.XPATH, "//button[contains(., 'כניסה')]").click()
        time.sleep(5)
        transactions = []
        cookies = driver.get_cookies()
        driver.quit()

        data = _get_data(cookies, start, end)
        if type(data) == dict:
            data = [data]
        if data[0].get('Error') and data[0].get('Error').get('ReturnedCode') == 'RET010297':
            return transactions
        account_balance = data[0]['CurrentAccountLastTransactions']['CurrentAccountInfo']['AccountBalance']
        user = User.objects.get(username='efraim')
        models.AdditionalInfo.objects.update_or_create(user=user, value={'bank_balance': account_balance})

        for transaction in data[0]['CurrentAccountLastTransactions']['OperationEntry']:
            transactions.append({
                'date': datetime.datetime.strptime(transaction['OperationDate'], '%Y%m%d'),
                'name': transaction['OperationDescription'],
                'urn': transaction['Urn'],
                'amount': transaction['OperationAmount'] * -1,
                'bank': True

            })

        return transactions


# async def _get_transactions_data(start_date, end_date):
#     # setup
#     browser = await launch({'headless': True})
#     page = await browser.newPage()
#     await stealth(page)
#     # page size
#     await page.setViewport({'width': 1366, 'height': 768})
#
#     # go to site
#     await page.goto('https://start.telebank.co.il/login/#/LOGIN_PAGE')
#     time.sleep(2)
#     inputs = await page.xpath('//input')
#
#     await inputs[0].type("308078088")
#     await inputs[1].type("upandup92")
#     await inputs[2].type("Ef2020hz")
#
#     # await page.click('#send-code')
#     button = await page.xpath("//button[contains(., 'כניסה')]")
#     time.sleep(2)
#     await page.evaluate('el => el.click()', button[0])
#     time.sleep(5)
#     cookies = await page.cookies()
#     data = _get_data(cookies, start_date, end_date)
#
#     await browser.close()
#     return data


# def get_discount_transactions(start_date, end_date):
#     loop = asyncio.get_event_loop()
#     loop.set_debug(False)
#     transactions = []
#     data = loop.run_until_complete(asyncio.gather(_get_transactions_data(start_date, end_date)))
#     if data[0].get('Error') and data[0].get('Error').get('ReturnedCode') == 'RET010297':
#         return transactions
#     account_balance = data[0]['CurrentAccountLastTransactions']['CurrentAccountInfo']['AccountBalance']
#     user = User.objects.get(username='efraim')
#     models.AdditionalInfo.objects.update_or_create(user=user, value={'bank_balance': account_balance})
#
#     for transaction in data[0]['CurrentAccountLastTransactions']['OperationEntry']:
#         transactions.append({
#             'date': datetime.datetime.strptime(transaction['OperationDate'], '%Y%m%d'),
#             'name': transaction['OperationDescription'],
#             'urn': transaction['Urn'],
#             'amount': transaction['OperationAmount'] * -1,
#             'bank': True
#
#         })
#
#     return transactions


if __name__ == "__main__":
    e = datetime.datetime.now().replace(day=18)
    s = datetime.datetime.now().replace(day=1)
    t = time.time()
    data = get_discount_transactions(s, e)
    print(data)
    print('time:', str(time.time() - t))
