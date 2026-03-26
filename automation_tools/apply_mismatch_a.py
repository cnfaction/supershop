import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Batch A Fixes
fixes = {
  "10265": "Polo Ralph Lauren Zip-Up Hoodie",
  "10345": "Nike Tech Fleece Hoodie",
  "10099": "Nike Tech Fleece Suit",
  "10322": "Polo Ralph Lauren Cable-Knit Sweater",
  "10320": "Nike Sportswear Fleece Suit",
  "10157": "Moose Knuckles Fur-Trimmed Puffer Jacket",
  "10375": "Nike Dri-FIT Strike Training Suit",
  "10135": "Designer Knitwear Collection (Dior/LV/Celine)",
  "10056": "Derschutze Sakura Embroidery Jeans",
  "10051": "Carhartt Canvas Active Jacket",
  "10086": "New Balance 1906R Sneakers",
  "10336": "Stone Island Zip-Up Hoodie",
  "10050": "C.P. Company Hooded Puffer Jacket",
  "10133": "Stone Island Down Puffer Jacket",
  "10107": "ASICS GEL-NYC Sneakers",
  "10264": "Palm Angels Reflective Windbreaker",
  "10139": "Purple Brand Flared Distressed Jeans",
  "10156": "Valentino Born in Roma Intense Perfume",
  "10368": "Corteiz Alcatraz Tracksuit",
  "10221": "Jordan Mesh Basketball Shorts",
  "10213": "Polo Ralph Lauren Hoodie/Puffer Collection",
  "10306": "Nike Air Force 1 '07 Sneakers",
  "10154": "Chrome Hearts Cross Patch Waffle Henley",
  "10063": "Fendi Watermark Monogram Shorts",
  "10363": "Polo Ralph Lauren Big Pony Japan Hoodie",
  "10066": "Gucci GG Monogram Baseball Cap",
  "10109": "Stussy Graphic Tee Collection",
  "10061": "Fear of God Essentials 1977 Tee",
  "10348": "Moncler x Valentino Puffer Jacket",
  "10087": "New Balance 2002R Sneakers",
  "10141": "Derschutze Angel Print Jeans",
  "10137": "Scff Logo Hoodie",
  "10062": "Fear of God Essentials Hoodie",
  "10065": "Gymshark Training T-Shirt",
  "10081": "MCM Stark Monogram Backpack"
}

updated_count = 0
for p in products:
    pid_str = str(int(p['id']))
    if pid_str in fixes:
        p['title'] = fixes[pid_str]
        updated_count += 1

print(f"Updated {updated_count} products.")

output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
output += """
// Sync with localStorage 
const DB_VERSION = 'v21_severe_mismatch_a';
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
