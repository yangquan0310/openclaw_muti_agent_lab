
#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

doi = "10.1037/xap0000086"
url = f"https://api.crossref.org/works/{doi}"

req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req) as response:
        data = json.load(response)
        item = data['message']
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
except Exception as e:
    print(f"Error: {e}")
