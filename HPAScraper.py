import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

MAPBOX_URL = os.getenv("MAPBOX_URL")
HASHED_EMAIL = os.getenv('HASHED_EMAIL')
POST_URL = os.getenv('POST_URL')

def process_areas(areas_list):
    if 'All' in areas_list:
        return ''
    return ','.join(areas_list)

def process_categories(categories_list):
    newList = []
    for cat in categories_list:
        if cat == 'Volunteer':
            newList.append('Volunteering')
        else:
            newList.append(cat)
    return ','.join(newList)

def format_p(p):
    p_parts = list(p.strings)
    p_parts = list(map(lambda x: x.encode('ascii', 'ignore').decode('ascii'), p_parts))
    p_whole = '\n'.join(p_parts)
    return p_whole

def scrape_opp_list(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="opportunity-content")
    # print(results.encode('utf8'))
    opp_elements = results.find_all('div', class_='opportunity')
    for i, opp_element in enumerate(opp_elements):
        if i == 0:
            continue
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
        title = opp_element.find('h2').text
        des_section = opp_element.find('div', class_='description')
        description = des_section.find_all('p', class_='')    
        description = list(map(format_p, description))
        description = ''.join(description)
        info = opp_element.find('ul', class_='two-column-list').children
        areas = ''
        location = ''
        specific_dates = ''
        categories = ''
        contact = ''
        for li in info:
            li_children = list(li.strings)
            if li_children[0].text == "Tracks:":
                areas = li_children[1:len(li_children)]
                areas = ''.join(areas).split(',')
                areas = list(map(lambda a: a.strip(), areas))
            if li_children[0].text == 'Location:':
                location = li_children[1:len(li_children)]
                location = ''.join(location).strip()
            if li_children[0].text == 'Start:':
                specific_dates = li_children[1:len(li_children)]
                specific_dates = ''.join(specific_dates).strip()
            if li_children[0].text == 'Position Type:':
                categories = li_children[1:len(li_children)]
                categories = ''.join(categories).split(',')
                categories = list(map(lambda a: a.strip(), categories))
            if li_children[0].text == 'Contact:':
                contact = li_children[1:len(li_children)]
                contact = ''.join(contact).strip()
        if contact != '':
            description = description + '\nCONTACT:\n' + contact
        link = opp_element.find('p', class_='arrow-link')
        website =''
        if link:
            website = link.find('a')['href']

        dict['opp_name'] = title
        dict['Description'] = description
        dict['Website'] = website
        dict['area_of_study'] = process_areas(areas)
        dict['specific_dates'] = specific_dates
        dict['opp_type'] = process_categories(categories)
        dict['Location'] = location
        if location != '':
            response = requests.get(MAPBOX_URL, params={'location': location})
            dict['latitude'] = response.json()['latitude']
            dict['longitude'] = response.json()['longitude']

        

        print(i)
        # print(dict)
        print(title)
        # post to database
        response = requests.post(POST_URL, data=dict)
        print(response.json())
        print()
        

scrape_opp_list('https://www.northwestern.edu/health-professions-advising/experiences/explore-opportunities/')