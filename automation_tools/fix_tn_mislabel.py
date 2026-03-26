import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

updated = False
for p in products:
    if p['id'] == 10090 or p['title'] == "Nike SB Dunk Low 'UNC'":
        p['title'] = "Nike Air Max Plus TN Collection"
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
        new_text = new_text.replace(f"'{old_ver}'", f"'v57_fix_tn_collection'")

    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Updated mislabeled Nike TN Collection.")
else:
    print("Product not found.")
