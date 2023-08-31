import requests
from bs4 import BeautifulSoup

URL = "https://www.pathwaystoscience.org/programs.aspx?u=Undergrads*Fresh_Undergraduate+Students+-+First+Year&d=MED-_Medical+%26+Life+Sciences+(All)&d=ENG-Bioengineering_Bioengineering&d=ENG-Biomedical_Biomedical+Engineering&d=ENG-Chemistry_Chemistry&d=ENG-MaterialsSci_Materials+Science+%26+Engineering&d=TEC-Bioinformatics_Bioinformatics+%26+Genomics&d=TEC-BioTech_Biotechnology&d=SOC-PsychBehavSci_Psychology+%26+Behavioral+Sciences&submit=y&all=all"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser") # alternatives: html5lib, lxml (requires installation)

results = soup.find(id="MainContent_panel2")
job_elements = results.find_all("div", class_="progigert", limit=10)

def scrape_child(link_url):
    childPage = requests.get(link_url)
    childSoup = BeautifulSoup(childPage.content, "html.parser")
    childResults = childSoup.find(class_="col-sm-7 text-left")
    
    # eligible_grades: ['Academic Level:' : 'Description:']
    # descrpition: ['Description:' : 'Application Deadline:']
    # app_deadline: ['Application Deadline:' : 'Participating Institution(s):']
    allText = childResults.findAll(string=True)
    grade_idx = allText.index('Academic Level:')
    des_idx = allText.index('Description:', grade_idx)
    app_idx = -1
    try:
        app_idx = allText.index('Application Deadline:', des_idx)
    except ValueError:
        pass
    pi_idx = allText.index('Participating Institution(s):', app_idx if app_idx != -1 else des_idx)

    eligible_grades = allText[grade_idx+1 : des_idx]

    des_arr = allText[des_idx+1 : app_idx if app_idx != -1 else pi_idx]
    description = ''.join(des_arr)
    app_deadline = 'N/A' if app_idx == -1 else allText[app_idx+1]

    print("ELIGIBLE GRADES")
    print(eligible_grades)
    print("DESCRIPTION")
    print(description)
    print("APP DEADLINE")
    print(app_deadline)

    # areas of study
    # website
    areas = childResults.find('span', style='font-size:8pt')
    areasList = areas.findAll(string=True)
    website = childResults.find('a', class_='btn btn-success')['href']
    print("AREAS OF STUDY")
    print(areasList)
    print("WEBSITE")
    print(website)

    
for job_element in job_elements:
    # institution header
    if '#dedede' in job_element['style']:
        print()
        institution = job_element.find("h2")
        location = job_element.find('span')
        print(institution.text.strip())
        print(location.text.strip())
    # job listing
    else:
        link_url = job_element.find_all("a")[0]['href']
        http_link_url = "https://www.pathwaystoscience.org/" + link_url
        print(http_link_url)
        scrape_child(http_link_url)

    # print(job_element.encode('utf8'), end="\n"*2)
    
# print(results.text.encode('utf8'))
# print(results.text.encode('utf8'))
