import requests
import bibtexparser
from pprint import pprint
import json
import sys
import re
from keys import notion_api_key, databases_id

if __name__ == '__main__':
    args = sys.argv

filename = args[1]

with open(filename) as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

bib_data = bib_database.entries[0]

def get_request_url(end_point):
    return f'https://api.notion.com/v1/{end_point}'
  

headers = {"Authorization": f"Bearer {notion_api_key}",
           "Content-Type": "application/json",
           "Notion-Version": "2022-06-28"}

author_names = bib_data['author'].split('and')
authors = []
for name in author_names:
  tmp = re.split('[.,]',name)
  if(len(tmp[0])>len(tmp[-1])):
    tmp = tmp[0].replace(' ','')
  else:
    tmp = tmp[-1].replace(' ','')
  authors.append(tmp)
# pprint(bib_data['author'])


body = {
    "parent": {
        "database_id": databases_id},
    "properties": {
        "Name": {"title": [
            {"text": {"content": f"{authors[0]}{bib_data['year']}"}}
        ]
        },
        "Authors": {
					"multi_select": [
						{"name": author} for author in authors
					]
				},
				"First": {
					"select": {
						"name": f"{authors[0]}"
					}
				},
    }}

if('journal' in bib_data):
  body['properties']['Journal'] = {
					"select": {
						"name": bib_data['journal']
					}
				}
if('title' in bib_data):
  body['properties']['Title'] = {
					'rich_text': [{
						"text": {"content": f"{bib_data['title']}"}
					}]
				}
if('year' in bib_data):
  body['properties']['Year'] = {
					'number': int(bib_data['year'])
				}
if('doi' in bib_data):
  body['properties']['DOI'] = {
					'url': bib_data['doi']
				}
if('volume' in bib_data):
  body['properties']['Volume'] = {
					'rich_text': [{
						"text": {"content": f"{bib_data['volume']}"}
					}]
				}
if('number' in bib_data):
  body['properties']['Issue'] = {
					'rich_text': [{
						"text": {"content": f"{bib_data['number']}"}
					}]
				}
if('pages' in bib_data):
  body['properties']['Pages'] = {
					'rich_text': [{
						"text": {"content": f"{bib_data['pages']}"}
					}]
				}
if('publisher' in bib_data):
  body['properties']['Publisher'] = {
					"select": {
						"name": f"{bib_data['publisher']}"
					}
				}
if('url' in bib_data):
  body['properties']['URL'] = {
    "url": bib_data['url']
				}


response = requests.request('POST', url=get_request_url('pages'), headers=headers, data=json.dumps(body))

pprint(response.json())
print(authors)