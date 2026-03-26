import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# 手心修正截图中的严重错误及相关漂移项
manual_fixes = {
    "10034": ("Balenciaga Track Sneaker 'Graffiti'", "Balenciaga"),
    "10056": ("Derschutze Sakura Embroidery Jeans", "Derschutze"),
    "10033": ("Gucci Screener GG Canvas Sneaker", "Gucci"),
    "10234": ("Canada Goose Puffer Jacket Collection", "Canada Goose"),
}

updated = 0
for p in products:
    pid_str = str(int(p['id']))
    if pid_str in manual_fixes:
        p['title'], p['brand'] = manual_fixes[pid_str]
        updated += 1

print(f"Manually fixed {updated} critical items.")

output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
# 保存版本
output += """
// Global Alignment Sync 
const DB_VERSION = 'v23_manual_mismatch_fix';
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
