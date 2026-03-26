import re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('data.js','r',encoding='utf-8') as f:
    c = f.read()
m = re.search(r'const initialProducts = (\[.*?\]);', c, re.DOTALL)
ps = json.loads(m.group(1))
for p in ps:
    if 'Premium' in p.get('title','') or p.get('category') == 'general':
        print(f"{p['id']}: {p['title']}, {p['images'][0]}")
