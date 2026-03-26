import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Batch 4 Fixes
fixes = {
  "10174": "Corteiz RTW All World Reservation Reflective Hoodie",
  "10018": "Nike Sportswear Tech Fleece Full-Zip Hoodie (FB8017)",
  "10031": "Burberry Check Swim Shorts",
  "10172": "Nike Elite Basketball Backpack",
  "10206": "Burberry Check Windbreaker Jacket",
  "10324": "Comme des Garçons PLAY Heart Logo Half-Zip Sweatshirt",
  "10212": "C.P. Company Goggle Lens Hooded Sweatshirt",
  "10026": "Amiri Gothic Logo Leather Belt",
  "10219": "Saint Laurent Script Logo Mohair Sweater",
  "10336": "Stone Island Logo Patch Full-Zip Hoodie",
  "10249": "BAPE College Big Ape Head T-Shirt",
  "10248": "Casablanca Tennis Club Printed T-Shirt",
  "10253": "Burberry Equestrian Knight Buckle Leather Belt",
  "10232": "Comme des Garçons PLAY Red Heart Hoodie",
  "10200": "Corteiz RTW HMP Hoodie and Tracksuit Collection",
  "10002": "Santos FC 2012-2013 Home Jersey Neymar Jr #11",
  "10368": "Corteiz Alcatraz Logo Full-Zip Hoodie and Sweatpants Set",
  "10221": "Air Jordan Diamond Basketball Shorts",
  "10283": "Chrome Hearts Embroidered Trucker Hat",
  "10242": "Gucci GG Supreme Leather Belt with G Buckle",
  "10373": "Rimowa Style Aluminum Alloy Carry-On Suitcase",
  "10386": "Canada Goose Freestyle Puffer Vest and Down Jacket Collection",
  "10029": "Burberry Equestrian Knight Logo Full-Zip Hoodie",
  "10213": "Polo Ralph Lauren Pony Logo Hoodie and Tracksuit Collection",
  "10165": "BAPE Shark Full-Zip Camo Hoodie",
  "10327": "Nike AeroSwift Lightweight Running Pants",
  "10374": "Acne Studios Stockholm 1996 Long Sleeve T-Shirt",
  "10143": "Murtaya Baggy Sweat Shorts",
  "10247": "Dior Oblique Monogram T-Shirt and Shorts Set",
  "10310": "Chanel CC Logo Knitted Beanie Hat"
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
const DB_VERSION = 'v19_naming_fix_v3';
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
