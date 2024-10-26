import re

from curl_cffi import requests

from src.utils import print_flushed as print
from src.models import Project
from src.field_parsers import parse_currency, parse_amount
from src import scrape_functions

# TODO: move to better scraping API!
def main():
    # TODO: add projects that have 'starting in ... days'
    url = 'https://www.conda.ch/projekte-entdecken/'
    data_to_extract = {
        'name':                 r'<meta\W+property=\"og:title\"\W+content=\"(.*?)\"',
        'name_short':           r'<meta\W+property=\"og:title\"\W+content=\"(.*?)\"',
        'external_link':        r'<meta\W+property=\"og:url\"\W+content=\"(.*?)\"',
        'external_image_link':  r'<meta\W+property=\"og:image\"\W+content=\"(.*?)\"',
        'funding_current':      r"<p class=\"conda-knob-value-text\".*?>(.*?CHF)</p>",
        'funding_min':          r"Mindestinvestition:(\W+CHF\W+\d*?\.[\-\d])",
        'funding_target':       lambda bfs: scrape_functions.text_from_class(bfs, 'p', 'total-amount'),
        'description':          r"<p class=\"text-white large italic text-shadow-dark\">(.*?)</p>",
        'description_short':    r"<p class=\"text-white large italic text-shadow-dark\">(.*?)</p>",
    }

    session = requests.Session(impersonate="chrome")

    result = session.get(url)
    if result.status_code != 200:
        print(f"WARNING: got status_code {result.status_code} on site '{result.url}'")
        return []
    html_project_page = result.content.decode(result.encoding)
    
    regex_projects_urls = r'<a href="(https://www\.conda\.ch/kampagne/.*?)"\s+target="_self"\s+class="i-btn'
    project_urls = re.findall(regex_projects_urls, html_project_page, re.MULTILINE)

    projects = []

    print(project_urls)
    
    for i, project_url in enumerate(project_urls):

        result = session.get(project_url)
        if result.status_code != 200:
            print(f"WARNING: got status_code {result.status_code} on site '{result.url}'")
            continue
        html = result.content.decode(result.encoding)
        print(html)
        
        data = scrape_functions.extract_all(data_to_extract, html)
        
        data['location'] = "Switzerland"
        currency = parse_currency(data['funding_min'])
        data['currency'] = currency
        data['funding_min'] = parse_amount(data['funding_min'])
        data['funding_current'] = parse_amount(data['funding_current'])
        data['funding_target'] = parse_amount(data['funding_target'])
        
        project = Project(**data)
        projects.append(project)

    return projects
