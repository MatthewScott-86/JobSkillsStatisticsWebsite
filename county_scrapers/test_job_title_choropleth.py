
import unittest
from county_scrapers import county_scraper_jobsearch

class TestScraper(unittest.TestCase):

    def test_scrape(self):
        fips_dict = county_scraper_jobsearch.get_FIPS_dict()
        fips_dict_len = len(fips_dict)
        self.assertEqual(fips_dict_len, 37913)


if __name__ == "__main__":
    unittest.main()