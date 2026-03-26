import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

updated = False
for p in products:
    if p['id'] == 10077 or p['title'] == "A Bathing Ape Bape Sta 'White/Blue'":
        p['title'] = "LV Skate Sneaker Collection"
        p['brand'] = "Louis Vuitton"
        updated = True
        break

if updated:
    json_str = json.dumps(products, indent=4, ensure_ascii=False)
    new_text = text.replace(res.group(1), json_str)

    # Bump DB Version
    db_search = re.search(r"const DB_VERSION = '(.*?)';", new_text)
    if db_search:
        old_ver = db_search.group(1)
        new_text = new_text.replace(f"'{old_ver}'", f"'v59_fix_lv_skate_sneaker'")

    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Updated mislabeled LV Skate Sneaker Collection.")
else:
    print("Product not found.")
