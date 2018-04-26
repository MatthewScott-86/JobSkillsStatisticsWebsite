
import django
from plotly.api.v2.grids import row
django.setup()
import csv
from django.utils import timezone
import Scraper
from Scraper import preprocessing
from Site import DisplayData
from django.db.models import F
from Site.models import *

def printShapeFile():
    import shapefile
    shape = shapefile.Reader("C:\\Users\Matt\\Downloads\\tl_2017_us_county\\tl_2017_us_county.shp")
    num_records = shape.numRecords
    
    for i in range(0, num_records):
        feat = shape.shapeRecord(i)
        print(feat.record[4] + "(" + feat.record[1] + "," + feat.record[0] + ")")
        
    print(shape.shapeRecords()[0])
    
def getNextMonth(now):
    end_date = datetime.datetime(now.year, now.month, 1)
    
    if (now.month == 12):
        end_date = datetime.datetime(now.year + 1, 1, 1)
    else:
        end_date = datetime.datetime(now.year, now.month + 1, 1)
        
    return end_date
               
def getCounts(unscrubbed_data):
    counts = {"" : 0}
    for jobSkills in unscrubbed_data:
            
            for skill in jobSkills.skills:
                #TODO Add logic for date posted filtering
                if (jobSkills.skills[skill] > 0):
                    if (skill in counts):   
                        currentCount = counts[skill]
                        counts[skill] = currentCount + 1
                    else: 
                        counts[skill] = 1                    
    
    del counts[""]
    return counts
    
def runPopulateJobSkillRegionData(scraper_implementation, job_title, job_location, geography_id, now):
    try:
        unscrubbed_data = scraper_implementation.getDataFromJobAndRegion(job_title, job_location)
        end_date = getNextMonth(now)
        counts = getCounts(unscrubbed_data)

        for jobSkill in counts:

            job, created = Jobs.objects.get_or_create(category = job_title)
            skill, created = Skills.objects.get_or_create(skill = jobSkill)
            
            row, count = JobSkillRegionDateCount.objects.get_or_create(
                job_id = job.id,
                skill_id = skill.id,
                geography_id = geography_id,
                start_date = timezone.make_aware(datetime.datetime(now.year, now.month, 1), timezone.get_current_timezone()),
                end_date = timezone.make_aware(end_date, timezone.get_current_timezone()))
            
            JobSkillRegionDateCount.objects.filter(id = row.id).update(posted_count = F('posted_count')+ counts[jobSkill])
            print("Success")
    except:
        print("failed")
        
def runPopulateJobSkillCityData(scraper_implementation, job_title, job_location, city_id, now):
    try:
        unscrubbed_data = scraper_implementation.getDataFromJobAndRegion(job_title, job_location)
        
        end_date = getNextMonth(now)
            
        counts = getCounts(unscrubbed_data)
        
        for jobSkill in counts:
            #p, created = JobSkill.objects.get_or_create(category = job_title, skill = jobSkill[1])
            job, created = Jobs.objects.get_or_create(category = job_title)
            skill, created = Skills.objects.get_or_create(skill = jobSkill[1])
            
            row, count = JobSkillCityDateCount.objects.get_or_create(
                job_id = job.id,
                skill_id = skill.id,
                city_id = city_id,
                start_date = timezone.make_aware(datetime.datetime(now.year, now.month, 1), timezone.get_current_timezone()),
                end_date = timezone.make_aware(end_date, timezone.get_current_timezone()))
            
            JobSkillCityDateCount.objects.filter(id = row.id).update(posted_count = F('posted_count')+ counts[jobSkill])
            print("Success")
    except:
        print("failed")

def populateCity():
    country = "US"
    country_code = 1
    csv_file = open("C:\\Users\\Matt\\Desktop\\CS673\\Cities.csv", "rt", encoding="ansi")
    reader = csv.reader(csv_file)
    first = True
    
    for row in reader:
        if(first):
            first = False
        else:
            state_code = row[1]
            county_code = row[2]
            state = row[9]
            county = ""
            try:
                county = Geography.objects.get(SubAreaCode = county_code)
            except:
                county = ""
                
            Cities.objects.get_or_create(Country = country, 
                                     CountryCode = country_code,
                                     Area = state,
                                     AreaCode = state_code,
                                     County = county,
                                     CountyCode = county_code,
                                     City = row[8])
     
def populateGeography():
    country = "US"
    country_code = 1
    csv_file = open("C:\\Users\\Matt\\Desktop\\CS673\\Geography.csv", "rt", encoding="ansi")
    reader = csv.reader(csv_file)
    states = {0 : ""}
    first = True
    
    for row in reader:
        if(first):
            first = False
        else:
            if(row[0] == "40"):
                states[row[1]] = row[6]
            if(row[0] == "50"):
                state = states[row[1]]
                state_code = row[1]
                county_code = row[2]
                county = row[6][:row[6].rfind(' ')]

                Geography.objects.get_or_create(Country = country, 
                                         CountryCode = country_code,
                                         Area = state,
                                         AreaCode = state_code,
                                         SubArea = county,
                                         SubAreaCode = county_code)

def populateMany(scraper_implementation):
    job_titles = ["data scientist",
                  "software engineer",
                  "software developer",
                  "computer scientist",
                  "information technology",
                  "network architect",
                  "database administrator",
                  "web developer"]    
    
    regions = Geography.objects.filter(AreaCode = 25).all()
    cities = Cities.objects.all()
    now = datetime.datetime.now()
    
    for region in regions:
        for job in job_titles:
            runPopulateJobSkillRegionData(scraper_implementation,
                job,
                region.SubArea + " County, " + region.Area, 
                region.id, 
                now)
    '''
    
    for city in cities:
        for job in job_titles:
            runPopulateJobSkillCityData(scraper_implementation,
                job,
                city.City + ", " + city.Area, 
                city.id, 
                now)'''
            
     
if __name__ == "__main__":  
    scraper_implementation = Scraper.GetScraperImplementation("Indeed")
    populateMany(scraper_implementation)
    #populateCity()
    #populateGeography()
    #printShapeFile()
    #DisplayData.GetSkillsFromJobRegionDateCount("data scientist", "Boston, Massachusetts")
   
    
    
    