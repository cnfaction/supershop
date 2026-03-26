import json
import re

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

keywords = {
    'hoodie': ['卫衣', '连帽'],
    'shoe': ['鞋'],
    'pant': ['裤'],
    'jacket': ['外'],
    'bag': ['包'],
    'watch': ['表']
}

mismatches = []
for p in products:
    title = p.get('title', '').lower()
    desc = p.get('description', '').lower()
    
    found_mismatch = False
    for eng, chn_list in keywords.items():
        # If English keyword is in title
        if eng in title:
            # Check if ANY other Chinese keyword is in description
            for other_eng, other_chn_list in keywords.items():
                if other_eng != eng:
                    for chn in other_chn_list:
                        if chn in desc:
                            found_mismatch = True
                            break
                if found_mismatch: break
        if found_mismatch: break
    
    if found_mismatch:
        mismatches.append(p)

print("Found " + str(len(mismatches)) + " potential mismatches.")
for p in mismatches[:10]:
    print("Product " + str(p['id']) + ": " + p['title'] + " | " + p['description'])
