
#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

# Journal of Experimental Psychology: Applied volume 22 issue 3
# article starting at 304 ending 313
# authors: Benjamin C. Storm, Sean M. Stone, Aaron S. Benjamin

query = "issn:1076-898x volume:22 issue:3 year:2016"
encoded_query = urllib.parse.quote(query)
url = f"https://api.crossref.org/works?query={encoded_query}&rows=30"

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.load(response)
    print(f"Scanning all articles in Volume 22 Issue 3 2016...")
    print()
    articles = []
    for item in data['message']['items']:
        if 'author' not in item:
            continue
        if 'published' not in item:
            continue
        if 'page' not in item:
            continue
        first_page = item['page'].split('-')[0]
        try:
            fp = int(first_page)
            articles.append((fp, item))
        except:
            continue
    
    # sort by first page
    articles.sort(key=lambda x: x[0])
    for fp, item in articles:
        print(f"----- Page {fp} -----")
        print(f"DOI: {item['DOI']}")
        authors_list = []
        for a in item['author']:
            authors_list.append(f"{a.get('given','')} {a.get('family','')}")
        print(f"Authors: {', '.join(authors_list)}")
        print(f"Title: {item['title'][0]}")
        print(f"Pages: {item.get('page', '')}")
        print()
