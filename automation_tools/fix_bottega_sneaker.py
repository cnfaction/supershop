import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

updated = False
for p in products:
    if p['title'] == "Givenchy City Court Canvas Sneakers" and p['price'] == 67.78:
        p['title'] = "Bottega Veneta Orbit Sneaker (Silver/Green)"
        p['brand'] = "Bottega Veneta"
        updated = True
        break

if updated:
    json_str = json.dumps(products, indent=4, ensure_ascii=False)
    new_text = text.replace(res.group(1), json_str)

    db_search = re.search(r"const DB_VERSION = '(.*?)';", new_text)
    if db_search:
        old_ver = db_search.group(1)
        new_text = new_text.replace(f"'{old_ver}'", "'v54_fix_bottega_sneaker'")

    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Updated mislabeled Bottega Orbit sneaker.")
else:
    print("Product not found.")
