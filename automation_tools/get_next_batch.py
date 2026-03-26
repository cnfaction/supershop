import json
import re

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

targets = []
for p in products:
    title = p.get('title', '')
    is_chinese = any('\u4e00' <= char <= '\u9fff' for char in title)
    is_corrupted = '?' in title or '\ufffd' in title
    is_generic = title.startswith('Premium ')
    
    if is_chinese or is_corrupted or is_generic:
        targets.append(p)

print("Targets Left: " + str(len(targets)))
# Export next 30 as a clean list
next_30 = targets[:30]
for p in next_30:
    print(str(p['id']) + "| " + p['title'] + "| " + p['link'])
