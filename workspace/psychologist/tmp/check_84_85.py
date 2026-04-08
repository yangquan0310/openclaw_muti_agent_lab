
#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

for num in range(84, 87):
    doi = f"10.1037/xap00000{num}"
    url = f"https://api.crossref.org/works/{doi}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.load(response)
            item = data['message']
            if 'issue' not in item:
                print(f"{doi}: no issue")
                continue
            print(f"DOI {doi}: issue = {item['issue']}")
            if item['issue'] == '3':
                print(f"  Title: {item['title'][0]}")
                authors_list = []
                for a in item['author']:
                    authors_list.append(f"{a.get('given','')} {a.get('family','')}")
                print(f"  Authors: {', '.join(authors_list)}")
                print(f"  Pages: {item.get('page', '')}")
            print()
    except Exception as e:
        print(f"{doi}: ERROR {e}")
        print()
