import matplotlib.pyplot as plt
plt.rcdefaults()
import requests
import plotly
import operator
from fake_useragent import UserAgent
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='patryan117', api_key='4ShAMHvEZPvz1AdSEjGm')
import matplotlib.ticker as mtick
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import numpy as np
np.set_printoptions(threshold=np.inf)





def main():
    raw_job_matrix = scrape("data scientist", "Boston, MA", 3)
    #clean_job_matrix = remove_empty_rows(raw_job_matrix)
    clean_job_matrix =  col_dict_to_horz_bar_chart(raw_job_matrix)              #THIS KEEPS THROWING AN  ERROR BECAUSE THE LOOP IS NOT DYNAMIC
    #export_as_csv(clean_job_matrix)





def cleanse(dataframe):
    df = np.array(dataframe)
    df = remove_empty_rows(df, 7)
    # df = format_dates(df,4)
    return df


def export_as_csv(df):
    df = pd.DataFrame(df)
    df.to_csv("jobs_matrix.csv")




"""
####################################################################################################################################################3
#
#  TO DO:
#
######################################################################################################################################################

    WE NEED TO LIMIT THE NUMBER OF SELECTABLE TITLES, OTHERWISE WE WONT BE ABLE TO FORM A DATABASE.
    :
    TITLE- LIMITED
    LOCATIONS - BY STATE




  WHAT TO DO WITH PAGES THAT LINK TO OUTSIDE SITES:
    Option 1: Remove (blank dictionary columns) them with the cleansing process
    Option 2: Have a try-except block that  


   FINAL PAGE DETECTION:
   Need to have a logic test that can identify when the last page has been reached, so searching can stop.
   Oddly the indeed site will kick back to either the second to last, or to the last page page for search calls exceeding the page limit.
   Cannot simply compare the HTML of current page to previous pages to check if page has been revisited (since ads and sponsored content change every time)
   I assume that this will have to be fixed by:
            1) stopping when a post has already been found (will definitely on sponsored content)
            2 ) identifying using the counter on the bottom of the page

    PUSH THE DICTIONARY CREATION TIL AFTER THE ORIGINAL SCRAPING LOOP


   CLEANSING FUNCTION:
   Need to have a function that will
        1) remove blank rows from job_data_matrix,
        2) remove incomplete rows where the title, company was found, but the post URL was not able to be parsed
        3) remove duplicate rows (i.e. identical posts)

# WTF is indeed prime?!  (obv not a job posting), and do we need exceptions in order to circumvent?!  (might only show to browsers)





# General Questions:

- Does indeed repeat non-sponsored posts
- Is there any way to grab just the  primary location (Natick, MA) and not the secondary information
- Should we search by date?
    could be helpful for providing a natural limit when doing a nationwide search (scraping until 30+ days is found)
- is there any reason that the description should be part of the data frame?
- What would we need to do to have a statewide search (and visualize as cloropleth) , is it possible, or would we just do major metro areas?
- If a search is "redundant" but has a different URL, is it safe to assume that poster's account ran dry, and they had to re-post?
- Is there a way to distinguish between two concurent posts for the same job (and is there a difference logically?)
- 




####################################################################################################################################################
"""

def remove_duplicate_rows(df):

    array = np.array(df)
    array_size = array.shape[0]
    for x in range(array_size):
        current_post = array[x]


    counter = 0
    array = np.array(df)
    print('Total array size: ', array.shape[0])
    while counter != (array.shape[0]):
        print("counter is: ", counter)
        if array[counter][col] == 0:
            array = np.delete(array, counter, 0)
            print('we deleted something, new length: ', array.shape[0])
        else:
            counter += 1
    print(array)
    return array


def col_dict_to_horz_bar_chart(dict, colum_num=7):
    keys = list(dict[0][colum_num].keys())    # extract the keys
    cum_dict = list_to_dict(keys)             # cumulative dictionary
    skills_array = []
    count_array = []
    job_count = 0
    for x in range(0,5000):     # DEF MORE COLUMNS THAN WE ACTUALLY NEED, IS THERE SOME WAY TO MAKE THIS DYNAMIC?
        if dict[x][colum_num] != 0:
            job_count += 1
            for y in keys:                          # if the job_title column is not empty
                if dict[x][colum_num][y] == 1:         # if dictionary for a word is 1 (aka yes)
                    cum_dict[y] += 1                    #increment the cumulative dictionary

    for x in cum_dict:
        skills_array.append(x)
        count_array.append(cum_dict[x]/job_count)

    y_pos = np.arange(len(skills_array))
    plt.barh(y_pos, count_array, align='center', alpha=0.5)
    plt.yticks(y_pos, skills_array)
    plt.xlim(0,1)
    plt.xlabel("Frequency")
    plt.ylabel('Keywords')
    plt.title('Keyword Frequency per Job Search')
    plt.tight_layout()
    plt.show()
    return(cum_dict)


# def format_dates(array, index):
#     counter = 0
#         while counter != (array.shape[0]):
#             if array[counter][index] ==






def remove_empty_rows(df, col = 7):

    counter = 0
    array = np.array(df)
    print('Total array size: ', array.shape[0])
    while counter != (array.shape[0]):
        print("counter is: ", counter)
        if array[counter][col] == 0:
            array = np.delete(array, counter, 0)
            print('we deleted something, new length: ', array.shape[0])
        else:
            counter += 1
    print(array)
    return array


def list_to_dict(target_list):    # Creates an dictionary for counting, with each pair as key:0
    target_list = list({ str(target_list[x].lower())for x in range(len(target_list))})
    return {target_list[x] : 0 for x in range(len(target_list))}


def incr_dict(dict, target_text):
    for x in dict.keys():
        if x in target_text:
            dict[x] += 1
    return(dict)


def column(matrix, i):
    return [row[i] for row in matrix]



skills_list = ["Python", 'sql', "hadoop", " R ", "C#", "SAS", "C++", "Java ", "Matlab", "Hive", "Excel", "Perl", "noSQL",
                            "JavaScript", "HBase", "Tableau", "Scala", "machine learning",  "Tensor Flow",
               "deep learning", "Economics", "Computer Science", " ML ", " PHP ", "Visual Basic", "css", "SAS", " Octave "  ]

frameworks_list = ["hadoop", "spark", "aws", "hive", "nosql", "cassandra", "mysql",
                   "mysql", "hbase", "pig", "mongodb", "git", "elasticsearch", "numpy",
                   "tensorflow", "scipy", "hadoop" ]

academics_list = [" PhD ", " Bachelor's ", " Bachelors ", " Master's ", "Masters", "publications", "Journal", "statistics",
                  "Mathematics", ]




global list_spot
global matrix_counter


def scrape(job_title="data analyst", job_location = "Boston, MA", num_pages = 1):


    start_time = time.time()

    print("\nSearching for '" + job_title + "' jobs in the '" + job_location + "' area...\n")


    w, h =12, 6000;
    global job_data_matrix                                                   # Define a matrix of enough rows to hold all scraped job posts
    job_data_matrix = [[0 for x in range(w)] for y in range(h)]
    list_spot = 0
    matrix_counter = 0
    job_page_soup_list = []


    job_title = job_title.replace(" ", "+")   # format the job title so that it can be directly inserted into the indeed url
    job_location = job_location.replace(" ", "+")    # format the job location so that it can be inserted into the indeed url
    job_location = job_location.replace(",", "%2C")




    for x in range(num_pages):           # number of pages to be scraped

        headers = requests.utils.default_headers()
        headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

        counter = x * 10
        url = "https://www.indeed.com/jobs?q=" + str(job_title) + "&l=" + str(job_location) + "&start=" + str(counter)
        print("\nSearching URL: " + "(" +str(x+1)+ ")" + "\n" + url + "\n")


        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")    # read the various components of the page, rather than as one long string.
        job_page_soup_list.append(soup)
       # print(soup.prettify())                            #printing soup in a more structured tree format that makes for easier reading

        jobs = []
        for div in soup.find_all(name="div", attrs={"class":"row"}):
          for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])

        dates = []
        for div in soup.find_all(name="div", attrs={"class":"row"}):
            try:
                for a in div.find(name="span", attrs= {"class":"date"}):
                    dates.append(a)
            except:
                dates.append("Sponsored")


        companies = []
        for div in soup.find_all(name="div", attrs={"class":"row"}):
            company = div.find_all(name="span", attrs = {"class":"company"})
            if len(company) > 0:
                for b in company:
                    companies.append(b.text.strip())
            else:
                sec_try = div.find_all(name="span", attrs = {"class":"result - link - source"})
                for span in sec_try:
                    companies.append(span.text.strip())


        post_urls=[]
        for div in soup.find_all(name="div", attrs={"class": "row"}):
            for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
                base_url = (a["href"])
                post_urls.append("http://indeed.com"+str(base_url))


        locations = []
        spans = soup.find_all(name="span", attrs = {"class" : "location"})
        for span in spans:
            locations.append(span.text)


        salaries = []
        for div in soup.find_all(name="div", attrs={"class" : "row"}):
            try:
                salaries.append(div.find("nobr").text)
            except:
                try:
                    div_two = div.find(name="div", attrs={"class": "sjcl"})
                    div_three = div_two.find("div")
                    salaries.append(div_three.text.strip())
                except:
                    salaries.append("No Salary Provided")


        list_spot += matrix_counter
        matrix_counter = 0

        for x in range((len(jobs))):
            job_data_matrix[x + list_spot][0] = jobs[x]
            job_data_matrix[x + list_spot][1] = companies[x]
            job_data_matrix[x + list_spot][2] = salaries[x]
            job_data_matrix[x + list_spot][3] = locations[x]
            job_data_matrix[x + list_spot][4] = dates[x]
            job_data_matrix[x + list_spot][5] = post_urls[x]
            target_url = job_data_matrix[x+list_spot][5]


            try:
                target_url
                post_page = requests.get(target_url)
                job_soup = BeautifulSoup(post_page.text, "html.parser")

                job_soup = job_soup.find(name="span", attrs={"id": "job_summary"})
                job_soup = job_soup.get_text().lower()

            except:
                print("x:" + str(x) + "  list_spot:" + str(list_spot) + " matrix_counter: " + str(matrix_counter))
                print(" URL ERROR!!! \n")
                continue

            job_soup = job_soup.replace(",", " ")
            job_soup = job_soup.replace(".", " ")
            job_soup = job_soup.replace(";", " ")
            job_data_matrix[x +list_spot][6] = job_soup

            data_science_skills_dict = list_to_dict(skills_list)
            job_data_matrix[x+list_spot][7] = incr_dict(data_science_skills_dict, job_soup)

            print ( "\nJob Title: " + job_data_matrix[x + list_spot][0] + "\t" + "Company: " + job_data_matrix[x + list_spot][1] + "\t"+ "Location: " + job_data_matrix[x + list_spot][3] + "\t" + " Date: "  + job_data_matrix[x + list_spot][4] )
            print(str(job_data_matrix[x+ list_spot][7]))
            matrix_counter += 1




    elapsed_time = time.time() - start_time



    return(job_data_matrix)





# print(np.matrix(returned_job_matrix))

# df = pd.DataFrame(returned_job_matrix)
# df.to_csv("jobs_matrix.csv")


if __name__ == '__main__':
    main()