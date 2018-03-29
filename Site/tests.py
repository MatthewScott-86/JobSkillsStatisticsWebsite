# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase

import unittest
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_landing_page_title(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        self.assertIn("CS673", driver.title)
        assert "Job Statistics Portal" in driver.page_source
    
    def test_landing_page_has_proper_title(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        self.assertIn("CS673", driver.title)
        assert "Job Statistics Portal" in driver.page_source

    def test_landing_page_has_indeed_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        self.assertIn("CS673", driver.title)
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('a'):
            links+= link
        assert "Indeed" in  links
        
    def test_landing_page_has_glassdoor_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        self.assertIn("CS673", driver.title)
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('a'):
            links+= link
        assert "Glassdoor" in  links
    
    def test_landing_page_has_home_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        self.assertIn("CS673", driver.title)
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('a'):
            links+= link
        assert "Home" in  links

    def test_landing_page_has_compare_jobs_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        self.assertIn("CS673", driver.title)
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('a'):
            links+= link
        assert "Compare Jobs" in  links

    
    def test_landing_page_has_database_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        self.assertIn("CS673", driver.title)
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('a'):
            links+= link
        assert "Database" in  links


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
