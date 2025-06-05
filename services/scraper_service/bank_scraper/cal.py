import datetime
import json
import os
import time

import django
import requests
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from telegram_bot import telegram_bot_api

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")
django.setup()
from selenium.webdriver.common.by import By
from dateutil import relativedelta

TIMEWAIT = 120
from bank_scraper.selenium_api import get_selenium_driver
from bank_scraper.base_scraper import Scraper
from dateutil.rrule import rrule, MONTHLY


class CalScraper(Scraper):

    def __init__(self):
        self.COMPANY = 'CAL'

    def get_transactions(self, start, end, credential, username=None, password=None, grid=True, *args, **kwargs):
        # options = uc.ChromeOptions()
        # options.headless = True
        # options.add_argument('--headless')
        # driver = uc.Chrome(options=options)
        if type(start) == datetime.date:
            start = datetime.datetime(start.year, start.month, start.day, 0, 0, 0)
        if type(end) == datetime.date:
            end = datetime.datetime(end.year, end.month, end.day, 0, 0, 0)
        driver = get_selenium_driver(grid=False, headless=False, wire=True)  # headless must be True for remote
        try:

            # driver = uc.Chrome()

            driver.get('https://www.cal-online.co.il/')
            time.sleep(0.7)
            WebDriverWait(driver, TIMEWAIT).until(EC.element_to_be_clickable((By.CLASS_NAME, "logindesktop"))).click()
            # driver.find_element(By.CLASS_NAME, 'imglogin').click()

            fr = driver.find_element(By.XPATH, '//*[@allow="otp-credentials"]')
            driver.switch_to.frame(fr)
            time.sleep(2)
            driver.find_element(By.ID, 'regular-login').click()
            time.sleep(1)
            driver.find_element(By.ID, 'mat-input-2').send_keys(username)
            driver.find_element(By.ID, 'mat-input-3').send_keys(password)
            driver.find_elements(By.XPATH, "//button[contains(., ' כניסה ')]")[0].click()
            time.sleep(10)
            # driver.add_cdp_listener('Network.responseReceived', mylousyprintfunction)
            # WebDriverWait(drivezr, 40).until(EC.element_to_be_clickable((By.CLASS_NAME,
            #                                                             "butn-medium-dark"))).click()
            driver.get('https://digital-web.cal-online.co.il/transactions')
            url = 'https://api.cal-online.co.il/Transactions/api/transactionsDetails/getCardTransactionsDetails'
            time.sleep(3)
            headers = payload = {}
            for request in driver.requests:
                if request.url == url:
                    headers = request.headers
                    payload = request._body
                    response = request.response
                    from seleniumwire.utils import decode

                    body = json.loads(
                        decode(response.body, response.headers.get('Content-Encoding', 'identity')).decode('utf-8'))
                    bill_date = datetime.datetime.strptime(
                        body['result']['bankAccounts'][0]['debitDates'][0]['toPurchaseDate'].split('T')[0], '%Y-%m-%d')
            date_range = list(rrule(MONTHLY, dtstart=start, until=bill_date))
            payload = json.loads(payload)
            transactions = []
            for date in date_range:
                payload['month'] = str(date.month)
                payload['year'] = str(date.year)
                response = requests.request("POST", url, headers=headers, json=payload)
                transactions.extend(
                    json.loads(response.text)['result']['bankAccounts'][0]['debitDates'][0]['transactions'])

            for trn in transactions:
                trn['date'] = datetime.datetime.strptime(trn['trnPurchaseDate'].split('T')[0], '%Y-%m-%d')
                trn['value'] = trn['trnAmt']
                trn['name'] = trn['merchantName']
                trn['identifier'] = trn['trnIntId']

        except Exception as e:
            telegram_bot_api.send_img(driver.get_screenshot_as_png())
            driver.quit()
            raise e
        driver.quit()
        return list(filter(lambda t: start <= t['date'] <= end, transactions))

    def _get_months_to_scrape(self, start, end, bill_date):
        months = [bill_date.strftime('%m%Y')]
        previous_bill_date = bill_date - relativedelta.relativedelta(months=1)
        while start < previous_bill_date:
            months.append(previous_bill_date.strftime('%m%Y'))
            previous_bill_date = previous_bill_date - relativedelta.relativedelta(months=1)
        return months

    def _set_search_month_by_date_billed(self, driver, month):
        driver.find_element(By.ID, 'ctl00_FormAreaNoBorder_FormArea_clndrDebitDateScope_Button').click()  # open picker
        time.sleep(1)
        driver.find_element(By.ID,  # select month date
                            'ctl00_FormAreaNoBorder_FormArea_clndrDebitDateScope_OptionList').find_element(
            By.XPATH, 'li[@value="{}"]'.format(month)).click()

    def _set_search_date_by_date_transaction_created(self, driver, start, end):
        start_year_month = start.strftime('%m%Y')
        end_year_month = start.strftime('%m%Y')
        start_day = start.strftime('%-d')
        end_day = end.strftime('%-d')

        driver.find_element(By.ID, 'ctl00_FormAreaNoBorder_FormArea_rdoTransactionDate').click()
        time.sleep(2)
        # Start
        driver.find_element(By.ID, 'ctl00_FormAreaNoBorder_FormArea_ctlDateScopeStart_ctlMonthYearList_Button').click()
        time.sleep(1)
        driver.find_element(By.ID,
                            'ctl00_FormAreaNoBorder_FormArea_ctlDateScopeStart_ctlMonthYearList_OptionList').find_element(
            By.XPATH, 'li[@value="{}"]'.format(start_year_month)).click()

        driver.find_element(By.ID, 'ctl00_FormAreaNoBorder_FormArea_ctlDateScopeStart_ctlDaysList_Button').click()
        time.sleep(1)
        driver.find_element(By.ID,
                            'ctl00_FormAreaNoBorder_FormArea_ctlDateScopeStart_ctlDaysList_OptionList').find_element(
            By.XPATH, 'li[@value="{}"]'.format(start_day)).click()
        # End
        driver.find_element(By.ID, 'ctl00_FormAreaNoBorder_FormArea_ctlDateScopeEnd_ctlMonthYearList_Button').click()
        time.sleep(1)
        driver.find_element(By.ID,
                            'ctl00_FormAreaNoBorder_FormArea_ctlDateScopeEnd_ctlMonthYearList_OptionList').find_element(
            By.XPATH, 'li[@value="{}"]'.format(end_year_month)).click()

        driver.find_element(By.ID, 'ctl00_FormAreaNoBorder_FormArea_ctlDateScopeEnd_ctlDaysList_Button').click()
        time.sleep(1)
        driver.find_element(By.ID,
                            'ctl00_FormAreaNoBorder_FormArea_ctlDateScopeEnd_ctlDaysList_OptionList').find_element(
            By.XPATH, 'li[@value="{}"]'.format(end_day)).click()
