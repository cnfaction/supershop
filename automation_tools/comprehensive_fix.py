import os
import json
import re

# File Paths
data_js_path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
images_root = 'c:/Users/Administrator/Desktop/新建文件夹/网站/p_images'

# 1. Build a map of filenames on disk to fix SKU corruption
# Key: prod_id -> list of actual filenames
disk_map = {}
for prod_dir in os.listdir(images_root):
    if prod_dir.startswith('prod_'):
        full_path = os.path.join(images_root, prod_dir)
        if os.path.isdir(full_path):
            disk_map[prod_dir] = os.listdir(full_path)

# 2. Read data.js
with open(data_js_path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# 3. Process products
fixed_count_titles = 0
fixed_count_skus = 0

keywords = {
    'hoodie': ['卫衣', '连帽', 'hoodie'],
    'shoe': ['鞋', 'sneaker', 'shoe', '滑板'],
    'pant': ['裤', 'pant', 'jeans'],
    'jacket': ['外', 'jacket', 'puffer'],
    'bag': ['包', 'bag'],
    'watch': ['表', 'watch'],
    'shirt': ['衫', 'shirt', 'polo']
}

for p in products:
    # A. Fix Mismatched Titles
    title = p.get('title', '').lower()
    desc = p.get('description', '').lower()
    
    # Extract original title from description if possible
    # "Product imported from ...."
    orig_title_match = re.search(r'Product imported from (.*)', p.get('description', ''), re.IGNORECASE)
    if orig_title_match:
        orig_title = orig_title_match.group(1).strip()
        
        # Check for mismatch
        has_mismatch = False
        for eng, chn_list in keywords.items():
            if eng in title:
                # If title says "Hoodie" but description says "Shoes"
                for other_eng, other_chn_list in keywords.items():
                    if other_eng != eng:
                        for chn in other_chn_list:
                            if chn in orig_title.lower():
                                has_mismatch = True
                                break
                    if has_mismatch: break
            if has_mismatch: break
        
        if has_mismatch:
            # Restore title to original (clean up some common crap first)
            p['title'] = orig_title.replace('?', '').strip()
            fixed_count_titles += 1

    # B. Fix SKU Image Paths
    if 'images' in p:
        new_images = []
        for img_path in p['images']:
            # If path contains '?' it's definitely broken
            if '?' in img_path:
                parts = img_path.split('/')
                if len(parts) >= 3:
                    prod_dir = parts[1] # e.g. "prod_140"
                    corrupted_file = parts[2] # e.g. "SKU_?36.jpg"
                    
                    # Try to find a match in disk_map
                    if prod_dir in disk_map:
                        # Find the file that looks MOST like this one
                        # SKU is usually unique enough per product.
                        # Pattern: starts with "SKU_" and ends with length/chars after corruption
                        # We compare the prefix "SKU_" and the suffix (after the first ?)
                        
                        # Example: SKU_?36.jpg -> prefix SKU_, suffix ;36.jpg
                        # We search for any file in disk_map[prod_dir] matching this
                        
                        found_best = None
                        prefix = "SKU_"
                        # Get suffix after the last '?'
                        suffix_match = re.search(r'.*\?(.*)', corrupted_file)
                        if suffix_match:
                            suffix = suffix_match.group(1)
                            for actual in disk_map[prod_dir]:
                                if actual.startswith(prefix) and actual.endswith(suffix):
                                    found_best = actual
                                    break
                        
                        if found_best:
                            new_images.append('p_images/' + prod_dir + '/' + found_best)
                            fixed_count_skus += 1
                        else:
                            # If not found, keep as is (maybe it's truly missing)
                            new_images.append(img_path)
                    else:
                        new_images.append(img_path)
                else:
                    new_images.append(img_path)
            else:
                new_images.append(img_path)
        p['images'] = new_images

    # Fix main 'image' field if it was broken too
    if 'image' in p and '?' in p['image']:
        # Try to use the first image from images array if we just fixed it
        if p['images'] and '?' not in p['images'][0]:
            p['image'] = p['images'][0]
        else:
            # Weidian case: maybe it's just '主图'
            parts = p['image'].split('/')
            if len(parts) >= 3:
                 prod_dir = parts[1]
                 if prod_dir in disk_map:
                     for actual in disk_map[prod_dir]:
                         if '主图' in actual or 'main' in actual.lower():
                             p['image'] = 'p_images/' + prod_dir + '/' + actual
                             break

print("Fixed Titles: " + str(fixed_count_titles))
print("Fixed SKU paths: " + str(fixed_count_skus))

# Write back
output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
output += """
// Sync with localStorage 
const DB_VERSION = 'v16_final_sync_restored';
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

with open(data_js_path, 'w', encoding='utf-8') as f:
    f.write(output)
