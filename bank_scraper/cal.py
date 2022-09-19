import datetime
import time

from selenium.webdriver.common.by import By

from bank_scraper.selenium_api import get_selenium_driver


def get_transactions(start, end):
    # options = uc.ChromeOptions()
    # options.headless = True
    # options.add_argument('--headless')
    # driver = uc.Chrome(options=options)
    driver = get_selenium_driver()
    start_year_month = start.strftime('%m%Y')
    end_year_month = start.strftime('%m%Y')
    start_day = start.strftime('%-d')
    end_day = end.strftime('%-d')

    # driver = uc.Chrome()

    driver.get('https://www.cal-online.co.il/')
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'imglogin').click()

    fr = driver.find_element(By.XPATH, '//*[@allow="otp-credentials"]')
    driver.switch_to.frame(fr)
    time.sleep(2)
    driver.find_element(By.ID, 'regular-login').click()
    time.sleep(5)
    driver.find_element(By.ID, 'mat-input-2').send_keys('efhazony')
    driver.find_element(By.ID, 'mat-input-3').send_keys('cinnamon1')
    driver.find_elements(By.XPATH, "//button[contains(., ' כניסה ')]")[0].click()
    time.sleep(10)
    # driver.add_cdp_listener('Network.responseReceived', mylousyprintfunction)
    driver.get('https://services.cal-online.co.il/Card-Holders/SCREENS/Transactions/Transactions.aspx')
    driver.find_element(By.XPATH,
                        '//*[@id="ctl00_ContentTop_cboCardList_categoryList_updatePanelList"]/table/tbody/tr/td[1]/div/span[2]/div[5]/div').click()
    time.sleep(2)
    cards = driver.find_element(By.ID, 'ctl00_ContentTop_cboCardList_categoryList_pnlMain').find_elements(
        By.CSS_SELECTOR, 'a')
    driver.find_element(By.XPATH,
                        '//*[@id="ctl00_ContentTop_cboCardList_categoryList_updatePanelList"]/table/tbody/tr/td[1]/div/span[2]/div[5]/div').click()

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

    # הצג
    transactions = []
    for i, card in enumerate(cards):
        driver.find_element(By.XPATH,
                            '//*[@id="ctl00_ContentTop_cboCardList_categoryList_updatePanelList"]/table/tbody/tr/td[1]/div/span[2]/div[5]/div').click()
        time.sleep(2)

        driver.find_element(By.ID, 'ctl00_ContentTop_cboCardList_categoryList_pnlMain').find_elements(By.CSS_SELECTOR,
                                                                                                      'a')[i].click()
        time.sleep(1)
        driver.find_element(By.ID, 'ctl00_FormAreaNoBorder_FormArea_ctlSubmitRequest').click()

        time.sleep(5)

        trs = driver.find_elements(By.XPATH, '//*[@id="ctlMainGrid"]/tbody[1]/tr')
        for tr in trs:
            tds = tr.find_elements(By.XPATH, 'td')
            values = [td.text for td in tds]
            values = dict(zip(['date', 'name', 'value_total', 'value', 'info'], values))

        # go through pages
        while len(driver.find_elements(By.ID, 'ctl00_FormAreaNoBorder_FormArea_ctlGridPager_btnNext')) != 0:
            driver.find_element(By.ID, 'ctl00_FormAreaNoBorder_FormArea_ctlGridPager_btnNext').click()
            time.sleep(5)
            trs = driver.find_elements(By.XPATH, '//*[@id="ctlMainGrid"]/tbody[1]/tr')
            for tr in trs:
                tds = tr.find_elements(By.XPATH, 'td')
                values = [td.text for td in tds]
                values = dict(zip(['date', 'name', 'value_total', 'value', 'info'], values))
                transactions.append(values)

    for trans in transactions:
        value = trans['value'].replace('₪ ', '').replace(',', '')
        value_total = trans['value_total'].replace('₪ ', '').replace(',', '')
        trans['amount'] = float(value) if value else None
        trans['value_total'] = float(value_total) if value_total else None
        trans['date'] = datetime.datetime.strptime(trans['date'], '%d/%m/%y')
    driver.quit()
    return transactions


if __name__ == "__main__":
    end = datetime.datetime.now()
    start = datetime.datetime.now().replace(day=1)
    transactions = get_transactions(start, end)
    print(transactions)
