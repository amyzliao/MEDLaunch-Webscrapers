# theprojectmed.org
# medlaunch.vercel.app
These are a set of webscrapers for various websites that provide listings of pre-med/pre-healthcare opportunities primarily for high school and college-aged students. These scrapers were built to populate ProjectMED's MEDLaunch database.
List of scrapers:
- HPAScraper scrapes https://www.northwestern.edu/health-professions-advising/experiences/explore-opportunities/
- nuScholarsScraper scrapes https://www.scholars.northwestern.edu/en/persons/
- pathwaysScraper scrapes search results from https://www.pathwaystoscience.org/programs.aspx
- volunteerMatchScraper scrapes https://www.volunteermatch.org/search/

## Reqs:
You should probably set up a python virtual env
install these
- requests `python -m pip install requests`
- beautiful soup `python -m pip install beautifulsoup4`
- [selenium](https://www.selenium.dev/)

## Setup:
```
git clone { url }
cd *into the medlaunch-webscrapers folder*
*if using virtual env* Scripts/activate
```

## Running webscrapers
Scrapers are named XXXScraper.py. XXXSite.html stores the output from running XXXScraper.py.
```
python XXXScraper.py > XXXSite.html
```