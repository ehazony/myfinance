# import asyncio
# import json
#
# from pyppeteer import launch
# import time
# from pyppeteer_stealth import stealth
import copy
import datetime
import json
import time

import django
import os
from pyppeteer.network_manager import Request

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

from pprint import pformat

# def mylousyprintfunction(eventdata):
# if eventdata.get('p/arams') and eventdata.get('params')['']
# print(pformat(eventdata))


import undetected_chromedriver as uc
import urllib
from selenium.webdriver.common.by import By

from bank_scraper.selenium_api import get_selenium_driver


def get_transactions(start, end):
    # options = uc.ChromeOptions()
    # options.headless = True
    # options.add_argument('--headless')
    driver = get_selenium_driver() # driver = uc.Chrome(enable_cdp_events=True)

    driver.get('https://www.max.co.il/homepage/welcome')
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'go-to-personal-area').click()
    driver.find_element(By.ID, 'login-password-link').click()
    driver.find_element(By.XPATH, '//*[@formcontrolname="username"]').send_keys('EFRAIMHAZONY@gmail.com')
    driver.find_element(By.XPATH, '//*[@formcontrolname="password"]').send_keys('Cinnamongirl1')
    driver.find_elements(By.XPATH, "//button[@id='send-code']")[1].click()
    time.sleep(5)
    # driver.add_cdp_listener('Network.responseReceived', mylousyprintfunction)
    driver.get('https://www.max.co.il/transaction-details/personal')
    time.sleep(3)
    print('trying')
    response = driver.get(
        'https://www.max.co.il/api/registered/transactionDetails/getTransactionsAndGraphs?filterData={}&firstCallCardIndex=-1null&v=V3.85-HF.21'.format(
            urllib.parse.unquote(json.dumps({"userIndex": -1, "cardIndex": -1, "monthView": False, "date": "2022-05-30",
                                             "dates": {"startDate": start.strftime('%Y-%m-%d'), "endDate":end.strftime('%Y-%m-%d') },
                                             "bankAccount": {"bankAccountIndex": -1, "cards": None}}))))
    # ))
    #     response = driver.get('https://www.max.co.il/api/registered/transactionDetails/getTransactionsAndGraphs?filterData={%22userIndex%22:-1,%22cardIndex%22:-1,%22monthView%22:true,%22date%22:%222022-05-30%22,%22dates%22:{%22startDate%22:%220%22,%22endDate%22:%220%22},%22bankAccount%22:{%22bankAccountIndex%22:-1,%22cards%22:null}}&firstCallCardIndex=-1null&v=V3.85-HF.21')
    json_text = driver.find_element(By.CSS_SELECTOR, 'pre').get_attribute('innerText')
    json_response = json.loads(json_text)
    time.sleep(5)
    trans = []
    for t in json_response['result']['transactions']:
        name = t['merchantName']
        date = datetime.datetime.strptime(t['purchaseDate'], '%Y-%m-%dT%X')
        amount = t['actualPaymentAmount']
        arn = t['arn']
        trans.append({'name': name, 'date': date, 'amount': amount, 'arn': arn, })
    return trans


if __name__ == "__main__":
    end = datetime.datetime.now().replace(day=23)
    start = datetime.datetime.now().replace(day=21)
    transactions = get_transactions(start, end)
    print(transactions)
