import json
import re
import os

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

broken = []
for p in products:
    # check if primary image file actually exists on disk
    img_path = p.get('image', '')
    if img_path:
        full_path = os.path.join(os.getcwd(), img_path)
        if not os.path.exists(full_path):
            broken.append(p)

print(f"Total broken image items: {len(broken)}")
for b in broken[:5]:
    print(f"ID: {b['id']} | Title: {b['title']} | Path: {b['image']}")
