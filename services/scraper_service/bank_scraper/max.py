# import asyncio
# import json
#
# from pyppeteer import launch
# import time
# from pyppeteer_stealth import stealth
import datetime
import json
import os
import time
import urllib

import django
from dateutil import relativedelta

from telegram_bot import telegram_bot_api

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")
django.setup()

from selenium.webdriver.common.by import By

from bank_scraper.base_scraper import Scraper
from bank_scraper.selenium_api import get_selenium_driver


URL = "https://www.max.co.il/api/registered/getHomePageData?v=V3.90-HF.29.53"

PAYLOAD = {}
HEADERS = {
    'authority': 'www.max.co.il',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'he-IL,he;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': '_cls_v=ca188a15-0920-4488-a76d-13d70f8f9486; _cls_s=7c51f72a-e44c-4064-8d3e-663b3add75a1:0; NotAuthOnline40V3=0kzcq5wgyzfk3an52relf3ms; ct1=c=3cb47725-b28b-4568-a600-b597c761a3ad&e=9/23/2024 4:01:24 PM; _ga=GA1.3.1339245075.1663938082; _gid=GA1.3.1323956009.1663938082; _fbp=fb.2.1663938081703.1570969999; ELOQUA=GUID=7D3F5ADF77CF47FB9D49354A6A200C95; _tt_enable_cookie=1; _ttp=b86e3e00-68c9-406b-986b-48b325baea00; BiometricPopup=NeedToShow%3Dtrue%3BLastShow%3DFri%2C%2023%20Sep%202022%2013%3A01%3A21%20GMT; __za_cds_19763054=%7B%22data_for_campaign%22%3A%7B%22country%22%3A%22IL%22%2C%22language%22%3A%22HE%22%2C%22ip%22%3A%22109.67.123.156%22%2C%22start_time%22%3A1663938081000%2C%22session_groups%22%3A%7B%222189%22%3A%7B%22campaign_Id%22%3A%2254472%22%7D%2C%222244%22%3A%7B%22campaign_Id%22%3A%2255766%22%7D%2C%222245%22%3A%7B%22campaign_Id%22%3A%2255778%22%7D%2C%222293%22%3A%7B%22campaign_Id%22%3A%2257083%22%7D%7D%7D%7D; __za_cd_19763054=%7B%22visits%22%3A%22%5B1663938082%5D%22%2C%22campaigns_status%22%3A%7B%2243680%22%3A1663938082%7D%7D; __za_19763054=%7B%22sId%22%3A58224088%2C%22dbwId%22%3A%221%22%2C%22sCode%22%3A%22efa45ffe7a22014d03b93ddae7dfcd82%22%2C%22sInt%22%3A5000%2C%22aLim%22%3A2000%2C%22asLim%22%3A1000%2C%22na%22%3A1%2C%22td%22%3A1%2C%22ca%22%3A%221%22%7D; ct2=t=95f1d6e3-7191-3131-e010-368383729fdf&it=2&i=KXkKDqad3I7QsPq9mVWsKnY0wV7Ss7ckd6gYW7Ng0OI=; ct3=pit=2&pi=KXkKDqad3I7QsPq9mVWsKnY0wV7Ss7ckd6gYW7Ng0OI=; .AUTHONLINE40V3=EFCF896457F48A538E7596A2572C915F2C701639E17612AFE452D5F068E5AA8D0F9125A67E920EFDED813E79CFFD017ACA0C11E219E4CF98E8D419C64035B9AC5C4DD7EA2B04D43BD5E3A8E63A2E45A992E1F91512B97ED253FBD98DAAF542C18460DB6AE042CBE499C751F1; BenefitDetailsV2=lHuYB5444bOCwBjCCjB6JGwsVLrJQKzYo74vf7GPJSNfXoZHPZVMcj79CG9iI7ZS0Drg6v9Ay3ehgrg8PuyfTn14xGUX1uwwGagRCt4RCIHOC1RVe1BPLni0MJjBu9ormQk8v46pCba9oHfTOIF%2fCQ%3d%3d; _vid_t=U4y5+wIOTicATMMDqwS58R5PBr0pP9RSsNeLys//9XQ47hu7IKUwzOc4VNKJG/mKwUMVo0YcV62GuIKbcj3IhJyIWZPwLGA=; ctFingerPrint=L4ttOENHnuTX1mojBPCT; .AUTHONLINE40V3=981F077B5ABD82154699E523F0CE26C7D327B84CEC0D216A08DF6E1CF09F37897CE23E00FAFD39510D545A1E3306EAB518790BF355B103C7AC1F4B5952ECB7EBD25AB3C0127BFA3863A777F805D837B417F3E81D942D0C54D5D0EBDCBE5CCB37D21114058A8F33064ADB0B3F; NotAuthOnline40V3=',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}



class MaxScraper(Scraper):
    COMPANY = 'MAX'

    def get_transactions(self, start, end, credential, username=None, password=None, grid=True, headless = True, *args, **kwargs):

        driver = get_selenium_driver(grid=grid, headless = headless)  # driver = uc.Chrome(enable_cdp_events=True)
        try:
            driver.get('https://www.max.co.il/homepage/welcome')
            time.sleep(2)

            driver.execute_script("arguments[0].click();", driver.find_element(By.CLASS_NAME, 'go-to-personal-area'))
            driver.execute_script("arguments[0].click();", driver.find_element(By.ID, 'login-password-link'))
            driver.find_element(By.XPATH, '//*[@formcontrolname="username"]').send_keys(username)
            driver.find_element(By.XPATH, '//*[@formcontrolname="password"]').send_keys(password)
            driver.execute_script("arguments[0].click();", driver.find_elements(By.XPATH, "//button[@id='send-code']")[1])
            time.sleep(5)
            driver.get('https://www.max.co.il/transaction-details/personal')
            time.sleep(3)
            print('trying')
            home_page_data = self.get_with_requests(driver, URL, HEADERS, PAYLOAD)
            current_month_total_some = 0
            for x in home_page_data['Result']['UserCards']['Summary']:
                if x['CurrencySymbol'] == '₪':
                    current_month_total_some = x['ActualDebitSum']
            card_details = [{'last_digits': card['Last4Digits'],
                             'next_bill': card['CycleSummary'][0]['Date'],
                             'debit': card['CycleSummary'][0]['ActualDebitSum']} for card in
                            home_page_data['Result']['UserCards']['Cards'] if len(card['CycleSummary']) > 0]

            credential.additional_info[credential.ADDITIONAL_INFO_BALANCE] = float(current_month_total_some) * -1
            credential.additional_info['card_details'] = card_details
            credential.save()

            url = 'https://www.max.co.il/api/registered/transactionDetails/getTransactionsAndGraphs?filterData={}&firstCallCardIndex=-1null&v=V3.85-HF.21'.format(
                urllib.parse.unquote(
                    json.dumps(
                        {"userIndex": -1, "cardIndex": -1, "monthView": False, "date": start.strftime('%Y-%m-%d'),
                         "dates": {"startDate": start.strftime('%Y-%m-%d'), "endDate": end.strftime('%Y-%m-%d')},
                         "bankAccount": {"bankAccountIndex": -1, "cards": None}})))
            transactions_response = self.get_with_requests(driver, url, HEADERS, PAYLOAD)
        except Exception as e:
            telegram_bot_api._send_img(driver.get_screenshot_as_png())
            driver.quit()
            raise e
        driver.quit()
        trans = []
        for t in transactions_response['result']['transactions']:
            name = t['merchantName']
            date = datetime.datetime.strptime(t['purchaseDate'], '%Y-%m-%dT%X')

            amount = t['actualPaymentAmount']
            arn = t['arn']
            comment = t.get('comments')
            plan = t['planName']
            if plan in ['תשלומים', 'קרדיט']:
                current, last = comment.split(' ')[1], comment.split(' ')[3]
                for i in range(int(last) - int(current)):
                    trans.append(
                        {'name': name, 'date': date + relativedelta.relativedelta(months=i + 1), 'value': amount,
                         'identifier': arn + '_' + str(int(current) + i + 1),
                         'comment': str(int(current) + i + 1) + ' מתוך ' + last,
                         'plan': plan})

            trans.append(
                {'name': name, 'date': date, 'value': amount, 'identifier': arn, 'comment': comment, 'plan': plan})
        return trans

