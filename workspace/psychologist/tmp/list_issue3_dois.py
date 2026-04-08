
#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

print("Scanning DOIs 10.1037/xap0000080 to 10.1037/xap0000093...")
print()

for num in range(80, 94):
    doi = f"10.1037/xap00000{num}"
    url = f"https://api.crossref.org/works/{doi}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.load(response)
            item = data['message']
            if 'issue' not in item:
                continue
            if item['issue'] != '3':
                continue
            # it's in issue 3!
            print(f"===== DOI: {doi} =====")
            print(f"Title: {item['title'][0]}")
            authors_list = []
            for a in item['author']:
                authors_list.append(f"{a.get('given','')} {a.get('family','')}")
            print(f"Authors: {', '.join(authors_list)}")
            print(f"Pages: {item.get('page', '')}")
            print()
    except Exception as e:
        continue
