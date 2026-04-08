
#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

# Search CrossRef without parentheses
query = "Using the camera to unbind memory Effects of photo-taking on memory for objects in a scene"
encoded_query = urllib.parse.quote(query)
url = f"https://api.crossref.org/works?query={encoded_query}&rows=5"

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.load(response)
    for item in data['message']['items']:
        if 'author' not in item:
            continue
        print(f"Title: {item['title'][0]}")
        print(f"DOI: {item['DOI']}")
        authors_list = []
        for a in item['author']:
            authors_list.append(f"{a.get('given','')} {a.get('family','')}")
        print(f"Authors: {', '.join(authors_list)}")
        if 'published' in item:
            print(f"Year: {item['published']['date-parts'][0][0]}")
        container = item.get('container-title', [''])[0] if item.get('container-title') else ''
        print(f"Container: {container}")
        print(f"Volume: {item.get('volume', '')}")
        print(f"Page: {item.get('page', '')}")
        print()
