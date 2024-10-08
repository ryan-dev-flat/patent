import os
from dotenv import load_dotenv
import requests

load_dotenv()

# Access the API key

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
        if not patents:
            print(f"No patents found for keywords: {keywords}")
        return patents
    else:
        print(f"Error fetching patents: {response.status_code} - {response.text}")
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
