from bank_scraper.cal import CalScraper
from bank_scraper.discount import DiscountScraper
from bank_scraper.max import MaxScraper
from myFinance import models


def scraper_factory(scraper_type):
    if scraper_type == models.Credential.DISCOUNT:
        return DiscountScraper()
    elif scraper_type == models.Credential.MAX:
        return MaxScraper()
    elif scraper_type == models.Credential.CAL:
        return CalScraper()
    else:
        raise Exception('No scraper type of {}'.format(scraper_type))
