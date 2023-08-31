import requests
from bs4 import BeautifulSoup

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
    for opp_element in opp_elements:
        title = opp_element.find('h2')
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

        print('TITLE')
        print(title.text)
        print("DESCRIPTION")
        print(description)
        # print(description.encode('utf8'))
        # print(''.join(description).text.encode('utf8'))
        print('WEBSITE')
        print(website)
        print("AREAS")
        print(areas)
        print("LOCATION")
        print(location)
        print('SPECIFIC DATES')
        print(specific_dates)
        print("CATEGORIES")
        print(categories)

        print()

scrape_opp_list('https://www.northwestern.edu/health-professions-advising/experiences/explore-opportunities/')