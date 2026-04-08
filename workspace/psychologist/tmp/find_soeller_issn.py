
#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

# ISSN 0090-502X for Memory & Cognition
query = "issn:0090-502X volume:49 year:2021 \"Soeller\""
encoded_query = urllib.parse.quote(query)
url = f"https://api.crossref.org/works?query={encoded_query}&rows=30"

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.load(response)
    print(f"Found items: {data['message']['items'].__len__()}")
    print()
    for item in data['message']['items']:
        if 'author' not in item:
            continue
        if 'published' not in item:
            continue
        print(f"-----")
        print(f"Title: {item['title'][0]}")
        print(f"DOI: {item['DOI']}")
        authors_list = []
        for a in item['author']:
            authors_list.append(f"{a.get('given','')} {a.get('family','')}")
        print(f"Authors: {', '.join(authors_list)}")
        print(f"Year: {item['published']['date-parts'][0][0]}")
        container = item.get('container-title', [''])[0] if item.get('container-title') else ''
        print(f"Container: {container}")
        print(f"Volume: {item.get('volume', '')}")
        print(f"Page: {item.get('page', '')}")
        print()
