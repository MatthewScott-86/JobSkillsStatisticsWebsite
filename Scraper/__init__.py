from importlib import import_module

from .IScraper import ScraperInterface

def GetScraperImplementation(type, *args, **kwargs):
    scraper_module = import_module('.' + "scraper", package = 'Scraper')
    if (type == "Indeed"):
        scraper_class = getattr(scraper_module, "Scraper")
        instance = scraper_class(*args, **kwargs)
        return instance
    else:
        raise NotImplementedError("No such scraper, " + type)
