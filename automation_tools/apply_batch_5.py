import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Batch 5 Fixes
fixes = {
  "10363": "Polo Ralph Lauren Japan City Zip Hoodie",
  "10348": "Valentino V-Logo Puffer Jacket",
  "10388": "Moncler Maya Classic Down Jacket",
  "10121": "Vetements Logo Sweatpants",
  "10035": "Supreme x Umbro Track Jacket",
  "10044": "Corteiz Alcatraz Embroidered Hoodie",
  "10175": "Maison Margiela Replica Sneakers",
  "10013": "Balenciaga Explorer Graffiti Backpack",
  "10162": "C.P. Company Lens Flat Nylon Crossbody Bag",
  "10281": "Louis Vuitton Damier Ebene Multi Wallet",
  "10022": "Moncler Classic Hooded Puffer Jacket",
  "10229": "Burberry Detachable Hood Puffer Jacket",
  "10304": "Polo Ralph Lauren Hooded Puffer Jacket",
  "10108": "Supreme x Umbro Tracksuit",
  "10378": "Rick Owens DRKSHDW Drawstring Sweatpants",
  "10361": "Vetements Logo Zip-Up Hoodie",
  "10186": "Hellstar Pink Flame Flare Tracksuit",
  "10271": "C.P. Company Goggle Lens Hooded Puffer Jacket",
  "10153": "Nike Air Max Plus (TN) Sneakers",
  "10236": "Corteiz Velour Tracksuit"
}

updated_count = 0
for p in products:
    pid_str = str(int(p['id']))
    if pid_str in fixes:
        p['title'] = fixes[pid_str]
        updated_count += 1

print("Updated " + str(updated_count) + " products.")

output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
output += """
// Sync with localStorage 
const DB_VERSION = 'v20_naming_fix_final_severe';
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
