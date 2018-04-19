import matplotlib.pyplot as plt
plt.rcdefaults()
import copy
import plotly
import plotly.plotly as py
import plotly.figure_factory as ff
import requests
import csv
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='patryan117', api_key='sU5DfakuvEH0BEVqQE5e')
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import collections
import numpy as np
np.set_printoptions(threshold=np.inf)



def main():
    job_title = "Librarian"
    job_title = format_job_title(job_title, True)  # Keep second quote layer for an exact string match, remove quotes to search for skills or industries
    matrix = scrape_salaries(str(job_title))
    df = pd.DataFrame(matrix)
    df.columns = ['State Abbreviation', 'State Name', "Job Count", 'Post per Salary Range', 'Posts per County', 'Posts per Company', 'Post per Experience Level', 'Posts per Jop Type', 'Mean Salary Per State'  ]
    # df.to_csv("jobs_matrix.csv")   UNCOMMENT SAVE RAW CSV FOR MOST RECENT SCRAPER EXECUTION
    fips_dict = get_FIPS_dict()   # OPENS UP CITY CSV AND JOINS CITY AND STATE VARIABLES, AND SAVES AS DICTIONARY


    fips_post_dict = get_populated_FIPS_matrix(fips_dict,df)
    print(fips_post_dict)
    fips_list = list(map(int,(fips_post_dict.keys())))
    posts_list = list(map(int,(fips_post_dict.values())))
    make_county_cloropleth(fips_list, posts_list, job_title)


def make_county_cloropleth(fips, posts, job_title):

    # "#f7fbff", "#ebf3fb", "#deebf7","#d2e3f3",    # TAKING OUT A COUPLE COLORS TO INCREASE CONTRAST

    colorscale = [ "#c6dbef", "#b3d2e9", "#9ecae1", "#85bcdb", "#6baed6",
                  "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
                  "#08519c", "#0b4083", "#08306b"]

    fips = fips
    values = posts
    endpts = list(np.linspace(1, 100, len(colorscale) - 1))
    # endpts = list(np.linspace(1, max(values), len(colorscale) - 1))

    fig = ff.create_choropleth(
        fips=fips,
        values=values,
        binning_endpoints=endpts,
        colorscale=colorscale,
        show_state_data=True,
        show_hover=True,
        centroid_marker={'opacity': 0},
        asp=2.9,   # ASPECT RATIO:  DONT EVER TOUCH THIS!!!
        title= str(job_title) + " Job Posts per US County",
        legend_title='No. of Posts'
    )
    py.plot(fig, filename='choropleth_full_usa')     # CHANGE TO plotly.offline.plot TO PLOT OFFLINE


def get_populated_FIPS_matrix(translation_dict, job_data_matrix):


    FIPS_dict = {}

    for x in range(48):
        state = str(job_data_matrix.iloc[x][0])
        town_list = list(job_data_matrix.iloc[x][4].keys())
        for y in range(len(town_list)):
            try:
                town = town_list[y]
                job_count = job_data_matrix.iloc[x][4][town]
                town_state = str(town + " " + state)
                FIPS = translation_dict[town_state]
                if str(FIPS) not in FIPS_dict:
                    FIPS_dict[str(FIPS)] = 0

                if str(FIPS) in FIPS_dict:
                    FIPS_dict[str(FIPS)] = (str(int(FIPS_dict[str(FIPS)]) + int(job_count)))

            except:
                print ("The location " + str(town_list[y]) + " cannot be found.")


    return(FIPS_dict)

def scrape_salaries(job_title):
    job_count = 0

    print("\nSearching for ", job_title, " jobs in all 50 US states...\n")

    state_abbreviations_list = ["AL", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "ID", "IL", "IN",
                                "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV",
                                "NH", "NJ", "NM", "NY", "NC","ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN",
                                "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    state_full_names_list = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
                       "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
                       "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
                       "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
                       "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
                       "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

    job_data_matrix = [[0 for x in range(9)] for y in range(50)]
    job_title = job_title.replace(" ", "+")   # format the job title so that it can be directly inserted into the indeed url
    job_title = job_title.replace("&", "%26")   # format the job title so that it can be directly inserted into the indeed url

    salary_list = []
    salary_dict = {}
    location_dict = {}
    company_dict = {}
    experience_level_dict = {}
    job_types_dict = {}

    for state in range(len(state_abbreviations_list)):

        global state_abbreviation
        state_abbreviation = state_abbreviations_list[state]
        state_name = state_full_names_list[state]
        url = "https://www.indeed.com/jobs?q=title%3A" + str(job_title) + "&l=" + str(state_abbreviation)+ "&radius=50&start=0"


        print(url)
        page = requests.get(url)
        salary = "N\A"
        soup = BeautifulSoup(page.text, "html.parser")

        for div in soup.find_all(name="div", attrs={"id":"searchCount"}):
            div = div.get_text()
            div = div.replace("\n","")
            div = div.replace(",","")
            div = div.replace("Page 1 of ","")
            div = div.replace(" jobs","")
            div = re.findall('\d+', div)
            div = int(div[0])
            job_count = div

        try:
            for div in soup.find_all(name="p", attrs={"id": "univsrch-salary-currentsalary"}):
                salary = div.get_text()
                if "hour" in salary:
                    salary = re.findall('\d+', salary)
                    salary = int(str(salary[0])+str(salary[1]))   # concatonates the two halves of the salary numbers
                    salary = int(salary)
                    salary = salary / 100 * 40 * 50
                    salary = round(salary, 0)
                    salary_list.append(salary)

                else:
                    salary = re.findall('\d+', salary)
                    salary = int(str(salary[0]) + str(salary[1]))  # concatonates the two halves of the salary numbers
                    salary_list.append(salary)
        except:
            salary = "N/A"
            salary_list.append(salary)
        print("Location: ", state_abbreviation, "\t  Mean Salary: ", salary)
        mean_salary = salary


        for div in soup.find_all(name="div", attrs={"id":"SALARY_rbo"}):

            tier = div.get_text()
            tier = tier.replace("\n","")
            tier = tier.replace(",","")
            tier = tier.replace("$","")
            tier = tier.replace("$","")
            tier = tier.replace("(","")
            tier = tier.replace(")"," ")
            tier = tier.split(" ")
            tier = tier[:-1]
            for x in range(0,len(tier),2):
                price_range = tier[x]
                number = tier[x+1]
                salary_dict[price_range] = number

        for div in soup.find_all(name="div", attrs={"id":"LOCATION_rbo"}):
            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'loc', '1');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '2');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '3');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '4');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '5');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '6');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '7');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '8');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '9');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '10');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '11');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '12');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '13');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '14');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '10');"}):
                locations_to_ordered_dict(li,location_dict)

        for div in soup.find_all(name="div", attrs={"id": "COMPANY_rbo"}):
            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '1');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '2');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '3');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '4');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '5');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '6');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '7');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '8');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '9');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '10');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '11');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '12');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '13');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '14');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '15');"}):
                companies_ordered_dict(li, company_dict)

        for div in soup.find_all(name="div", attrs={"id": "EXP_LVL_rbo"}):
            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'explvl', '1');"}):
                experience_level_to_ordered_dict(li, experience_level_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'explvl', '2');"}):
                experience_level_to_ordered_dict(li, experience_level_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'explvl', '3');"}):
                experience_level_to_ordered_dict(li, experience_level_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'explvl', '4');"}):
                experience_level_to_ordered_dict(li, experience_level_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'explvl', '5');"}):
                experience_level_to_ordered_dict(li, experience_level_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'explvl', '6');"}):
                experience_level_to_ordered_dict(li, experience_level_dict)

        for div in soup.find_all(name="div", attrs={"id": "JOB_TYPE_rbo"}):
            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '1');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '2');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '3');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '4');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '5');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '6');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '7');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '8');"}):
                job_type_to_ordered_dict(li, job_types_dict)

        print("Job Count: ", job_count)
        print("Salary Ranges: ", salary_dict)
        print("Locations: ", location_dict)
        print("Company Names: ",company_dict)
        print("Experience Levels: ", experience_level_dict)
        print("Job Types: ", job_types_dict)
        print("\n")

        job_data_matrix[state][0] = state_abbreviation
        job_data_matrix[state][1] = state_name
        job_data_matrix[state][2] = job_count
        job_data_matrix[state][3] = salary_dict
        job_data_matrix[state][4] = location_dict
        job_data_matrix[state][5] = company_dict
        job_data_matrix[state][6] = experience_level_dict
        job_data_matrix[state][7] = job_types_dict
        job_data_matrix[state][8] = mean_salary

        job_count=0
        salary_dict = {}
        location_dict = {}
        company_dict = {}
        experience_level_dict = {}
        job_types_dict = {}

    return job_data_matrix

def format_job_title(job_title, exact_match=True):
    if exact_match:
        job_title = '"' + job_title + '"'
    return job_title

def locations_to_ordered_dict(li,dict):
    li = li.get_text()
    li = li.replace(")", "")
    li = li.replace(" (", "")
    li = li.replace("\n", "")
    li = li.replace(" " + state_abbreviation, "")
    li = li.replace(" ", "_")
    try:
        li = li.split(",")
        li[0] = li[0].replace("_"," ")
        dict[li[0]] = li[1]
    except:
        print("Someone entered the state as the county: ", li)

def companies_ordered_dict(li, dict):
    li = li.get_text()
    li = li.replace("\n", "")
    li = li.replace(")", "")
    li = li.replace(" (", ",")
    li = li.split(",")
    li[0] = li[0].replace("_"," ")
    dict[li[0]] = li[1]

def job_type_to_ordered_dict(li, dict):
    li =  li.get_text()
    li = li.replace("\n", "")
    li = li.replace(")", "")
    li = li.replace(" Level", "_Level")
    li = li.replace("(", "")
    li = li.split(" ")
    li[0] = li[0].replace("_"," ")
    dict[li[0]] = li[1]

def experience_level_to_ordered_dict(li, dict):
    li =  li.get_text()
    li = li.replace("\n", "")
    li = li.replace(" Level", "_Level")
    li = li.replace("(", "")
    li = li.replace(" )", "")
    li = li.replace(")", "")
    li = li.split(" ")
    dict[li[0]] = li[1]

def get_FIPS_dict():
    with open('us_cities.csv', mode='r') as infile:
        reader = csv.reader(infile)
        dict = {str(rows[0])+" "+str(rows[2]):rows[5] for rows in reader}
        return dict


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))