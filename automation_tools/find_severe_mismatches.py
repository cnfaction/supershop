import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# 定义更松散的同义词规则
synonyms = {
  "sneakers": ["shoes", "footwear", "sneaker", "dunk", "jordan", "slide"],
  "pants": ["jeans", "shorts", "sweatpants", "trousers", "bottoms"],
  "hoodie": ["hoodies", "fleece", "sweatshirt", "zip"],
  "jackets": ["jacket", "puffer", "parka", "windbreaker", "coat"],
  "t-shirt": ["tshirts", "tees", "polo", "shirts"]
}

severe_mismatches = []
for p in products:
    title_lower = p['title'].lower()
    cat = p.get('category', '').lower()
    
    expected_cat = None
    for k, words in synonyms.items():
        if any(w in title_lower for w in words):
            expected_cat = k
            break
            
    if expected_cat:
        # Check if cat matches either expected_cat or any of its synonyms
        is_match = (cat == expected_cat) or (cat in synonyms.get(expected_cat, []))
        if not is_match:
            severe_mismatches.append(p)

print(f"Severe Mismatches: {len(severe_mismatches)}")
for p in severe_mismatches[:30]:
    print(f"ID {p['id']}: {p['title']} | CAT: {p['category']}")
