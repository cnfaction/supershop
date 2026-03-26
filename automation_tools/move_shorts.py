import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

short_keywords = ['short', 'shorts']
updated_count = 0

for p in products:
    if p.get('category') == 'pants':
        title = p.get('title', '').lower()
        # Find exact word matches for 'short' or 'shorts' to avoid matching 'shorter' if there is any mapping but it's safe
        if any(re.search(fr'\b{k}\b', title) for k in short_keywords):
            p['category'] = 'shorts'
            updated_count += 1
            print(f"Moved to shorts: {p['title']}")

if updated_count > 0:
    json_str = json.dumps(products, indent=4, ensure_ascii=False)
    new_text = text.replace(res.group(1), json_str)
    
    db_search = re.search(r"const DB_VERSION = '(.*?)';", new_text)
    if db_search:
        old_ver = db_search.group(1)
        # Bump the version
        new_text = new_text.replace(f"'{old_ver}'", "'v49_move_shorts'")
        
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f"\nSuccessfully moved {updated_count} shorts to the 'shorts' category and bumped DB version.")
else:
    print("No shorts found in pants to move.")
