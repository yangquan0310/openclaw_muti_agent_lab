
#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

# Soeller & Benjamin 2021 Memory & Cognition volume 49 pages 543-555
# DOI pattern: 10.3758/s13428-XXXX-XXXX
# Actually 10.3758/s13421-...

for num in range(1100, 1250):
    doi = f"10.3758/s13421-020-{num}-z"
    url = f"https://api.crossref.org/works/{doi}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.load(response)
            item = data['message']
            authors_list = []
            if 'author' in item:
                for a in item['author']:
                    authors_list.append(f"{a.get('given','')} {a.get('family','')}")
            if 'published' not in item:
                continue
            year = item['published']['date-parts'][0][0]
            if year != 2021:
                continue
            print(f"===== DOI: {doi} =====")
            print(f"Title: {item['title'][0]}")
            print(f"Authors: {', '.join(authors_list)}")
            print(f"Year: {year}")
            container = item.get('container-title', [''])[0] if item.get('container-title') else ''
            print(f"Container: {container}")
            print(f"Volume: {item.get('volume', '')}")
            print(f"Page: {item.get('page', '')}")
            print()
    except Exception as e:
        continue
