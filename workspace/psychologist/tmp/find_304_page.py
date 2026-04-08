
#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

# Check all DOIs from 088 to 091 in order:
candidates = [
    "10.1037/xap0000088",
    "10.1037/xap0000089", 
    "10.1037/xap0000090",
    "10.1037/xap0000091",
    "10.1037/xap0000092",
    "10.1037/xap0000093",
    "10.1037/xap0000094",
]

for doi in candidates:
    url = f"https://api.crossref.org/works/{doi}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.load(response)
            item = data['message']
            print(f"DOI: {doi}")
            print(f"  Title: {item['title'][0]}")
            authors_list = []
            for a in item['author']:
                authors_list.append(f"{a.get('given','')} {a.get('family','')}")
            print(f"  Authors: {', '.join(authors_list)}")
            print(f"  Year: {item['published']['date-parts'][0][0]}")
            print(f"  Pages: {item.get('page', '')}")
            print()
    except Exception as e:
        print(f"DOI: {doi} - ERROR: {e}")
        print()
