import re
import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Step 1: Extract all product objects { ... }
# Use a regex that matches from { to } balancing them roughly
# Or just find all blocks between { and } that have "id":
products = []
raw_products = re.findall(r'\{[^{}]*?\"id\":.*?\n\s+\}', text, re.DOTALL)
# This might fail for nested objects. 
# But our products are simple objects with nested arrays (and no nested objects).

if not raw_products:
    # Use a more aggressive regex if needed
    # Let's find each '{' that starts a product and search for the closing '}'
    pass

# Actually, I'll just use a smarter one
product_blocks = []
current_pos = 0
while True:
    start = text.find('{', current_pos)
    if start == -1: break
    
    # Check if it has an id inside
    id_pos = text.find('"id":', start)
    if id_pos != -1 and id_pos < start + 100: # it is a product start
        # Find closing brace
        brace_count = 0
        end_pos = start
        while end_pos < len(text):
            if text[end_pos] == '{': brace_count += 1
            elif text[end_pos] == '}': 
                brace_count -= 1
                if brace_count == 0:
                    break
            end_pos += 1
        product_blocks.append(text[start:end_pos+1])
        current_pos = end_pos + 1
    else:
        current_pos = start + 1

print("Found blocks: " + str(len(product_blocks)))

# Step 2: For each block, try to fix it. 
# Many blocks might have missing quotes at line ends.
fixed_products = []
for block in product_blocks:
    # A product should have id, title, brand, category, price, image, images, link, description
    # We will use Regex to extract these values even if quotes are missing or garbled
    def get_val(key, default=''):
        m = re.search(r'\"' + key + r'\":\s*(.*?)[,\n]', block)
        if m:
            val = m.group(1).strip()
            # Clean up quotes
            if val.startswith('"'): val = val[1:]
            if val.endswith('"'): val = val[:-1]
            return val
        return default

    # Handling arrays (images)
    imgs_match = re.search(r'\"images\":\s*\[(.*?)\]', block, re.DOTALL)
    imgs = []
    if imgs_match:
        raw_imgs = imgs_match.group(1).split(',')
        for img in raw_imgs:
            img = img.strip()
            if img.startswith('"'): img = img[1:]
            if img.endswith('"'): img = img[:-1]
            if img: imgs.append(img)
            
    p_id = get_val('id')
    title = get_val('title')
    brand = get_val('brand')
    category = get_val('category')
    price = get_val('price', '0')
    image = get_val('image')
    link = get_val('link')
    description = get_val('description')
    
    # Rebuild a clean object
    p = {
        "id": int(float(p_id)) if p_id else 0,
        "title": title,
        "brand": brand,
        "category": category,
        "price": float(price) if price else 0,
        "image": image,
        "images": imgs,
        "link": link,
        "description": description
    }
    fixed_products.append(p)

print("Rebuilt " + str(len(fixed_products)) + " products.")

output = "const initialProducts = " + json.dumps(fixed_products, indent=2, ensure_ascii=False) + ";"
output += """
// Sync with localStorage 
const DB_VERSION = 'v15_final_recovery';
try {
    const val = localStorage.getItem('db_version');
    if (val !== DB_VERSION) {
        localStorage.setItem('products', JSON.stringify(initialProducts));
        localStorage.setItem('db_version', DB_VERSION);
    }
} catch (e) {
    console.warn(e);
}

function getProducts() {
    try {
        const stored = localStorage.getItem('products');
        if (stored) return JSON.parse(stored);
    } catch (e) {}
    return initialProducts;
}

function saveProducts(products) {
    try {
        localStorage.setItem('products', JSON.stringify(products));
    } catch (e) {}
}
"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(output)
