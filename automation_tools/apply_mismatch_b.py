import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Batch B Fixes
fixes = {
  "10122": "Dior Saddle Messenger Bag",
  "10071": "Nike Air Zoom Vomero 5",
  "10293": "Louis Vuitton Nano Speedy (Denim Monogram)",
  "10095": "Prada Nylon Cargo Pants",
  "10104": "Stussy Hooded Puffer Jacket",
  "10361": "Corteiz Allstar Zip Hoodie",
  "10362": "Dior Oblique Zip Hoodie",
  "10113": "Syna World Shell Jacket",
  "10350": "Nike Tech Fleece Hoodie",
  "10054": "Denim Tears Cotton Wreath Tracksuit",
  "10289": "Hellstar Studios Tracksuit (Hoodie & Sweatpants)",
  "10088": "Nike Windbreaker Jacket",
  "10167": "Lacoste Quarter-Zip Knit Sweater",
  "10208": "Jordan Jumpman Sweatpants",
  "10318": "Purple Brand Hooded Sweatshirt & Flare Sweatpants Set",
  "10064": "Gallery Dept. Flare Sweatpants",
  "10096": "Nike Stussy Spiridon Cage 2 'Fossil'",
  "10377": "Prada Nylon Gabardine Tracksuit",
  "10117": "Louis Vuitton Water-Reactive Monogram Swim Shorts",
  "10343": "Alo Yoga Hooded Sweatshirt",
  "10074": "Stussy Jennie Kim Vintage Tee",
  "10183": "Football National Team Training Tracksuit",
  "10263": "American Vintage Washed Hoodie (Oversized)",
  "10231": "Corteiz Devil Print Tracksuit",
  "10142": "Ami Paris Heart Embroidered Sweater",
  "10138": "Retro Golden State Warriors Basketball Jersey",
  "10201": "Corteiz Alcatraz Tracksuit",
  "10006": "High-Street Zip-Back Sweatpants",
  "10191": "Stussy 8-Ball Dice Sweatshirt",
  "10079": "Louis Vuitton Monogram Belt",
  "10080": "Moncler Knit Beanie",
  "10238": "Polo Ralph Lauren Pony Logo Beanie"
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
const DB_VERSION = 'v22_severe_mismatch_b';
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
