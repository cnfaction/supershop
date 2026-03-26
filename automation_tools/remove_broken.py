import json
import re
import os

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract inner JSON
res = re.search(r'const initialProducts = (\[.*?\]);', text, re.DOTALL)
products = json.loads(res.group(1))

# Filter out the broken ID
filtered = [p for p in products if p['id'] != 10085]
print(f"Removed ID 10085. Old size: {len(products)}, new size: {len(filtered)}")

# Generate new JSON
json_str = json.dumps(filtered, indent=4, ensure_ascii=False)

# Replace the block
new_text = text.replace(res.group(1), json_str)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Saved data.js")
