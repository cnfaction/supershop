import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract inner JSON
res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

# Update item 10353
for p in products:
    if p['id'] == 10353:
        p['category'] = 'accessories'
        break

# Generate new JSON
json_str = json.dumps(products, indent=4, ensure_ascii=False)

# Replace the block
new_text = text.replace(res.group(1), json_str)

# Bump DB Version
db_search = re.search(r"const DB_VERSION = '(.*?)';", new_text)
if db_search:
    old_ver = db_search.group(1)
    new_text = new_text.replace(f"'{old_ver}'", "'v51_fix_general_category'")

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Saved data.js. Lego Millennium Falcon moved to accessories.")
