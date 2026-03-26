import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

updated = False
for p in products:
    if p['id'] == 10303 or p['title'] == "Christian Louboutin Louis Junior Spikes Sneaker":
        p['title'] = "Supreme x Nike Air Max 98 TL (Brown)"
        p['brand'] = "Nike"
        updated = True
        break

if updated:
    json_str = json.dumps(products, indent=4, ensure_ascii=False)
    new_text = text.replace(res.group(1), json_str)

    # Bump DB Version
    db_search = re.search(r"const DB_VERSION = '(.*?)';", new_text)
    if db_search:
        old_ver = db_search.group(1)
        new_text = new_text.replace(f"'{old_ver}'", f"'v58_fix_supreme_nike_98'")

    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Updated mislabeled Supreme x Nike Air Max 98 TL.")
else:
    print("Product not found.")
