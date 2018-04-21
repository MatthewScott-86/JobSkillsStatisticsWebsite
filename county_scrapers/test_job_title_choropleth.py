
import unittest
from county_scrapers import county_scraper_jobsearch

class TestScraper(unittest.TestCase):

    def test_fips_dict_length(self):
        fips_dict = county_scraper_jobsearch.get_FIPS_dict()
        fips_dict_len = len(fips_dict)
        self.assertEqual(fips_dict_len, 37913)

    def test_if_fips_in_fips_dict(self):
        fips_dict = county_scraper_jobsearch.get_FIPS_dict()
        self.assertIn('38017', fips_dict.values())
        self.assertIn('29167', fips_dict.values())
        self.assertIn('27143', fips_dict.values())
        self.assertIn('37171', fips_dict.values())
        self.assertIn('42049', fips_dict.values())





if __name__ == "__main__":
    unittest.main()