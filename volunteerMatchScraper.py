import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
import re

CATEGORY = 'Volunteering'
STIPEND = 0

def scrape_opp_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="content_opp_details")
    description = results.find(id='short_desc').text.strip()
    info = results.find("div", class_='logistics logistics--box text-sm')
    areas = info.find('div', class_='logistics__causes-list').text.split(',')
    areas = list(map(lambda a: a.strip(' \n'), areas))
    specific_dates = info.find('div', class_='para').text.strip()
    req_section = info.find('section', class_='logistics__section logistics__section--requirements')
    requirements = req_section.find('ul', class_='list')
    if requirements:
        requirements = requirements.text.strip()
    else:
        requirements = req_section.find('p').text.strip()

    # print(results)
    print("DESCRIPTION")
    print(description)
    print("AREAS OF STUDY")
    print(areas)
    print("SPECIFIC DATES")
    print(specific_dates)
    print("REQUIREMENTS")
    print(requirements)

# scrape_opp_page('https://www.volunteermatch.org/search/opp3572788.jsp')

def scrape_search_results(url):
    browser = webdriver.Chrome()
    browser.get(url)

    print(browser.title)
    print()
    
    browser.implicitly_wait(1)

    result = browser.find_element(By.CSS_SELECTOR, 'div.pub-srp-opps')
    job_elements = result.find_elements(By.TAG_NAME, 'li')
    
    for job in job_elements:
        title = job.find_element(By.TAG_NAME, 'span')
        institution = job.find_element(By.CSS_SELECTOR, 'a.ga-track-to-org-profile')
        location = job.find_element(By.CSS_SELECTOR, 'div.pub-srp-opps__loc')
        website = job.find_element(By.CSS_SELECTOR, 'a.ga-track-to-opp-details')
        website_url = website.get_attribute('href')

        print("NAME")
        print(title.text)
        print('INSTITUTION')
        print(institution.text)
        print('LOCATION')
        print(location.text)
        print('WEBSITE')
        print(website_url)
        scrape_opp_page(website_url)

        print()

    browser.quit()

scrape_search_results('https://www.volunteermatch.org/search/?l=Chicago%2C+IL%2C+USA&cats=11&v=true&r=region&opp=3572788')