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
        self.driver = webdriver.PhantomJS()

    def test_landing_page_title(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        print(driver)
        self.assertIn("Bird's Eye Statistics", driver.title)
        assert "Job Statistics Portal" in driver.page_source
    
    def test_landing_page_has_proper_title(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        assert "Job Statistics Portal" in driver.page_source

    def test_landing_page_has_indeed_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('a'):
            links+= link
        assert "Indeed" in  links
        
    def test_landing_page_has_glassdoor_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('a'):
            links+= link
        assert "Glassdoor" in  links
    
    def test_landing_page_has_home_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('a'):
            links+= link
        assert "Home" in  links

    def test_landing_page_has_compare_jobs_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('a'):
            links+= link
        assert "Compare Jobs" in  links

    
    def test_landing_page_has_database_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('a'):
            links+= link
        assert "Database" in  links
    
    def test_indeed_page_has_city_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090/indeed")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('select'):
            links+= link
        assert next((True for link in links if "Which City?" in link), False)

    def test_indeed_page_has_job_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090/indeed")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('select'):
            links+= link
        assert next((True for link in links if "Do you have a job?" in link), False)

    def test_compare_page_has_first_job_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090/indeed_compare")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('select'):
            links+= link
        assert next((True for link in links if "Choose a job" in link), False)

    def test_compare_page_has_2nd_job_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090/indeed_compare")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('select'):
            links+= link
        assert next((True for link in links if "Choose a second job" in link), False)

    def test_glassdoor_page_has_gen_stat_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090/glassdoor")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('select'):
            links+= link
        assert next((True for link in links if "General Statistics" in link), False)

    def test_glassdoor_page_has_box_plot_menu(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090/glassdoor")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        links = []
        for link in soup.find_all('select'):
            links+= link
        assert next((True for link in links if "Box Plot" in link), False)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
