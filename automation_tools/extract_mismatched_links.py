import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

synonyms = {
  "sneakers": ["shoes", "footwear", "sneaker", "dunk", "jordan", "slide", "b30"],
  "pants": ["jeans", "shorts", "sweatpants", "trousers", "bottoms", "pants"],
  "hoodie": ["hoodies", "fleece", "sweatshirt", "zip"],
  "jackets": ["jacket", "puffer", "parka", "windbreaker", "coat"],
  "t-shirt": ["tshirts", "tees", "polo", "shirts"]
}

targets = []
for p in products:
    title_lower = p['title'].lower()
    cat = p.get('category', '').lower()
    
    expected_cat = None
    for k, words in synonyms.items():
        if any(w in title_lower for w in words):
            expected_cat = k
            break
            
    if expected_cat:
        is_match = (cat == expected_cat) or (cat in synonyms.get(expected_cat, []))
        if not is_match:
            targets.append(p)
    elif any('\u4e00' <= char <= '\u9fff' for char in p['title']) or '?' in p['title']:
        # Also catch remaining chinese/broken
        targets.append(p)

print(f"Total Targets: {len(targets)}")
for p in targets:
    print(f"{p['id']}| {p['link']}")
