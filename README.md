# JobSkillsStatisticsWebsite
Website Showing Statistics on Skills needed for Jobs in US Regions
Implemented with the Django framework

## Modules
  ### EmploymentSkillsStatistics
  Required for Django architecture. Some information used for presenting our website 
  is contained in this package. The paths for various files files, including our sqlite database is in the settings 
  file. The urls file links website URLs to views in the Site package
  
  ### Site
  This package primarily contains our views and our models. The models file describes our code first database. 
  This includes those entity objects needed for storing and displaying data. 
  The views describe both how to render the html files in the templates folder and how and what data to render, 
  while the aforementioned urls file describes on which page to render. The html files themselves along with the 
  Django framework also describe how they should be rendered through keywords referenced in the views and recognized 
  by the Django framework. Some of the views utilize the scraper classes directly to pull and then visualize data,
  while others display data from persistent storage. 

  ### Scraper
  This package is responsible for crawling and scraping web sites for data. 
  IScraper is the interface describing the behavior for scrapers of different websites. 
  The scraper file is currently the implementation of IScraper for the indeed web page. 
  
  ### CollectData
  The CollectData package accepts data directly from a scraper and stores it persistently. 
  This package may also modify the data for better storage. 
  For example, one of its uses is to aggregate the data from a scraper return for quick display 
  of that aggregated data in some of our graphs.
  
## Other Folders
  ### county_scrapers
  Choropleth related functions. Need to be incorporated into Scraper package
  
  ### static and staticfiles
  CSS, Fonts, and Javascript files 
  
  ### templates
  HTML files 
  
  ### data
  Non database persistent storage (the glassdoor data only at the moment)
