import datetime
import os
import time

import django
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")
django.setup()
from selenium.webdriver.common.by import By
from dateutil import relativedelta

from bank_scraper.selenium_api import get_selenium_driver
from bank_scraper.base_scraper import Scraper


class CalScraper(Scraper):

    def __init__(self):
        self.COMPANY = 'CAL'

    def get_transactions(self, start, end, credential, username=None, password=None, grid=True, *args, **kwargs):
        # options = uc.ChromeOptions()
        # options.headless = True
        # options.add_argument('--headless')
        # driver = uc.Chrome(options=options)
        if type(start) == datetime.date:
            start = datetime.datetime(start.year, start.month, start.day)
        if type(end) == datetime.date:
            start = datetime.datetime(end.year, end.month, end.day)
        driver = get_selenium_driver(grid=False)
        try:

            # driver = uc.Chrome()

            driver.get('https://www.cal-online.co.il/')
            time.sleep(0.7)
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, "imglogin"))).click()
            # driver.find_element(By.CLASS_NAME, 'imglogin').click()

            fr = driver.find_element(By.XPATH, '//*[@allow="otp-credentials"]')
            driver.switch_to.frame(fr)
            time.sleep(2)
            driver.find_element(By.ID, 'regular-login').click()
            time.sleep(1)
            driver.find_element(By.ID, 'mat-input-2').send_keys(username)
            driver.find_element(By.ID, 'mat-input-3').send_keys(password)
            driver.find_elements(By.XPATH, "//button[contains(., ' כניסה ')]")[0].click()
            # time.sleep(10)
            # driver.add_cdp_listener('Network.responseReceived', mylousyprintfunction)
            next_debit_sum = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.ID, "lblNextDebitSum"))).text
            next_bill_date_str = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.ID, "lblNextDebitDate"))).text
            next_bill_date = datetime.datetime.strptime(next_bill_date_str, '%d/%m/%Y')
            # next_debit_sum = driver.find_element(By.ID, 'lblNextDebitSum').text
            credential.additional_info[credential.ADDITIONAL_INFO_BALANCE] = float(next_debit_sum) * -1
            credential.save()
            driver.get('https://services.cal-online.co.il/Card-Holders/SCREENS/Transactions/Transactions.aspx')
            driver.find_element(By.XPATH,
                                '//*[@id="ctl00_ContentTop_cboCardList_categoryList_updatePanelList"]/table/tbody/tr/td[1]/div/span[2]/div[5]/div').click()
            time.sleep(2)
            cards = driver.find_element(By.ID, 'ctl00_ContentTop_cboCardList_categoryList_pnlMain').find_elements(
                By.CSS_SELECTOR, 'a')
            driver.find_element(By.XPATH,
                                '//*[@id="ctl00_ContentTop_cboCardList_categoryList_updatePanelList"]/table/tbody/tr/td[1]/div/span[2]/div[5]/div').click()

            months = self._get_months_to_scrape(start, end, next_bill_date)
            transactions = []
            for month in months:
                temp_current_bill_date = datetime.datetime.strptime(month, '%m%Y')
                temp_current_last_bill_date = temp_current_bill_date - relativedelta.relativedelta(months=1)
                temp_bill_day = temp_current_bill_date.day
                self._set_search_month_by_date_billed(driver, month)
                for i in range(len(cards)):
                    current_transactions = []
                    driver.find_element(By.XPATH,
                                        '//*[@id="ctl00_ContentTop_cboCardList_categoryList_updatePanelList"]/table/tbody/tr/td[1]/div/span[2]/div[5]/div').click()
                    time.sleep(2)

                    driver.find_element(By.ID, 'ctl00_ContentTop_cboCardList_categoryList_pnlMain').find_elements(
                        By.CSS_SELECTOR,
                        'a')[i].click()
                    time.sleep(1)
                    driver.find_element(By.ID, 'ctl00_FormAreaNoBorder_FormArea_ctlSubmitRequest').click()

                    time.sleep(5)

                    trs = driver.find_elements(By.XPATH, '//*[@id="ctlMainGrid"]/tbody[1]/tr')

                    # first page
                    for tr in trs:
                        tds = tr.find_elements(By.XPATH, 'td')
                        values = [td.text for td in tds]
                        values = dict(zip(['date', 'name', 'value_total', 'value', 'info'], values))
                        current_transactions.append(values)

                    # go through pages
                    while len(driver.find_elements(By.ID, 'ctl00_FormAreaNoBorder_FormArea_ctlGridPager_btnNext')) != 0:
                        driver.find_element(By.ID, 'ctl00_FormAreaNoBorder_FormArea_ctlGridPager_btnNext').click()
                        time.sleep(5)
                        trs = driver.find_elements(By.XPATH, '//*[@id="ctlMainGrid"]/tbody[1]/tr')
                        for tr in trs:
                            tds = tr.find_elements(By.XPATH, 'td')
                            values = [td.text for td in tds]
                            values = dict(zip(['date', 'name', 'value_total', 'value', 'info'], values))
                            current_transactions.append(values)

                    # format data
                    for trans in current_transactions:
                        value = trans['value'].replace('₪ ', '').replace(',', '')
                        value_total = trans['value_total'].replace('₪ ', '').replace(',', '')
                        trans['amount'] = float(value) if value else None
                        trans['deal_total'] = float(value_total) if value_total and '$' not in value_total else None
                        trans['date'] = datetime.datetime.strptime(trans['date'], '%d/%m/%y')
                        # set date to be in this month billing period
                        if not temp_current_last_bill_date <= trans['date'] <= temp_current_bill_date:
                            trans['date'] = temp_current_last_bill_date.replace(day=trans['date'].day) \
                                if temp_bill_day <= trans['date'].day\
                                else temp_current_bill_date.replace(day=trans['date'].day)

                    transactions.extend(current_transactions)
        except Exception as e:
            driver.quit()
            raise e
        driver.quit()
        return filter(lambda t: start <= t['date'] <= end, transactions)

    def _get_months_to_scrape(self, start, end, bill_date):
        months = [str(bill_date.month) + str(bill_date.year)]
        previous_bill_date = bill_date - relativedelta.relativedelta(months=1)
        while start < previous_bill_date:
            months.append(previous_bill_date.strftime('%m%Y'))
            previous_bill_date = previous_bill_date - relativedelta.relativedelta(months=1)
        return months

    def _set_search_month_by_date_billed(self, driver, month):
        driver.find_element(By.ID, 'ctl00_FormAreaNoBorder_FormArea_clndrDebitDateScope_Button').click()  # open picker
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
