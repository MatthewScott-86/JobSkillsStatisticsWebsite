# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase

import unittest
import HtmlTestRunner
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    #Selenium Unit test cases starts here
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

    #Error handling test cases starts here    
    def test_indeed_menu_error(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090/indeed")
        driver.find_element_by_id("submit").click()
        soup = BeautifulSoup(driver.page_source, "html.parser")
        assert 'please input job and city' in driver.page_source

    def test_indeed_compare_menu_error(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090/indeed_compare")
        driver.find_element_by_css_selector(".btn.btn-primary").click()
        soup = BeautifulSoup(driver.page_source, "html.parser")
        assert 'please choose two jobs to compare' in driver.page_source

    def test_glassdoor_menu_error_general(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090/glassdoor")
        driver.find_element_by_id("submit1").click()
        soup = BeautifulSoup(driver.page_source, "html.parser")
        assert 'please choose a menu option' in driver.page_source

    def test_glassdoor_menu_error_box(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090/glassdoor")
        driver.find_element_by_id("submit2").click()
        soup = BeautifulSoup(driver.page_source, "html.parser")
        assert 'please choose a menu option' in driver.page_source
    
    #Integration Test cases starts here

    def test_landing_to_indeed_to_plot_1(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090/")
        indeed_button = driver.find_element_by_name("indeed_button")
        indeed_button.click()
        job = driver.find_elements_by_id("job")
        city = driver.find_elements_by_id("city")
        WebDriverWait(driver, 5).until(EC.visibility_of(job[0]))
        WebDriverWait(driver, 5).until(EC.visibility_of(city[0]))
        self.assertTrue(job[0].is_displayed())
        self.assertTrue(city[0].is_displayed())
        job[0].send_keys('data scientist')
        city[0].send_keys('Boston, Massachusetts')
        submit_button = driver.find_element_by_id("submit")
        submit_button.click()
        plot = driver.find_element_by_id("plot")
        WebDriverWait(driver, 5).until(EC.visibility_of(plot))
        self.assertTrue(plot.is_displayed())

    def test_landing_to_indeed_to_plot_2(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090/")
        indeed_button = driver.find_element_by_name("indeed_button")
        indeed_button.click()
        job = driver.find_elements_by_id("job")
        city = driver.find_elements_by_id("city")
        WebDriverWait(driver, 5).until(EC.visibility_of(job[0]))
        WebDriverWait(driver, 5).until(EC.visibility_of(city[0]))
        self.assertTrue(job[0].is_displayed())
        self.assertTrue(city[0].is_displayed())
        job[0].send_keys('software engineer')
        city[0].send_keys('Austin, Texas')
        submit_button = driver.find_element_by_id("submit")
        submit_button.click()
        plot = driver.find_element_by_id("plot")
        WebDriverWait(driver, 5).until(EC.visibility_of(plot))
        self.assertTrue(plot.is_displayed())

    def test_landing_to_indeed_to_plot_3(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8090/")
        indeed_button = driver.find_element_by_name("indeed_button")
        indeed_button.click()
        job = driver.find_elements_by_id("job")
        city = driver.find_elements_by_id("city")
        WebDriverWait(driver, 5).until(EC.visibility_of(job[0]))
        WebDriverWait(driver, 5).until(EC.visibility_of(city[0]))
        self.assertTrue(job[0].is_displayed())
        self.assertTrue(city[0].is_displayed())
        job[0].send_keys('daat scientist')
        city[0].send_keys('Austin, Texas')
        submit_button = driver.find_element_by_id("submit")
        submit_button.click()
        plot = driver.find_element_by_id("plot")
        WebDriverWait(driver, 5).until(EC.visibility_of(plot))
        self.assertTrue(plot.is_displayed())

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test_report'))