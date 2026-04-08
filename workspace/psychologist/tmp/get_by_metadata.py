
#!/usr/bin/env python3
# Use CrossRef's mailblend API to get DOI from metadata
import urllib.request
import urllib.parse
import json

# Build query with known metadata
query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"container-title": "Journal of Experimental Psychology: Applied"}},
                {"match": {"volume": "22"}},
                {"match": {"issue": "3"}},
                {"match": {"author": "Storm"}},
                {"match": {"author": "Stone"}},
                {"match": {"author": "Benjamin"}},
            ]
        }
    }
}

# Actually we use simple query
url = "https://api.crossref.org/works?query=container-title%3A%22Journal%20of%20Experimental%20Psychology%3A%20Applied%22%20volume%3A22%20author%3AStorm%20author%3AStone%20author%3ABenjamin&rows=10"

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.load(response)
    print(f"Found {data['message']['total-results']} results")
    print()
    for item in data['message']['items']:
        if 'author' not in item:
            continue
        print(f"-----")
        print(f"Title: {item['title'][0]}")
        print(f"DOI: {item['DOI']}")
        authors_list = []
        for a in item['author']:
            authors_list.append(f"{a.get('given','')} {a.get('family','')}")
        print(f"Authors: {', '.join(authors_list)}")
        if 'published' in item:
            print(f"Year: {item['published']['date-parts'][0][0]}")
        print(f"Volume: {item.get('volume', '')}")
        print(f"Issue: {item.get('issue', '')}")
        print(f"Page: {item.get('page', '')}")
        print()
