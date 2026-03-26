#!/usr/bin/env python3
"""
Comprehensive fix script for data.js product name, brand, and category mismatches.
This script fixes products where titles/brands/categories don't match the actual product images.
"""
import re
import json
import sys
import shutil
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# Read data.js
with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
backup_name = f'data.js.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
shutil.copy('data.js', backup_name)
print(f"Backup created: {backup_name}")

# Extract products
match = re.search(r'const initialProducts = (\[.*?\]);', content, re.DOTALL)
if not match:
    print("ERROR: Could not find initialProducts array")
    sys.exit(1)

products = json.loads(match.group(1))
print(f"Loaded {len(products)} products")

# Build lookup by ID
products_by_id = {p['id']: p for p in products}

# ============================================================================
# FIXES: Visually verified title/brand/category corrections
# ============================================================================

fixes = {
    # --- TITLE + BRAND + CATEGORY FIXES (image doesn't match title at all) ---
    
    # prod_23: Shows Air Jordan 11 collection, NOT Saint Laurent
    10023: {
        "title": "Air Jordan 11 Retro Collection",
        "brand": "Jordan",
        "category": "shoes"
    },
    
    # prod_89: Shows Nike Shox TL, NOT SB Dunk Low Panda
    10089: {
        "title": "Nike Shox TL Sneakers",
        "brand": "Nike",
        "category": "shoes"
    },
    
    # prod_134: Shows Football/Soccer Jerseys, NOT Balenciaga Track Sneaker
    10134: {
        "title": "Football Jersey Collection (PSG, Man United, Chelsea, Barcelona)",
        "brand": "Multi-Club",
        "category": "jerseys"
    },
    
    # prod_149: Shows Saint Laurent Court Classic SL/06, NOT NB 993
    10149: {
        "title": "Saint Laurent Court Classic SL/06 Handwritten Sneaker",
        "brand": "Saint Laurent",
        "category": "shoes"
    },
    
    # prod_158: Shows Birkenstock Arizona Sandals, NOT Stone Island Knit
    10158: {
        "title": "Birkenstock Arizona Suede Sandals",
        "brand": "Birkenstock",
        "category": "shoes"
    },
    
    # prod_331: Shows Christian Louboutin black suede high-top, NOT NB 9060
    10331: {
        "title": "Christian Louboutin Louis Junior High-Top Sneaker",
        "brand": "Christian Louboutin",
        "category": "shoes"
    },
    
    # prod_52: Shows Nike Sportswear Shorts, NOT Air Force 1
    10052: {
        "title": "Nike Tech Fleece Shorts",
        "brand": "Nike",
        "category": "shorts"
    },
    
    # prod_60: Shows Enfants Riches Déprimés (ERD) Hoodies, NOT Louboutin 
    10060: {
        "title": "Enfants Riches Déprimés Graphic Hoodie Collection",
        "brand": "ERD",
        "category": "hoodies"
    },
    
    # prod_93: Shows grey sweatpants (logo embroidered), title says Rick Owens shoes
    10093: {
        "title": "Logo Embroidered Drawstring Sweatpants",
        "brand": "Other",
        "category": "pants"
    },
    
    # prod_126: Shows luxury puffer jackets (Burberry-style), NOT Gucci Messenger Bag
    10126: {
        "title": "Luxury Hooded Puffer Jacket",
        "brand": "Other",
        "category": "jackets"
    },
    
    # prod_106: SKU files show NB 2002R colorways, NOT Bape Tee
    10106: {
        "title": "New Balance 2002R Sneaker Collection",
        "brand": "New Balance",
        "category": "shoes"
    },
    
    # --- BRAND-ONLY FIXES ---
    
    # prod_65: Image is Gymshark training shirt, brand says Balenciaga
    10065: {
        "brand": "Gymshark"
    },
    
    # prod_11: Title says Nike T-Shirt, brand says Other
    10011: {
        "brand": "Nike"
    },
    
    # --- CATEGORY-ONLY FIXES (title is correct but category is wrong) ---
    
    # prod_133: Stone Island Down Puffer Jacket → category should be jackets, not bags
    10133: {
        "category": "jackets"
    },
    
    # prod_161: Moncler Maglia Cardigan → category should be general/jackets, not bags
    10161: {
        "category": "jackets"
    },
    
    # prod_348: Moncler x Valentino Puffer Jacket → category should be jackets, not bags
    10348: {
        "category": "jackets"
    },
    
    # prod_144: New Balance 550 White/Grey → category should be shoes, not bags
    10144: {
        "category": "shoes"
    },
    
    # prod_147: New Balance 9060 'Rain Cloud' → category should be shoes, not jerseys
    10147: {
        "category": "shoes"
    },
    
    # prod_148: New Balance 990v3 Core Grey → category should be shoes, not jerseys
    10148: {
        "category": "shoes"
    },
    
    # prod_146: New Balance 1906R Silver Metallic → category should be shoes, not accessories
    10146: {
        "category": "shoes"
    },
    
    # prod_69: Nike Air Max Plus TN 'Voltage Purple' → category should be shoes, not electronics
    10069: {
        "category": "shoes"
    },
    
    # prod_68: Nike Air Max Plus TN 'Sunset Orange' → category should be shoes, not accessories
    10068: {
        "category": "shoes"
    },
    
    # prod_235: Denim Tears Cotton Wreath Hoodie → category should be hoodies, not bags
    10235: {
        "category": "hoodies"
    },
    
    # prod_125: Gucci Double G Buckle Leather Belt → category should be accessories, not jackets
    10125: {
        "category": "accessories"
    },
    
    # prod_132: Apple AirPods Pro → category should be electronics, not hoodies
    10132: {
        "category": "electronics"
    },
    
    # prod_119: Adidas Yeezy 700 V3 'Azael' → category should be shoes, not tshirts
    10119: {
        "category": "shoes"
    },
    
    # prod_120: Adidas Yeezy 500 'Utility Black' → category should be shoes, not hoodies
    10120: {
        "category": "shoes"
    },
    
    # prod_59: Christian Louboutin Louis Junior Spikes 'White' → should be shoes, not hoodies
    10059: {
        "category": "shoes"
    },
    
    # prod_242: Gucci GG Supreme Belt → should be accessories, not pants
    10242: {
        "category": "accessories"
    },
    
    # prod_26: Amiri Gothic Logo Leather Belt → should be accessories, not pants
    10026: {
        "category": "accessories"
    },
    
    # prod_152: Salomon XT-6 'Black Phantom' → should be shoes, not pants
    10152: {
        "category": "shoes"
    },
    
    # prod_313: Chrome Hearts Forever Spacer Ring → should be accessories, not shoes
    10313: {
        "category": "accessories"
    },
    
    # prod_315: Chrome Hearts Filigree Cross Pendant → should be accessories, not shoes
    10315: {
        "category": "accessories"
    },
    
    # prod_380: Louis Vuitton Keepall Bandouliere 50 Monogram → should be bags, not shoes
    10380: {
        "category": "bags"
    },
    
    # prod_83: Dior B23 High-Top 'Oblique' → should be shoes, not sets
    10083: {
        "category": "shoes"
    },
    
    # prod_362: Dior Oblique Zip Hoodie → should be hoodies, not accessories
    10362: {
        "category": "hoodies"
    },
    
    # prod_198: Polo Ralph Lauren Cardigan Sweater → should be general, not pants
    10198: {
        "category": "general"
    },
    
    # prod_62: Fear of God Essentials Hoodie → should be hoodies, not jackets
    10062: {
        "category": "hoodies"
    },
    
    # prod_114: Syna World Classic Logo Hoodie → should be hoodies, not accessories
    10114: {
        "category": "hoodies"
    },
    
    # prod_92: Nike x Sacai VaporWaffle 'Black Gum' → should be shoes, not pants
    10092: {
        "category": "shoes"
    },
    
    # prod_76: Maison Mihara Yasuhiro Peterson Low → should be shoes, not pants
    10076: {
        "category": "shoes"
    },
    
    # prod_162: C.P. Company Lens Flat Nylon Crossbody Bag → should be bags, not bags (already correct)
    # Actually it's correct

    # prod_151: Asics Gel-1130 White/Green → should be shoes, not accessories
    10151: {
        "category": "shoes"
    },
    
    # prod_129: Chrome Hearts Cross Logo Tee → should be tshirts, not accessories
    10129: {
        "category": "tshirts"
    },
}

# Apply fixes
fix_count = 0
for pid, fix_data in fixes.items():
    if pid not in products_by_id:
        print(f"  ⚠ Product ID {pid} not found, skipping")
        continue
    
    p = products_by_id[pid]
    changes = []
    
    for field, new_value in fix_data.items():
        old_value = p.get(field, '')
        if old_value != new_value:
            p[field] = new_value
            changes.append(f"{field}: '{old_value}' → '{new_value}'")
    
    if changes:
        fix_count += 1
        print(f"  ✓ Fixed ID {pid}: {'; '.join(changes)}")

print(f"\nApplied {fix_count} fixes")

# Rebuild data.js
products_json = json.dumps(products, indent=2, ensure_ascii=False)
# Fix Windows line endings in the JSON
products_json = products_json.replace('\n', '\r\n')

# Update DB_VERSION to force browser refresh
new_version = 'v33_name_fix'
new_content = f'const initialProducts = {products_json};\r\n'
new_content += '// Price Conversion Complete (CNY -> USD)\r\n'
new_content += f"const DB_VERSION = '{new_version}';\r\n"
new_content += '''try {\r
    const val = localStorage.getItem('db_version');\r
    if (val !== DB_VERSION) {\r
        localStorage.setItem('products', JSON.stringify(initialProducts));\r
        localStorage.setItem('db_version', DB_VERSION);\r
    }\r
} catch (e) {\r
    console.warn(e);\r
}\r
\r
function getProducts() {\r
    try {\r
        const stored = localStorage.getItem('products');\r
        if (stored) return JSON.parse(stored);\r
    } catch (e) {}\r
    return initialProducts;\r
}\r
\r
function saveProducts(products) {\r
    try {\r
        localStorage.setItem('products', JSON.stringify(products));\r
    } catch (e) {}\r
}\r
'''

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✅ data.js updated successfully!")
print(f"✅ DB_VERSION bumped to '{new_version}' (will force browser refresh)")
print(f"✅ Backup saved as: {backup_name}")
