import asyncio

from pyppeteer import launch


async def run_process():
    browser = await launch({'executablePath': '/usr/bin/chromium-browser',
        'args': ['--no-sandbox', '--disable-dev-shm-usage'],'headless': True})
    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})

    # go to site
    await page.goto('https://pricebackers.com/')
    url = await page.evaluate('() => document.location.href')
    await browser.close()
    print('url ' + url)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(False)
    transactions = []
    data = loop.run_until_complete(asyncio.gather(run_process()))
    print(f'Finished!')

