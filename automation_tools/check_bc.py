import re

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

brands = re.findall(r'\"brand\": \"(.*?)\"', text)
bad_brands = [b for b in brands if '?' in b]
print("Total brands: " + str(len(brands)))
print("Broken brands: " + str(len(bad_brands)))
for b in bad_brands[:10]:
    print("  " + b)

categories = re.findall(r'\"category\": \"(.*?)\"', text)
bad_cats = [c for c in categories if '?' in c]
print("Total categories: " + str(len(categories)))
print("Broken categories: " + str(len(bad_cats)))
