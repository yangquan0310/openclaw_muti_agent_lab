
#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

query = "issn:1076-898x volume:22 issue:3 year:2016"
encoded_query = urllib.parse.quote(query)
url = f"https://api.crossref.org/works?query={encoded_query}&rows=20"

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.load(response)
    print(f"Volume 22 Issue 3 2016 articles:")
    print()
    i = 1
    for item in data['message']['items']:
        if 'author' not in item:
            continue
        if 'published' not in item:
            continue
        print(f"{i}. ")
        print(f"   Title: {item['title'][0]}")
        print(f"   DOI: {item['DOI']}")
        authors_list = []
        for a in item['author']:
            authors_list.append(f"{a.get('given','')} {a.get('family','')}")
        print(f"   Authors: {', '.join(authors_list)}")
        print(f"   Pages: {item.get('page', '')}")
        print()
        i += 1
