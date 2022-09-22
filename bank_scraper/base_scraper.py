import abc


class Scraper:
    @abc.abstractmethod
    def get_transactions(self, start, end,  *args, **kwargs):
        pass
