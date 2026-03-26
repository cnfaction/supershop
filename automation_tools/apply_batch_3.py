import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Batch 3 Fixes
fixes = {
  "10392": "Hellstar Flame Logo Mesh Shorts",
  "10391": "FOG Essentials Sweat Shorts with Logo",
  "10110": "Stone Island Compass Patch Crewneck Sweatshirt",
  "10233": "Stone Island Classic Logo Patch Sweatshirt",
  "10343": "Alo Yoga Heavyweight Embossed Logo Full-Zip Hoodie",
  "10183": "National Team Quarter-Zip Football Training Kit",
  "10075": "Alo Yoga Jisoo Collection Half-Zip Pullover",
  "10263": "Chrome Hearts x NY Yankees Logo Zip Hoodie",
  "10191": "Stussy 8 Ball & Dice Logo Crewneck Sweatshirt",
  "10201": "Corteiz Alcatraz Logo Hoodie & Sweatpants Set",
  "10167": "Polo Ralph Lauren Half-Zip Cotton Knit Sweater",
  "10208": "Jordan Essentials Fleece Sweatpants",
  "10224": "Vlone Friends Mosaic Logo Hoodie",
  "10318": "Purple Brand Distressed Logo Hoodie & Sweatpants Set",
  "10372": "LV Artistic Print Leather Wallet",
  "10344": "Adidas F50 Elite AG Soccer Cleats",
  "10355": "Gallery Dept. Painted Flare & Splatter Sweatpants",
  "10377": "FOG Essentials Classic Sweatpants & Hoodie Set",
  "10073": "Nike Air Max 95 Classic Sneakers",
  "10082": "Nike Cushion Crew Socks",
  "10317": "Stone Island Lightweight Water-Repellent Windbreaker Jacket",
  "10347": "Nike Air Max Plus TN Sneakers",
  "10169": "Burberry Vintage Check Sneakers",
  "10330": "Purple Brand Slim-Fit Distressed Denim Jeans",
  "10316": "FOG Essentials Sweat Shorts",
  "10295": "Cactus Jack x FC Barcelona 24/25 Home Jersey",
  "10300": "Retro Football Jersey Collection - AC Milan & Arsenal & Croatia",
  "10299": "Real Madrid 24/25 Home Jersey",
  "10346": "Zadig & Voltaire Rock Wings Leather Crossbody Bag",
  "10390": "Luxurious Geometric Patterned Messenger Bag"
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
const DB_VERSION = 'v18_naming_fix_v2';
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
