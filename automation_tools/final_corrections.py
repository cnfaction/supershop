import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Correct wrong category assignments from previous script
final_corrections = {
    10365: 'hoodies',   # Chrome Hearts Horseshoe Logo Hoodie - image confirmed it's a hoodie
    10208: 'pants',     # Jordan Jumpman Sweatpants - pants is correct, undo if wrongly changed
}

for p in products:
    if p['id'] in final_corrections:
        old = p['category']
        p['category'] = final_corrections[p['id']]
        print(f"ID {p['id']}: category {old} -> {p['category']} | {p['title']}")

# Quick verification of key items
check_ids = [10311, 10381, 10034, 10354, 10365, 10052, 10116]
print("\n--- Final Verification ---")
for p in products:
    if p['id'] in check_ids:
        print(f"ID {p['id']}: {p['title']} | brand={p['brand']} | cat={p['category']}")

output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
output += """
// Final Corrections Done
const DB_VERSION = 'v31_final_corrections';
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
print("\nSaved!")
