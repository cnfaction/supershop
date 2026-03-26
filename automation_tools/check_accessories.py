import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

acc_items = [p for p in products if p.get('category') == 'accessories']
print(f"Total accessories: {len(acc_items)}")
for p in acc_items:
    print(f"ID {p['id']}: {p['title']}")
