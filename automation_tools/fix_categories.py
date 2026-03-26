import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Fix the remaining category warnings
category_fixes = {
    10354: 'hoodies',     # Denim Tears Cotton Wreath Hoodie -> was shoes, should be hoodies
    10358: 'hoodies',     # Denim Tears Cotton Wreath Hoodie -> was shoes, should be hoodies
    10052: 'shoes',       # Nike Air Force 1 -> was pants, should be shoes
    10221: 'pants',       # Jordan Basketball Shorts -> pants is fine (shorts are pants)
    10058: 'bags',        # Louis Vuitton Shoe Trunk Case -> bags is fine (it's a case)
    10116: 'shoes',       # Nike Air Max 90 -> was hoodies, should be shoes
    10365: 'shoes',       # Chrome Hearts Horseshoe Logo Hoodie but image is shoes - need to check
    10208: 'pants',       # Jordan Jumpman Sweatpants -> pants is correct
    10150: 'shoes',       # ASICS Gel-Kayano -> was pants, should be shoes
}

# Check ID 10365 image first
for p in products:
    if p['id'] == 10365:
        print(f"10365: {p['title']} | {p['category']} | {p['image']}")

cat_updated = 0
for p in products:
    if p['id'] in category_fixes:
        old_cat = p['category']
        p['category'] = category_fixes[p['id']]
        if old_cat != p['category']:
            cat_updated += 1
            print(f"Fixed category ID {p['id']}: {old_cat} -> {p['category']} | {p['title']}")

print(f"\nCategories fixed: {cat_updated}")

output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
output += """
// Category + Title Final Fix
const DB_VERSION = 'v30_category_fix';
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
