import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

# The corrections mapping based on visual identification and corresponding IDs
corrections = {
    10084: {"title": "Nike Air Max Plus", "brand": "Nike"},
    10193: {"title": "Hermes Oran Sandals", "brand": "Hermes"},
    10244: {"title": "BAPE Camo Clogs", "brand": "BAPE"},
    10091: {"title": "Prada America's Cup Sneakers", "brand": "Prada"}
}

for p in products:
    if p['id'] in corrections:
        p['title'] = corrections[p['id']]['title']
        p['brand'] = corrections[p['id']]['brand']

json_str = json.dumps(products, indent=4, ensure_ascii=False)
new_text = text.replace(res.group(1), json_str)

db_search = re.search(r"const DB_VERSION = '(.*?)';", new_text)
if db_search:
    old_ver = db_search.group(1)
    new_text = new_text.replace(f"'{old_ver}'", "'v52_rename_shoes_cards'")

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Updated mislabeled products and bumped DB_VERSION.")
