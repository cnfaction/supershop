import json
import re

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# 提取前 50 个 ID 和 Link 进行精准校对
batch_1 = products[:50]
for p in batch_1:
    print(f"{p['id']}|{p['link']}")
