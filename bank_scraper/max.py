# import asyncio
# import json
#
# from pyppeteer import launch
# import time
# from pyppeteer_stealth import stealth
import datetime
import json
import time
import urllib

from django.contrib.auth.models import User
from selenium.webdriver.common.by import By

from bank_scraper.base_scraper import Scraper
from bank_scraper.selenium_api import get_selenium_driver
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carScraping.settings")
# django.setup()
# async def intercept_network_request(request):
#     # print(request.url)
#     # await request.continue_()
#     # if "application/json" in request.headers.get("content-type", ""):
#     r = await request.json()
#     print(request.url)
#     print(r)
# async def main():
#     # driver = uc.Chrome()
#     # driver.get('https://nowsecure.nl')
#
#     # setup
#     browser = await launch({'headless': False})
#     page = await browser.newPage()
#     # await page.setUserAgent(
#     #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
#     await stealth(page, ['user_agent_override'])
#     # await stealth(page, )
#     # page size
#     await page.setViewport({'width': 1600, 'height': 796})
#
#     # go to site
#     try:
#         await page.goto('https://www.max.co.il/homepage/welcome')
#         time.sleep(2)
#         button = await page.xpath('//a[@class="go-to-personal-area"]')
#         await page.click('.go-to-personal-area')
#         await page.click('#login-password-link')
#         time.sleep(2)
#         # el = await page.querySelector('[formcontrolname="username"]')
#         # await page.evaluate( 'el => el.value = "EFRAIMHAZONY@gmail.com"', el)
#         # el = await page.querySelector('[formcontrolname="password"]')
#         # await page.evaluate( 'el => el.value = "Cinnamongirl1"', el)
#         await page.type('[formcontrolname="username"]', "EFRAIMHAZONY@gmail.com")
#         # await page.click('#send-code')
#         await page.type('[formcontrolname="password"]', "Cinnamongirl1")
#         button = await page.xpath("//button[@id='send-code']")
#         await page.evaluate( 'el => el.click()', button[1])
#         time.sleep(5)
#         button = await page.xpath("//a[contains(., 'פירוט חיובים')]")
#         await page.setRequestInterception(value=True)
#         page.on('response', lambda req: asyncio.ensure_future(intercept_network_request(req)))
#         # await page.evaluate( 'el => el.click()', button[1])
#         response = await page.goto('https://www.max.co.il/transaction-details/personal')
#         # response = await page.goto('https://www.max.co.il/api/registered/transactionDetails/getTransactionsAndGraphs?filterData={%22userIndex%22:-1,%22cardIndex%22:-1,%22monthView%22:true,%22date%22:%222022-05-30%22,%22dates%22:{%22startDate%22:%220%22,%22endDate%22:%220%22},%22bankAccount%22:{%22bankAccountIndex%22:-1,%22cards%22:null}}&firstCallCardIndex=-1null&v=V3.85-HF.21')
#         # await asyncio.sleep(10)
#         # time.sleep(10)
#         await page.waitForNavigation({'waitUntil': "networkidle0"})
#         # response = await response.json()
#         # print(response)
#         await browser.close()
#         return None# response
#     except:
#         await browser.close()
# # https://www.max.co.il/api/registered/transactionDetails/getTransactionsAndGraphs?filterData=&firstCallCardIndex=-1null&v=V3.85-HF.21
# if __name__ == '__main__':
#
#     loop = asyncio.get_event_loop()
#     loop.set_debug(False)
#     loop.run_until_complete(main())
# def mylousyprintfunction(eventdata):
# if eventdata.get('p/arams') and eventdata.get('params')['']
# print(pformat(eventdata))
from myFinance import models

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


# result_example = {'Result': {'UserCards': {
#     'Summary': [{'Currency': 376, 'ActualDebitSum': 4892.43, 'TotalDebitSum': 4892.43, 'CurrencySymbol': '₪'},
#                 {'Currency': 840, 'ActualDebitSum': 0.0, 'TotalDebitSum': 0.0, 'CurrencySymbol': '$'},
#                 {'Currency': 978, 'ActualDebitSum': 0.0, 'TotalDebitSum': 0.0, 'CurrencySymbol': '€'}], 'Cards': [
#         {'CatalogId': '640004', 'Last4Digits': '9894', 'ExpirationDate': '03/27', 'OwnerFullName': 'אפרים חזוני',
#          'CardName': 'max executive', 'CardImage': 'https://onlinelcapi.max.co.il/SharedMedia/12448/card296.png',
#          'CreditLimit': 15000.0, 'OpenToBuy': 12657.05, 'FixedDebit': 15000.0, 'CycleSummary': [
#             {'Date': '2022-10-11T00:00:00', 'Currency': 376, 'ActualDebitSum': 1436.32, 'TotalDebitSum': 1436.32,
#              'IsFinnal': False, 'CurrencySymbol': '₪'},
#             {'Date': '2022-10-11T00:00:00', 'Currency': 840, 'ActualDebitSum': 0.0, 'TotalDebitSum': 0.0,
#              'IsFinnal': False, 'CurrencySymbol': '$'},
#             {'Date': '2022-10-11T00:00:00', 'Currency': 978, 'ActualDebitSum': 0.0, 'TotalDebitSum': 0.0,
#              'IsFinnal': False, 'CurrencySymbol': '€'}], 'CycleSummaryInfo': None, 'ReturnCode': 0, 'CardLogo': 9,
#          'Index': 0, 'CreditLimitType': 0, 'IsActiveDigitalCard': False, 'IsOwnerDigitalCard': False,
#          'ShowMonthlyBillingLayout': False, 'IsControlsBiZCardSubscribe': False, 'ClearingAmtForOtb': None},
#         {'CatalogId': '460001', 'Last4Digits': '5920', 'ExpirationDate': '03/27', 'OwnerFullName': 'שרה אסקין חזוני',
#          'CardName': 'Dream Card VIP', 'CardImage': 'https://onlinelcapi.max.co.il/SharedMedia/12430/card277.png',
#          'CreditLimit': 20000.0, 'OpenToBuy': 16113.45, 'FixedDebit': 20000.0, 'CycleSummary': [
#             {'Date': '2022-10-11T00:00:00', 'Currency': 376, 'ActualDebitSum': 3456.11, 'TotalDebitSum': 3456.11,
#              'IsFinnal': False, 'CurrencySymbol': '₪'},
#             {'Date': '2022-10-11T00:00:00', 'Currency': 840, 'ActualDebitSum': 0.0, 'TotalDebitSum': 0.0,
#              'IsFinnal': False, 'CurrencySymbol': '$'},
#             {'Date': '2022-10-11T00:00:00', 'Currency': 978, 'ActualDebitSum': 0.0, 'TotalDebitSum': 0.0,
#              'IsFinnal': False, 'CurrencySymbol': '€'}], 'CycleSummaryInfo': None, 'ReturnCode': 0, 'CardLogo': 2,
#          'Index': 1, 'CreditLimitType': 0, 'IsActiveDigitalCard': False, 'IsOwnerDigitalCard': False,
#          'ShowMonthlyBillingLayout': False, 'IsControlsBiZCardSubscribe': False, 'ClearingAmtForOtb': None}],
#     'IsMultUsers': True, 'IsMultAccounts': False}}, 'CorrelationID': '6bd90b42-b717-4920-8406-a1e9c4babd4d',
#           'ReturnCode': 0, 'RcDesc': None}


class MaxScraper(Scraper):
    COMPANY = 'MAX'

    def get_transactions(self, start, end, username=None, password=None, grid=True, *args, **kwargs):
        # options = uc.ChromeOptions()
        # options.headless = True
        # options.add_argument('--headless')
        driver = get_selenium_driver(grid=grid)  # driver = uc.Chrome(enable_cdp_events=True)

        driver.get('https://www.max.co.il/homepage/welcome')
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'go-to-personal-area').click()
        driver.find_element(By.ID, 'login-password-link').click()
        driver.find_element(By.XPATH, '//*[@formcontrolname="username"]').send_keys(username)
        driver.find_element(By.XPATH, '//*[@formcontrolname="password"]').send_keys(password)
        driver.find_elements(By.XPATH, "//button[@id='send-code']")[1].click()
        time.sleep(5)
        # driver.add_cdp_listener('Network.responseReceived', mylousyprintfunction)
        driver.get('https://www.max.co.il/transaction-details/personal')
        time.sleep(3)
        print('trying')
        home_page_data = self.get_with_requests(driver, URL, HEADERS, PAYLOAD)
        current_month_total_some = home_page_data['Result']['UserCards']['Summary'][0]['ActualDebitSum']
        user = User.objects.get(username='efraim')
        info, created = models.AdditionalInfo.objects.get_or_create(user=user)
        info.value[self.COMPANY] = float(current_month_total_some)*-1
        info.save()

        url = 'https://www.max.co.il/api/registered/transactionDetails/getTransactionsAndGraphs?filterData={}&firstCallCardIndex=-1null&v=V3.85-HF.21'.format(
            urllib.parse.unquote(
                json.dumps({"userIndex": -1, "cardIndex": -1, "monthView": False, "date": "2022-05-30",
                            "dates": {"startDate": start.strftime('%Y-%m-%d'), "endDate": end.strftime('%Y-%m-%d')},
                            "bankAccount": {"bankAccountIndex": -1, "cards": None}})))
        transactions_response = self.get_with_requests(driver, url, HEADERS, PAYLOAD)
        # response = driver.get(
        #     'https://www.max.co.il/api/registered/transactionDetails/getTransactionsAndGraphs?filterData={}&firstCallCardIndex=-1null&v=V3.85-HF.21'.format(
        #         urllib.parse.unquote(
        #             json.dumps({"userIndex": -1, "cardIndex": -1, "monthView": False, "date": "2022-05-30",
        #                         "dates": {"startDate": start.strftime('%Y-%m-%d'), "endDate": end.strftime('%Y-%m-%d')},
        #                         "bankAccount": {"bankAccountIndex": -1, "cards": None}}))))
        # ))
        #     response = driver.get('https://www.max.co.il/api/registered/transactionDetails/getTransactionsAndGraphs?filterData={%22userIndex%22:-1,%22cardIndex%22:-1,%22monthView%22:true,%22date%22:%222022-05-30%22,%22dates%22:{%22startDate%22:%220%22,%22endDate%22:%220%22},%22bankAccount%22:{%22bankAccountIndex%22:-1,%22cards%22:null}}&firstCallCardIndex=-1null&v=V3.85-HF.21')
        # json_text = driver.find_element(By.CSS_SELECTOR, 'pre').get_attribute('innerText')
        # json_response = json.loads(json_text)
        # time.sleep(5)
        trans = []
        for t in transactions_response['result']['transactions']:
            name = t['merchantName']
            date = datetime.datetime.strptime(t['purchaseDate'], '%Y-%m-%dT%X')
            amount = t['actualPaymentAmount']
            arn = t['arn']
            trans.append({'name': name, 'date': date, 'amount': amount, 'arn': arn, })
        driver.quit()
        return trans


if __name__ == "__main__":
    # TODO cant import model becuse of cerculer imports
    end = datetime.datetime.now().replace(day=23)
    start = datetime.datetime.now().replace(day=21)
    transactions = MaxScraper().get_transactions(start, end, **c.get_credential)
    print(transactions)
