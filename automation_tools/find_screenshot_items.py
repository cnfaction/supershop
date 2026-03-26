import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Find the two mismatched items
for p in products:
    if 'Louis Vuitton Trainer Sneaker White/Blue' in p['title']:
        print(f"LV Trainer: ID={p['id']} | Link={p['link']} | Image={p['image']} | Category={p['category']}")
    if 'Chrome Hearts Horseshoe Logo Hoodie' in p['title']:
        print(f"CH Hoodie: ID={p['id']} | Link={p['link']} | Image={p['image']} | Category={p['category']}")
