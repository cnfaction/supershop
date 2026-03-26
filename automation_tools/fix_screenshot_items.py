import json
import os

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Direct fixes from image inspection
direct_fixes = {
    10311: {
        'title': 'Gucci Rhyton GG Canvas Sneaker',
        'brand': 'Gucci',
        'category': 'shoes'
    },
    10381: {
        'title': 'Golden Goose Running Dad Sneaker',
        'brand': 'Golden Goose',
        'category': 'shoes'
    },
}

updated = 0
for p in products:
    if p['id'] in direct_fixes:
        fix = direct_fixes[p['id']]
        p['title'] = fix['title']
        p['brand'] = fix['brand']
        p['category'] = fix['category']
        updated += 1
        print(f"Fixed ID {p['id']}: -> {fix['title']} | {fix['brand']}")

# Also check: sneaker-titled products that are in wrong category
# "shoes" and "sneakers" are separate categories - normalize them
cat_fixes = 0
for p in products:
    title_lower = p['title'].lower()
    cat = p.get('category', '')
    # If title mentions hoodie/sweatshirt/zip but category is shoes, that's wrong
    is_shoe_title = any(w in title_lower for w in ['sneaker', 'shoe', 'dunk', 'air max', 'jordan', 'trainer', 'running dad', 'vomero', 'tn ', 'air force', 'spiridon', 'vapormax', 'gel-', 'slide', 'slipper', 'loafer', 'boot'])
    is_hoodie_title = any(w in title_lower for w in ['hoodie', 'sweatshirt', 'zip-up hoodie', 'full-zip hoodie'])
    
    if is_hoodie_title and cat == 'shoes':
        print(f"WARN: ID {p['id']} has hoodie title but category=shoes: {p['title']}")
    if is_shoe_title and cat in ['hoodies', 'jackets', 'pants', 'bags']:
        print(f"WARN: ID {p['id']} has sneaker title but category={cat}: {p['title']}")

print(f"\nTotal fixed: {updated}")

output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
output += """
// Screenshot Fix
const DB_VERSION = 'v29_screenshot_fix';
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
print("Saved!")
