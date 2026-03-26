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
    # Check for '?' or other corruption indicators (excluding legitimate punctuation)
    is_corrupted = '?' in title
    is_generic = title.startswith('Premium ')
    
    if is_chinese or is_corrupted or is_generic:
        targets.append({
            "id": p['id'],
            "title": title,
            "link": p['link']
        })

print("Found " + str(len(targets)) + " products that need naming fix.")
for t in targets:
    print(str(t['id']) + "| " + t['title'] + "| " + t['link'])
