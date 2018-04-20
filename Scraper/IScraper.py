from abc import ABCMeta, abstractmethod

class ScraperInterface(metaclass=ABCMeta):
    
    def __init__(self):
        pass
    
    def col_dict_to_array(self, dict, colum_num=5):
        pass
    
    def remove_empty_rows(self, array, col = 5):
        pass
    
    def list_to_dict(self, target_list):
        pass
    
    def incr_dict(self, dict, target_text):
        pass
    
    def column(self, matrix, i):
        pass
    
    def scrape(self, job_title="data analyst", job_location = "Boston, MA"):
        pass
        
    def getJobSkills(self, pageText):
        pass
    
    def getJobs(self, pageText):
        pass
    
    def getDataFromJobAndRegion(self, job_title="data analyst", job_location = "Boston, MA", page_count = 1):
        pass
    
        