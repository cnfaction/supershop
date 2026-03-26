import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

prices = [30.28, 25.00, 17.50, 67.78]
for p in products:
    if p['price'] in prices or p['title'] in ["Dior B23 Low-Top 'Oblique'", "Nike Air Max Plus TN Black/Volt", "Hermes Oran Sandals Gold/White", "Nike x Sacai VaporWaffle 'Royal Fuchsia'"]:
        print(p['id'], p['title'], p['price'], p['brand'])
