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



def main(title):
    job_title = str(title)
    job_title = format_job_title(job_title, False)  # Keep second quote layer for an exact string match, remove quotes to search for skills or industries
    matrix = scrape_salaries(str(job_title))
    df = pd.DataFrame(matrix)
    df.columns = ['State Abbreviation', 'State Name', "Job Count", 'Post per Salary Range', 'Posts per County', 'Posts per Company', 'Post per Experience Level', 'Posts per Jop Type', 'Mean Salary Per State'  ]
    # df.to_csv("jobs_matrix.csv")  #  UNCOMMENT TO SAVE RAW CSV FOR MOST RECENT SCRAPER EXECUTION
    pie_list = []
    pie_list.append(make_salary_donut_chart(df))
    pie_list.append(make_location_donut_chart(df))
    pie_list.append(make_company_donut_chart(df))
    pie_list.append(make_job_type_donut_chart(df))
    print('PIE_LIST:', pie_list)
    return(pie_list)

def format_as_financial(array):
    for x in range(len(array)):
        array[x] = '${:,.0f}'.format(array[x])
    return array


def make_location_range_bar_chart(dataframe):
    dict = dataframe.iloc[0,4]
    locations = list(map(str, (dict.keys())))
    locations = locations[::-1]
    count = list(map(str, (dict.values())))
    count = count[::-1]
    print(locations)
    print(count)

    data = [go.Bar(
        x=count,
        y=locations,
        orientation='h'
    )]
    plot_div = plotly.offline.plot(data, output_type="div", include_plotlyjs=False)
    return plot_div


def make_salary_range_bar_chart(dataframe):
    dict = dataframe.iloc[0,3]
    salaries = list(map(int, (dict.keys())))
    count = list(map(str, (dict.values())))
    print(salaries)
    print(count)

    data = [go.Bar(
        x=count,
        y=salaries,
        orientation='h'
    )]
    plot_div = plotly.offline.plot(data, output_type="div", include_plotlyjs=False)
    return plot_div


def make_salary_donut_chart(dataframe):
    dict = dataframe.iloc[0, 3]
    salaries = list(map(int, (dict.keys())))
    salaries = format_as_financial(salaries)
    count = list(map(str, (dict.values())))

    fig = {
        "data": [
            {
                "values": count,
                "labels": salaries,
                "text":salaries,
                 "showlegend": False,
                'textposition': 'outside',
                "textfont" : {
                "size":10,
                },
                "name": "",
                "hoverinfo": "label+percent+name",
                "hole": .7,
                "type": "pie"
            },
            ],
        "layout": {
            "autosize" : True,
            "width" : 350,
            "height" : 350,
            "title": "",
            "annotations": [
                {
                    "font": {
                        "size": 15
                    },
                    "showarrow": False,
                    "text": "Salaries",
                },
            ]
        }
    }

    plot_div = plotly.offline.plot(fig, output_type="div", include_plotlyjs=False)
    return plot_div


def make_location_donut_chart(dataframe):
    dict = dataframe.iloc[0, 4]
    salaries = list(map(str, (dict.keys())))
    count = list(map(str, (dict.values())))
    fig = {
        "data": [
            {
                "values": count,
                "labels": salaries,
                "text":salaries,
                "showlegend": False,
                'textposition': 'outside',
                "textfont": {
                    "size": 10,
                },
                "name": "",
                "hoverinfo": "label+percent+name",
                "hole": .7,
                "type": "pie"
            },
            ],
        "layout": {
            "title": "",
            "width": 350,
            "height": 350,
            "annotations": [
                {
                    "font": {
                        "size": 15
                    },
                    "showarrow": False,
                    "text": "Locations",
                },
            ]
        }
    }
    plot_div = plotly.offline.plot(fig, output_type="div", include_plotlyjs=False)
    return plot_div


def make_company_donut_chart(dataframe):
    dict = dataframe.iloc[0, 5]
    salaries = list(map(str, (dict.keys())))
    count = list(map(str, (dict.values())))
    fig = {
        "data": [
            {
                "values": count,
                "labels": salaries,
                "text":salaries,
                "showlegend": False,
                'textposition': 'outside',
                "textfont": {
                    "size": 10,
                },
                "name": "",
                "hoverinfo": "label+percent+name",
                "hole": .7,
                "type": "pie"
            },
            ],
        "layout": {
            "title": "",
            "width": 350,
            "height": 350,
            "annotations": [
                {
                    "font": {
                        "size": 15
                    },
                    "showarrow": False,
                    "text": "Companies",
                },
            ]
        }
    }
    plot_div = plotly.offline.plot(fig, output_type="div", include_plotlyjs=False)
    return plot_div


def make_job_type_donut_chart(dataframe):
    dict = dataframe.iloc[0, 7]
    salaries = list(map(str, (dict.keys())))
    count = list(map(str, (dict.values())))
    fig = {
        "data": [
            {
                "values": count,
                "labels": salaries,
                "text":salaries,
                'textposition': 'outside',
                "textfont": {
                    "size": 10,
                },
                "name": "",
                "showlegend": False,
                "hoverinfo": "label+percent+name",
                "hole": .7,
                "type": "pie"
            },
            ],
        "layout": {
            "title": "",
            "width": 350,
            "height": 350,
            "annotations": [
                {
                    "font": {
                        "size": 15
                    },
                    "showarrow": False,
                    "text": "Job Types",
                    # "x": 0.1,
                    # "y": 0.1
                },
            ]
        }
    }
    plot_div = plotly.offline.plot(fig, output_type="div", include_plotlyjs=False)
    return plot_div












def scrape_salaries(job_title):
    job_count = 0

    print("\nSearching for ", job_title, " jobs in 48 US states...\n")

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

    job_data_matrix = [[0 for x in range(9)] for y in range(2)]
    job_title = job_title.replace(" ", "+")   # format the job title so that it can be directly inserted into the indeed url
    job_title = job_title.replace("&", "%26")   # format the job title so that it can be directly inserted into the indeed url

    salary_list = []
    salary_dict = collections.OrderedDict()

    location_dict = collections.OrderedDict()
    company_dict = collections.OrderedDict()
    experience_level_dict = collections.OrderedDict()
    job_types_dict = collections.OrderedDict()

    for state in range(1):

        global state_abbreviation
        state_abbreviation = state_abbreviations_list[state]
        state_name = state_full_names_list[state]
        url = "https://www.indeed.com/jobs?q=title%3A" + str(job_title) + "&l=" + "usa"+ "&radius=50&start=0"

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
        salary_dict = collections.OrderedDict()
        location_dict = collections.OrderedDict()
        company_dict = collections.OrderedDict()
        experience_level_dict = collections.OrderedDict()
        job_types_dict =collections.OrderedDict()

    return job_data_matrix

def format_job_title(job_title, exact_match=True):
    if exact_match:
        job_title = '"' + job_title + '"'
    return job_title

def locations_to_ordered_dict(li,dict):
    li = li.get_text()
    li = li.replace("\n", "")
    li = li.split("(")
    location = li[0]
    location = location[:-1]
    count = li[1]
    count = count[:-1]
    dict[location] = count


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