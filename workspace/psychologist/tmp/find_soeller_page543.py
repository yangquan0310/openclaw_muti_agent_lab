
#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

# Memory & Cognition volume 49 2021, find article starting at 543
query = "issn:0090-502X volume:49 year:2021"
encoded_query = urllib.parse.quote(query)
url = f"https://api.crossref.org/works?query={encoded_query}&rows=100"

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.load(response)
    print(f"Scanning volume 49 2021 for article starting page 543...")
    print()
    for item in data['message']['items']:
        if 'author' not in item:
            continue
        if 'page' not in item:
            continue
        first_page = item['page'].split('-')[0]
        try:
            fp = int(first_page)
            if fp >= 540 and fp <= 550:
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
                print(f"Issue: {item.get('issue', '')}")
                print(f"Page: {item.get('page', '')}")
                print()
        except:
            continue
