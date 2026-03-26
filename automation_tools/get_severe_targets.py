import json
import re

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

bad_targets = []
for p in products:
    title = p.get('title', '')
    is_chinese = any('\u4e00' <= char <= '\u9fff' for char in title)
    is_corrupted = '?' in title or '\ufffd' in title
    if is_chinese or is_corrupted:
        bad_targets.append(p)

print("Severe Targets Left: " + str(len(bad_targets)))
for p in bad_targets:
    print(str(p['id']) + "| " + p['title'] + "| " + p['link'])
