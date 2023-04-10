import requests
import pdf2doi
from pprint import pprint
import json
import sys
from keys import notion_api_key, databases_id

def get_doi_url(get_doi):
  return f'https://api.crossref.org/works/{get_doi}'

def get_request_url(end_point):
    return f'https://api.notion.com/v1/{end_point}'
  
if __name__ == '__main__':
    args = sys.argv

filename = args[1]

headers = {"Authorization": f"Bearer {notion_api_key}",
           "Content-Type": "application/json",
           "Notion-Version": "2022-06-28"}

pdf2doi.config.set('verbose',False)
doi_result = pdf2doi.pdf2doi(filename)

doi = doi_result['identifier']
response = requests.request('GET', url=get_doi_url(f'{doi}'))
json_load = response.json()

body = {
    "parent": {
        "database_id": databases_id},
    "properties": {
        "Name": {"title": [
            {"text": {"content": f"{json_load['message']['author'][0]['family']}{json_load['message']['issued']['date-parts'][0][0]}"}}
        ]
        },
        "Journal": {
					"select": {
						"name": f"{json_load['message']['container-title'][0]}"
					}
				},
        "Title": {
					# 'rich_text': f"{json_load['message']['title'][0]}"
					'rich_text': [
            {"text": {"content": f"{json_load['message']['title'][0]}"}}
        ]
				},
        "Year": {
					'number': json_load['message']['issued']['date-parts'][0][0]
				},
        "DOI": {
					'url': json_load['message']['DOI']
				},
				"First": {
					"select": {
						"name": f"{json_load['message']['author'][0]['family']}"
					}
				},
				"Volume": {
					'rich_text': [
            {"text": {"content": f"{json_load['message']['volume'][0]}"}}
					]
				},
				"Issue": {
					'rich_text': [
            {"text": {"content": f"{json_load['message']['issue'][0]}"}}
					]
				},
				"Publisher": {
					"select": {
						"name": f"{json_load['message']['publisher']}"
					}
				},
				"URL": {"url": 
						f"{json_load['message']['URL']}"
				},
    }}

response = requests.request('POST', url=get_request_url('pages'), headers=headers, data=json.dumps(body))

pprint(response.json())