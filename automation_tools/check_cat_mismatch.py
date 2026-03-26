import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

mismatches = []
# 定义简单的分类核对逻辑
rules = {
    "sneakers": ["shoe", "sneaker", "dunk", "jordan", "tn", "max", "slide", "b30"],
    "pants": ["pant", "jean", "short", "trousers", "sweatpants"],
    "hoodie": ["hoodie", "zip", "fleece", "sweatshirt"],
    "jackets": ["jacket", "puffer", "parka", "vest", "windbreaker"],
    "t-shirt": ["tee", "t-shirt", "shirt", "polo"]
}

for p in products:
    title_lower = p['title'].lower()
    cat = p.get('category', '').lower()
    
    found_match = False
    expected_cat = None
    
    for key, keywords in rules.items():
        if any(kw in title_lower for kw in keywords):
            expected_cat = key
            if key == cat:
                found_match = True
            break
    
    # 如果标题里有明显的品类词，但 category 不一致，记下来
    if expected_cat and not found_match:
        mismatches.append({
            "id": p['id'],
            "title": p['title'],
            "category": cat,
            "expected_from_title": expected_cat,
            "link": p['link']
        })

print(f"Found {len(mismatches)} obvious category-title mismatches.")
for m in mismatches[:20]:
    print(f"ID {m['id']}: Title '{m['title']}' is categorized as '{m['category']}' (Expected: {m['expected_from_title']})")
