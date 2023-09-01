import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

START_IDX = 759
END_IDX = 765

MAPBOX_URL = os.getenv("MAPBOX_URL")
HASHED_EMAIL = os.getenv('HASHED_EMAIL')
POST_URL = os.getenv('POST_URL')

URL = "https://www.pathwaystoscience.org/programs.aspx?u=Undergrads*Fresh_Undergraduate+Students+-+First+Year&d=MED-_Medical+%26+Life+Sciences+(All)&d=ENG-Bioengineering_Bioengineering&d=ENG-Biomedical_Biomedical+Engineering&d=ENG-Chemistry_Chemistry&d=ENG-MaterialsSci_Materials+Science+%26+Engineering&d=TEC-Bioinformatics_Bioinformatics+%26+Genomics&d=TEC-BioTech_Biotechnology&d=SOC-PsychBehavSci_Psychology+%26+Behavioral+Sciences&submit=y&all=all"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser") # alternatives: html5lib, lxml (requires installation)

results = soup.find(id="MainContent_panel2")
# job_elements = results.find_all("div", class_="progigert", limit=END_IDX)
job_elements = results.find_all("div", class_="progigert")

def process_grade(gradelist):
    newlist = []
    for grade in gradelist:
        if grade == 'High School Students':
            newlist.append('\'9 (HS)\'')
            newlist.append('\'10 (HS)\'')
            newlist.append('\'11 (HS)\'')
            newlist.append('\'12 (HS)\'')
        elif grade == 'Undergraduates - First Year':
            newlist.append('\'Freshman (College)\'')
        elif grade == 'Undergraduates - Sophomore':
            newlist.append('\'Sophomore (College)\'')
        elif grade == 'Undergraduates - Junior':
            newlist.append('\'Junior (College)\'')
        elif grade == 'Undergraduates - Senior':
            newlist.append('\'Senior (College)\'')
    return newlist

def scrape_child(link_url, dict):
    childPage = requests.get(link_url)
    childSoup = BeautifulSoup(childPage.content, "html.parser")
    childResults = childSoup.find(class_="col-sm-7 text-left")
    
    title = childResults.find('h1').text
    dict['opp_name'] = title
    allText = childResults.findAll(string=True)
    grade_idx = -1
    try:
        grade_idx = allText.index('Academic Level:')
    except ValueError:
        pass
    des_idx = allText.index('Description:', grade_idx if grade_idx != -1 else 0)
    app_idx = -1
    try:
        app_idx = allText.index('Application Deadline:', des_idx)
    except ValueError:
        pass
    pi_idx = allText.index('Participating Institution(s):', app_idx if app_idx != -1 else des_idx)

    if grade_idx > -1:
        eligible_grades = allText[grade_idx+1 : des_idx]
        dict['Grade'] = process_grade(map(lambda x:x.strip(), eligible_grades))

    des_arr = allText[des_idx+1 : app_idx if app_idx != -1 else pi_idx]
    dict['Description'] = ''.join(des_arr)
    dict['app_deadline'] = 'N/A' if app_idx == -1 else allText[app_idx+1].strip()

    areas = childResults.find('span', style='font-size:8pt')
    areas = areas.findAll(string=True)
    dict['area_of_study'] = ','.join(areas)
    dict['Website'] = childResults.find('a', class_='btn btn-success')['href']

    
    print(title)
    # print(dict)

    # response = requests.post(POST_URL, data=dict)
    # print(response.json())
    print()


for i in range(START_IDX,len(job_elements)):
    job_element = job_elements[i]

    # we find a header
    if '#dedede' in job_element['style']:
        dict = {
            'hashedemail': HASHED_EMAIL,
            'opp_name': '',
            'Website': '',
            'Email': '',
            'area_of_study': '',
            'Institution': '',
            'Location': '',
            'opp_type': '',
            'Dates': '',
            'Grade': [],
            'Age': '',
            'app_deadline': '',
            'Stipend': '',
            'Description': '',
            'app_requirements': '',
            'latitude': None,
            'longitude': None,
            'specific_dates': ''
        }
        dict['Institution'] = job_element.find("h2").text.strip()
        dict['Location'] = job_element.find('span').text.strip(' ()')
        # get lat and lon
        response = requests.get(MAPBOX_URL, params={'location': dict['Location']})
        dict['latitude'] = response.json()['latitude']
        dict['longitude'] = response.json()['longitude']

        # process all children
        j = i+1
        while j < len(job_elements) and not '#dedede' in job_elements[j]['style']:
            if j == 760:
                j += 1
                continue

            link_url = job_elements[j].find_all("a")[0]['href']
            http_link_url = "https://www.pathwaystoscience.org/" + link_url
            
            print(i)
            print(j)
            print(http_link_url)
            scrape_child(http_link_url, dict.copy())
            j += 1
        i = j - 1
