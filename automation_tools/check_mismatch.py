import re
import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Extract products (assuming current data.js is valid JSON array)
# Since I used json.dumps, I can find the start and end
start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

mismatches = 0
for p in products:
    orig_title_match = re.search(r'Product imported from (.*)', p.get('description', ''))
    if orig_title_match:
        orig_title = orig_title_match.group(1).strip()
        # Very loose check: if title is English but original title is Chinese and doesn't match conceptually
        # But wait, we don't know the concept.
        # Let's check for 'shoe' vs 'hoodie'
        title = p.get('title', '').lower()
        orig = orig_title.lower()
        
        # If title contains 'hoodie' but orig contains '鞋' (shoe)
        if 'hoodie' in title and '鞋' in orig:
            print("Mismatch for Product " + str(p['id']) + ":")
            print("  Current Title: " + p['title'])
            print("  Original Title in Desc: " + orig_title)
            mismatches += 1

print("Total mismatches found: " + str(mismatches))
