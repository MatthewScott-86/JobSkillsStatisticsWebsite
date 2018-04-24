import unittest
import CollectData
import Scraper
import datetime
from Scraper import scraper

class TestCollectData(unittest.TestCase):
    
    def makeSkillsJobDataCollection(self, count, skills):
        job_data = []
        scraper = Scraper.GetScraperImplementation("Indeed")
        for r in range(count):
            job_data.append(Scraper.scraper.JobData.fromParameters(company = "", jobTitle = "", salary = "", location = "", url = ""))
            job_data[r].skills = {}
            for upperSkill in scraper.data_science_skills_list:
                skill = upperSkill.lower()
                if skill in skills:
                    job_data[r].skills[skill] = 1
                else:
                    job_data[r].skills[skill] = 0
        return job_data  
        
    def test_nextMonth(self):
        now = datetime.datetime(year = 2000, month = 1, day = 1, hour = 1, minute = 1, second = 1)
        end_date = CollectData.CollectData.getNextMonth(now)
        assert(end_date.month == 2)
        
    def test_nextMonthJanuary(self):
        now = datetime.datetime(year = 2000, month = 12, day = 1, hour = 1, minute = 1, second = 1)
        end_date = CollectData.CollectData.getNextMonth(now)
        assert(end_date.month == 1)
        assert(end_date.year == 2001)
        
    def test_skillsGetCounts(self):
        skills = {"c++", " r ", " sas "}
        count = 5
        scraper = Scraper.GetScraperImplementation("Indeed")
        job_data = self.makeSkillsJobDataCollection(count, skills)
        
        counts = CollectData.CollectData.getCounts(job_data)
       
        for skillUpper in scraper.data_science_skills_list:
            skill = skillUpper.lower()
            if skill in skills:
                assert(counts[skill] == count)
            else:
                assert(skill not in counts)
                
    def test_emptySkills(self):
        skills = {}
        count = 10
        scraper = Scraper.GetScraperImplementation("Indeed")
        job_data = self.makeSkillsJobDataCollection(count, skills)
        
        counts = CollectData.CollectData.getCounts(job_data)
        for skillUpper in scraper.data_science_skills_list:
            skill = skillUpper.lower()
            assert(skill not in counts)
            
    def test_allSkills(self):
        scraper = Scraper.GetScraperImplementation("Indeed")
        upperSkills = scraper.data_science_skills_list
        skills = []
        count = 5
        
        for skill in upperSkills:
            skills.append(skill.lower())
            
        job_data = self.makeSkillsJobDataCollection(count, skills)
        
        counts = CollectData.CollectData.getCounts(job_data)
        for skillUpper in scraper.data_science_skills_list:
            skill = skillUpper.lower()
            assert(counts[skill] == count)
        
        
        
        