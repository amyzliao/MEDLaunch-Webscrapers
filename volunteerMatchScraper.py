import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
import os
from dotenv import load_dotenv

load_dotenv()

MAPBOX_URL = os.getenv("MAPBOX_URL")
HASHED_EMAIL = os.getenv('HASHED_EMAIL')
POST_URL = os.getenv('POST_URL')

def process_requirements(requirements, dict):
    if type(requirements) is list:
        if 'Must be at least 18' in requirements:
            dict['Age'] = '>18'
        elif 'Must be at least 17' in requirements:
            dict['Age'] = '>17'
        elif 'Must be at least 16' in requirements:
            dict['Age'] = '>16'
        elif 'Must be at least 15' in requirements:
            dict['Age'] = '>15'
        elif 'Must be at least 14' in requirements:
            dict['Age'] = '>14'
        elif 'Must be at least 13' in requirements:
            dict['Age'] = '>13'
        return ''.join(requirements)
    elif requirements == 'N/A':
        return ''
    else:
        raise Exception('ayo wtf happened here')

def scrape_opp_page(url, dict):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="content_opp_details")
    description = list(results.find(id='short_desc').strings)
    description = '\n'.join(description).strip()
    info = results.find("div", class_='logistics logistics--box text-sm')
    areas = info.find('div', class_='logistics__causes-list').text.split(',')
    areas = list(map(lambda a: a.strip(' \n'), areas))
    specific_dates = info.find('div', class_='para').text.strip()
    req_section = info.find('section', class_='logistics__section logistics__section--requirements')
    requirements = req_section.find('ul', class_='list')
    if requirements:
        requirements = list(requirements.strings)
        requirements = process_requirements(requirements, dict)
    else:
        requirements = req_section.find('p').text.strip()
        requirements = process_requirements(requirements, dict)

    dict['Description'] = description
    dict['area_of_study'] = ','.join(areas)
    dict['specific_dates'] = specific_dates
    dict['app_requirements'] = requirements

    
    # print(dict)
    print(dict['opp_name'])
    response = requests.post(POST_URL, data=dict)
    print(response.json())
    print()

# scrape_opp_page('https://www.volunteermatch.org/search/opp3572788.jsp')

def scrape_search_results(url):
    browser = webdriver.Chrome()
    browser.get(url)

    print(browser.title)
    print()
    
    browser.implicitly_wait(1)

    result = browser.find_element(By.CSS_SELECTOR, 'div.pub-srp-opps')
    job_elements = result.find_elements(By.TAG_NAME, 'li')
    
    for i,job in enumerate(job_elements):
        # if i == 0:
        #     continue
        dict = {
            'hashedemail': HASHED_EMAIL,
            'opp_name': '',
            'Website': '',
            'Email': '',
            'area_of_study': '',
            'Institution': '',
            'Location': '',
            'opp_type': 'Volunteering',
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
        title = job.find_element(By.TAG_NAME, 'span').text.encode('ascii', 'ignore').decode('ascii')
        institution = job.find_element(By.CSS_SELECTOR, 'a.ga-track-to-org-profile').text
        location = job.find_element(By.CSS_SELECTOR, 'div.pub-srp-opps__loc').text
        website = job.find_element(By.CSS_SELECTOR, 'a.ga-track-to-opp-details')
        website_url = website.get_attribute('href')

        dict['opp_name'] = title
        dict['Institution'] = institution
        dict['Website'] = website_url
        dict['Location'] = location
        response = requests.get(MAPBOX_URL, params={'location': dict['Location']})
        dict['latitude'] = response.json()['latitude']
        dict['longitude'] = response.json()['longitude']
        
        print(i)
        scrape_opp_page(website_url, dict)
        

    browser.quit()

# scrape_search_results('https://www.volunteermatch.org/search/?l=Chicago%2C+IL%2C+USA&cats=11&v=true&r=region&opp=3572788')
# scrape_search_results('https://www.volunteermatch.org/search/?l=Chicago%2C+IL%2C+USA&cats=11&v=true&r=region&p=2')
# scrape_search_results('https://www.volunteermatch.org/search/?l=Chicago%2C+IL%2C+USA&cats=11&v=true&r=region&p=3')
# scrape_search_results('https://www.volunteermatch.org/search/?l=Chicago%2C+IL%2C+USA&cats=11&v=true&r=region&p=4')
# scrape_search_results('https://www.volunteermatch.org/search/?l=Chicago%2C+IL%2C+USA&cats=11&v=true&r=region&p=5')

