import re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('data.js','r',encoding='utf-8') as f:
    c = f.read()
m = re.search(r'const initialProducts = (\[.*?\]);', c, re.DOTALL)
ps = json.loads(m.group(1))
print("=== Products with 'Premium' in title ===")
count = 0
for p in ps:
    if 'Premium' in p.get('title',''):
        count += 1
        print(f"  {p['id']} (prod_{p['id']-10000}): title='{p['title']}', brand='{p['brand']}', cat='{p['category']}'")
print(f"\nTotal Premium products: {count}")
print(f"\n=== Products needing attention (category=general) ===")
gen_count = 0
for p in ps:
    if p.get('category') == 'general':
        gen_count += 1
        print(f"  {p['id']} (prod_{p['id']-10000}): title='{p['title']}', brand='{p['brand']}'")
print(f"\nTotal general category: {gen_count}")
