import json
import re

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Skip the 40 I already fixed (not really needed since they won't match Chinese/corrupted anymore)
targets = []
for p in products:
    title = p.get('title', '')
    
    is_chinese = any('\u4e00' <= char <= '\u9fff' for char in title)
    is_corrupted = '?' in title or '\ufffd' in title
    is_generic = title.startswith('Premium ')
    
    if is_chinese or is_corrupted or is_generic:
        targets.append({
            "id": p['id'],
            "title": title,
            "link": p['link']
        })

print(json.dumps(targets, ensure_ascii=False))
