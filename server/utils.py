import os
from dotenv import load_dotenv
import requests

load_dotenv()

claude_api_key = os.getenv('CLAUDE_API_KEY')

def fetch_patent_grants(keywords):
    url = "https://developer.uspto.gov/ibd-api/v1/application/grants"
    params = {
        "searchText": keywords,
        "start": 0,
        "rows": 10
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get('results', [])
        patents = []
        for result in results:
            patent = {
                'patent_number': result.get('patentApplicationNumber'),
                'title': result.get('inventionTitle'),
                'abstract': result.get('abstractText', [''])[0],
                'url': result.get('filelocationURI')
            }
            patents.append(patent)
        return patents
    else:
        return None

def search_case_law(keywords):
    url = f'https://api.harvard.edu/federal-patent-caselaw?query={" ".join(keywords)}'
    headers = {
        'Authorization': 'Bearer your_harvard_api_key'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []


