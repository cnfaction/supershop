import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Fix the 14 remaining mismatches
fixes = {
    10135: 'Mixed Luxury',
    10051: 'Carhartt',
    10314: 'Fear of God',
    10109: 'Stussy',
    10348: 'Moncler',   # "Moncler x Valentino" - Moncler is primary brand
    10077: 'BAPE',
    10023: 'Saint Laurent',
    10149: 'New Balance',
    10332: 'Adidas',
    10380: 'Louis Vuitton',
    10078: 'BAPE',
    10132: 'Apple',
    10096: 'Nike',      # "Nike Stussy" collab - Nike is the shoe brand
    10144: 'New Balance',
}

updated = 0
for p in products:
    if p['id'] in fixes:
        p['brand'] = fixes[p['id']]
        updated += 1

print(f"Fixed {updated} brand mismatches.")

output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
output += """
// Brand Audit Complete
const DB_VERSION = 'v28_brand_audit_done';
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
