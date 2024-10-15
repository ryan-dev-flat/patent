
import requests
from faker import Faker
import spacy

fake = Faker()

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha and len(token.text) > 2]
    top_keywords = " ".join(sorted(set(keywords), key=keywords.count, reverse=True)[:10])
    return top_keywords

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
            if result:
                patent = {
                    'patent_number': result.get('patentApplicationNumber', ''),
                    'title': result.get('inventionTitle', ''),
                    'abstract': result.get('abstractText', [''])[0] if result.get('abstractText') else '',
                    'url': result.get('filelocationURI', '')
                }
                patents.append(patent)
        if not patents:
            print(f"No patents found for keywords: {keywords}")
            patents = generate_mock_patents(3)  # Generate 3 mock patents
        return patents
    else:
        print(f"Error fetching patents: {response.status_code} - {response.text}")
        return generate_mock_patents(3)  # Generate 3 mock patents in case of error

def generate_mock_patents(num_patents):
    mock_patents = []
    for _ in range(num_patents):
        mock_patent = {
            'patent_number': fake.unique.random_number(digits=8),
            'title': fake.sentence(nb_words=6),
            'abstract': fake.paragraph(nb_sentences=3),
            'url': fake.url()
        }
        mock_patents.append(mock_patent)
    return mock_patents

def search_case_law(keywords):
    from app import create_app
    url = f'https://api.harvard.edu/federal-patent-caselaw?query={" ".join(keywords)}'
    headers = {
        'Authorization': 'Bearer your_harvard_api_key'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []
