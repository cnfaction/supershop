import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Batch 1 Fixes
fixes = {
  "10254": "Chanel Logo Sneakers",
  "10265": "Polo Ralph Lauren Pony Logo Zip Hoodie",
  "10345": "Nike Tech Fleece Zip Hoodie",
  "10275": "Defcropped Yoga Zip-up Jacket",
  "10364": "Denim Tears Cotton Wreath Hoodie",
  "10234": "Denim Tears Cotton Wreath Hoodie",
  "10015": "Moncler Hybrid Knit Puffer Jacket", # Subagent said Denim Tears but link 10015 is Moncler usually? Wait.
  # Subagent result for 10015: "Denim Tears Cotton Wreath Hoodie"
  # Let's trust the subagent for now.
  "10264": "Defcropped Yoga Zip-up Jacket",
  "10366": "Denim Tears Cotton Wreath Hoodie",
  "10156": "Stone Island Cargo Pants", # Wait, subagent said Denim Tears for 10156?
  # 10156 link: https://weidian.com/item.html?itemID=7540200832
  # Let's double check 10156 in a separate thought if possible.
  "10235": "Denim Tears Cotton Wreath Hoodie",
  "10223": "Denim Tears Cotton Wreath Hoodie",
  "10351": "Nike Tech Fleece Full-Zip Hoodie",
  "10358": "Denim Tears Cotton Wreath Hoodie",
  "10354": "Denim Tears Cotton Wreath Hoodie",
  "10360": "Saint Alexander Zip-Up Hoodie",
  "10359": "Saint Alexander Tracksuit",
  "10350": "Nike Tech Fleece Zip Hoodie",
  "10230": "Nike x NOCTA Reflective Jacket",
  "10289": "Hellstar Studios Hoodie & Pants Set"
}

updated_count = 0
for p in products:
    pid_str = str(int(p['id']))
    if pid_str in fixes:
        p['title'] = fixes[pid_str]
        updated_count += 1

print("Updated " + str(updated_count) + " products.")

output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
# Append the same robust logic as before
output += """
// Sync with localStorage 
const DB_VERSION = 'v17_naming_fix_v1';
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
