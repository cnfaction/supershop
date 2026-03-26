import re

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

descriptions = re.findall(r'\"description\": \"(.*?)\"', text)
bad_desc = [d for d in descriptions if '?' in d]
print("Total descriptions: " + str(len(descriptions)))
print("Broken descriptions: " + str(len(bad_desc)))
for d in bad_desc[:10]:
    print("  " + d)
