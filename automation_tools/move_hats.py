import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

hat_keywords = ['hat', 'cap', 'beanie', 'toque']
updated_count = 0

for p in products:
    if p.get('category') == 'accessories':
        title = p.get('title', '').lower()
        if any(k in title for k in hat_keywords):
            p['category'] = 'hats'
            updated_count += 1
            print(f"Moved to hats: {p['title']}")

if updated_count > 0:
    json_str = json.dumps(products, indent=4, ensure_ascii=False)
    new_text = text.replace(res.group(1), json_str)
    
    db_search = re.search(r"const DB_VERSION = '(.*?)';", new_text)
    if db_search:
        old_ver = db_search.group(1)
        new_text = new_text.replace(f"'{old_ver}'", "'v48_move_hats'")
        
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f"\nSuccessfully moved {updated_count} hats/beanies/caps to the 'hats' category and bumped DB version.")
else:
    print("No hats found in accessories to move.")
