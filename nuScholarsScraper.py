from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
import requests
from bs4 import BeautifulSoup

# TODO: scrape other pages of the site
# TODO: something that explains that this is a prof entry, not smth to apply for
institution = 'Northwestern University'

def scrape_profile(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(class_="page-section page-section-persons page-section-persons-view")
    role_parts = results.find(class_= 'rendering rendering_person rendering_personorganisationlistrendererportal rendering_person_personorganisationlistrendererportal').next_element.children
    role_formatted = '\n'.join([r.text for r in role_parts])
    subheaders = results.find_all('h3', class_='subheader')
    bio = ''
    for subheader in subheaders:
        if subheader.text == 'Research Interests':
            bio = "\n\n" + subheader.next_sibling.text

    description = role_formatted + bio
    print("DESCRIPTION")
    print(description)


# scrape_profile('https://www.scholars.northwestern.edu/en/persons/abdul-aziz-aadam')

def scrape_search_results(url):
    browser = webdriver.Chrome()
    browser.get(url)

    print(browser.title)
    print()
    
    browser.implicitly_wait(0.5)

    result = browser.find_element(By.CLASS_NAME, 'grid-results')
    profiles = result.find_elements(By.CLASS_NAME, 'result-container')
    for profile in profiles:
        name = profile.find_element(By.CLASS_NAME, 'title')
        email = profile.find_element(By.CSS_SELECTOR, "li.email")
        area = profile.find_element(By.CSS_SELECTOR, "a.organisation")
        profile_link = profile.find_element(By.CSS_SELECTOR, 'a.person').get_attribute('href')
        print("NAME")
        print(name.text)
        print("EMAIL")
        print(email.text)
        print("AREA OF STUDY")
        print(area.text)
        print("LEARN MORE")
        print(profile_link)
        scrape_profile(profile_link)
        print()


    browser.quit()

scrape_search_results('https://www.scholars.northwestern.edu/en/persons/?organisationIds=5f66bfc7-2861-471b-a120-c74475eb4ece&organisationIds=e7f5e371-47f2-4b00-a0c6-49427c044d4c&organisationIds=a9de7138-8f4e-431d-9bb9-94ccbc472174&organisationIds=eaa5b65c-0be5-483c-b740-9cc4dfa6b446&organisationIds=ffc8e1ca-d39b-4af8-9b5e-10124c8d054f&organisationIds=76454e6c-ce94-4dc1-9511-2947f579c7e8&organisationIds=91e1a896-723d-4eb2-9897-c40a05fd522f&organisationIds=f1bcb1b4-c6f0-42e2-9c23-582a7a94f238&organisationIds=47ce2c48-c55a-44d4-9ec8-ed5adc151828&organisationIds=5288c465-330f-481d-b397-946a02531369&organisationIds=52a97471-462b-41d1-ac98-178f7e9a79d2&organisationIds=d20243f7-811b-4378-9a2a-c0844f61a483&organisationIds=32aa53e9-c5d7-4e58-b7e2-e8bfbceb4d39&organisationIds=9ef12178-15f4-46a4-bbcf-77d3e3677f0c&organisationIds=ed51cdf3-3097-4029-8968-7dda3ee4427b&organisationIds=9ef3e417-f62d-4e58-9624-635948c1e60b&organisationIds=6ef2176a-93fd-4584-8d18-10a066796c60&organisationIds=6a77f380-b8b3-4292-8c6f-ce091198c7cb&organisationIds=c11fc036-025b-4de2-83ba-fa4e0b8c2893&organisationIds=2c36a1cd-0bba-4b73-88f5-461639af224b&organisationIds=ff290e49-2c1a-4596-b67d-97e090d0a11a&organisationIds=927dacd4-5872-4646-93cf-d03ba4032ade&organisationIds=0c8f6c7f-b5b7-40c3-a2f5-a2bda67f6d7c&organisationIds=561489e3-2862-4590-9fc2-c71d8fb2fba2&nofollow=true&format=')

