import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract inner JSON
res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

# Update item 10339
for p in products:
    if p['id'] == 10339:
        p['title'] = 'Gucci Original GG Canvas Baseball Cap'
        p['brand'] = 'Gucci'
        p['category'] = 'hats'
        break

# Generate new JSON
json_str = json.dumps(products, indent=4, ensure_ascii=False)

# Replace the block
new_text = text.replace(res.group(1), json_str)

# Bump DB Version
db_search = re.search(r"const DB_VERSION = '(.*?)';", new_text)
if db_search:
    old_ver = db_search.group(1)
    new_text = new_text.replace(f"'{old_ver}'", "'v47_fix_gucci_cap'")

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Saved data.js with upated item 10339 (Gucci Cap) and bumped DB version.")
