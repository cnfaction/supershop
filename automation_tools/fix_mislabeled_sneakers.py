import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

# Mapping of ID -> Fixed Data
corrections = {
    10292: {"title": "DC Shoes Court Graffik (Black/Pink)", "brand": "DC"},
    10305: {"title": "Nike Air Max 97 Triple Black", "brand": "Nike"},
    10328: {"title": "Prada America's Cup Sneaker (Pink/Grey)", "brand": "Prada"},
    10078: {"title": "LV Trainer Collection", "brand": "Louis Vuitton"}
}

updated = False
for p in products:
    if p['id'] in corrections:
        p['title'] = corrections[p['id']]['title']
        p['brand'] = corrections[p['id']]['brand']
        updated = True

if updated:
    json_str = json.dumps(products, indent=4, ensure_ascii=False)
    new_text = text.replace(res.group(1), json_str)

    # Bump DB Version
    db_search = re.search(r"const DB_VERSION = '(.*?)';", new_text)
    if db_search:
        old_ver = db_search.group(1)
        new_text = new_text.replace(f"'{old_ver}'", "'v56_fix_sneaker_mislabels'")

    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Updated 4 mislabeled sneakers and bumped DB_VERSION.")
else:
    print("No products found for update.")
