
#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

# Soeller & Benjamin 2021 Memory & Cognition 49(3): 543-555
# DOI pattern: 10.3758/s13421-020-[xxxx]

for num in range(1100, 1200):
    doi = f"10.3758/s13421-020-{num}"
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
            if int(item['volume']) != 49:
                continue
            if 'page' not in item:
                continue
            first_page = item['page'].split('-')[0]
            try:
                fp = int(first_page)
                if fp >= 540 and fp <= 550:
                    print(f"===== FOUND IT! =====")
                    print(f"DOI: {doi}")
                    print(f"Title: {item['title'][0]}")
                    authors_list = []
                    for a in item['author']:
                        authors_list.append(f"{a.get('given','')} {a.get('family','')}")
                    print(f"Authors: {', '.join(authors_list)}")
                    print(f"Pages: {item['page']}")
                    print()
            except:
                continue
    except Exception as e:
        continue
