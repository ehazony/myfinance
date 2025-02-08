# import asyncio
import datetime
import logging
import os
import time

import django

# from pyppeteer import launch
# from pyppeteer_stealth import stealth
from bank_scraper.base_scraper import Scraper
from telegram_bot import telegram_bot_api

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")
django.setup()
from selenium.webdriver.common.by import By

from bank_scraper.selenium_api import get_selenium_driver

URL = "https://start.telebank.co.il/Titan/gatewayAPI/lastTransactions/transactions/0142181635/ByLastYear"
URL_LOANS = 'https://start.telebank.co.il/Titan/gatewayAPI/onlineLoans/loansQuery/0142181635'
HEADERS = {
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
# must fill FromDate, ToDate
# PARAMS = {"FromDate": None, "ToDate": None,
#           "IsTransactionDetails": True, "IsFutureTransactionFlag": True,
#           "IsEventNames": True, "IsCategoryDescCode": True}
PARAMS = {
    'IsTransactionDetails': 'True',
    'IsFutureTransactionFlag': 'True',
    'IsEventNames': 'True',
    'IsCategoryDescCode': 'True'
}


class DiscountScraper(Scraper):
    COMPANY = 'DISCOUNT'

    def get_transactions(self, start, end, credential, username=None, password=None, user_id=None, headless=False,
                         grid=True, *args, **kwargs):
        driver = get_selenium_driver(headless=headless, grid=grid)
        try:
            driver.get('https://start.telebank.co.il/login/#/LOGIN_PAGE')
            time.sleep(2)
            inputs = driver.find_elements(By.XPATH, '//input')
            inputs[0].send_keys(user_id)
            inputs[1].send_keys(password)
            inputs[2].send_keys(username)
            driver.find_element(By.XPATH, "//button[contains(., 'כניסה')]").click()
            time.sleep(5)
            transactions = []

            if datetime.datetime.now() - start > datetime.timedelta(days=365):
                print('Cant get transaction that are older than a year')
                start = datetime.datetime.now() - datetime.timedelta(days=365)
                print('setting start date to:', start)

            data = self.get_with_requests(driver, URL, HEADERS, PARAMS)

            if type(data) == dict:
                data = [data]
            if data[0].get('Error') and data[0].get('Error').get('ReturnedCode') == 'RET010297':
                return transactions
            account_balance = data[0]['CurrentAccountLastTransactions']['CurrentAccountInfo']['AccountBalance']
            credential.additional_info[credential.ADDITIONAL_INFO_BALANCE] = account_balance
            s = self.get_with_requests(driver, URL_LOANS, HEADERS, PARAMS)
            loans = -s['LoansQuery']['Summary']['TotalBalance']

            credential.additional_info[credential.ADDITIONAL_INFO_LOANS] = loans
            credential.save()
        except Exception as e:
            telegram_bot_api.send_img(driver.get_screenshot_as_png())
            driver.quit()
            raise e
        driver.quit()
        for transaction in data[0]['CurrentAccountLastTransactions']['OperationEntry']:
            if end >= datetime.datetime.strptime(transaction['OperationDate'], '%Y%m%d') >= start:
                transactions.append({
                    'date': datetime.datetime.strptime(transaction['OperationDate'], '%Y%m%d'),
                    'name': transaction['OperationDescription'],
                    'identifier': transaction['OperationNumber'],
                    'value': transaction['OperationAmount'] * -1,
                    'bank': True

                })
