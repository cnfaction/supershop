import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

# Corrections for the two mislabeled cards
corrections = {
    "Travis Scott x Air Jordan 1 Low Reverse Mocha": {
        "new_title": "New Balance 9060 Collection",
        "new_brand": "New Balance",
        "target_price": 43.06
    },
    "Adidas Samba OG Core Black": {
        "new_title": "Travis Scott x Air Jordan 1 Low Reverse Mocha",
        "new_brand": "Jordan",
        "target_price": 42.78
    }
}

updated = False
for p in products:
    title = p['title']
    price = p['price']
    
    if title in corrections and abs(price - corrections[title]["target_price"]) < 0.1:
        p['title'] = corrections[title]['new_title']
        p['brand'] = corrections[title]['new_brand']
        updated = True

if updated:
    json_str = json.dumps(products, indent=4, ensure_ascii=False)
    new_text = text.replace(res.group(1), json_str)

    db_search = re.search(r"const DB_VERSION = '(.*?)';", new_text)
    if db_search:
        old_ver = db_search.group(1)
        new_text = new_text.replace(f"'{old_ver}'", "'v55_fix_nb_ts_sneakers'")

    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Updated mislabeled NB 9060 and TS AJ1 Reverse Mocha.")
else:
    print("Products not found.")
