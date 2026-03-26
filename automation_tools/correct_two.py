import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract inner JSON
res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

# Update items
for p in products:
    t = p.get('title', '')
    if "Prada Cloudbust Thunder 'Grey'" in t:
        p['title'] = 'Yeezy Slide Collection'
        p['brand'] = 'Yeezy'
        p['category'] = 'shoes'
        print(f"Updated {t} to Yeezy Slide Collection")
    elif "Prada Nylon Gabardine Tracksuit" in t:
        p['title'] = 'Fear of God Essentials Sweatpants'
        p['brand'] = 'Fear of God Essentials'
        p['category'] = 'pants'
        print(f"Updated {t} to Essentials Sweatpants")

# Generate new JSON
json_str = json.dumps(products, indent=4, ensure_ascii=False)

# Replace the block
new_text = text.replace(res.group(1), json_str)

# Bump DB Version
db_search = re.search(r"const DB_VERSION = '(.*?)';", new_text)
if db_search:
    old_ver = db_search.group(1)
    new_text = new_text.replace(f"'{old_ver}'", "'v50_fix_prada_errors'")

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Saved data.js with upated items and bumped DB version.")
