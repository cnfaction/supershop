import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

for i, p in enumerate(products):
    if p.get('title') == "Gucci Ace Sneaker 'Bee'":
        print(json.dumps(p, indent=2, ensure_ascii=False))
        break
