#!/usr/bin/env python3
"""
Round 3: Fix remaining Premium-named products and other mismatches.
All fixes visually verified against actual product images.
"""
import re, json, sys, shutil
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

backup_name = f'data.js.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
shutil.copy('data.js', backup_name)
print(f"Backup: {backup_name}")

match = re.search(r'const initialProducts = (\[.*?\]);', content, re.DOTALL)
products = json.loads(match.group(1))
print(f"Loaded {len(products)} products")
products_by_id = {p['id']: p for p in products}

fixes = {
    # ===== PREMIUM PRODUCTS - Visually verified =====
    
    # prod_0: Black leather harness ankle boots (luxury style)
    10000: {"title": "Leather Harness Ankle Boots", "brand": "Other", "category": "shoes"},
    
    # prod_1: Chrome Hearts T-shirts (horseshoe, cross, gothic text)
    10001: {"title": "Chrome Hearts Horseshoe Cross Logo T-Shirt Collection", "brand": "Chrome Hearts", "category": "tshirts"},
    
    # prod_3: Rimowa iPhone cases (ribbed, multiple colors, with Rimowa boxes)
    10003: {"title": "Rimowa Groove iPhone Case Collection", "brand": "Rimowa", "category": "accessories"},
    
    # prod_5: ASSC Anti Social Social Club koi fish T-shirt (black)
    10005: {"title": "Anti Social Social Club Koi Fish T-Shirt", "brand": "ASSC", "category": "tshirts"},
    
    # prod_7: Louis Vuitton monogram leather bracelet with gold LV buckle
    10007: {"title": "Louis Vuitton Monogram Sign It Bracelet", "brand": "Louis Vuitton", "category": "accessories"},
    
    # prod_9: Brazil national team football jerseys (many designs)
    10009: {"title": "Brazil National Team Football Jersey Collection", "brand": "Soccer", "category": "jerseys"},
    
    # prod_24: Acne Studios Stockholm 1996 white T-shirt
    10024: {"title": "Acne Studios Stockholm 1996 Logo T-Shirt", "brand": "Acne Studios", "category": "tshirts"},
    
    # prod_40: Chrome Hearts long sleeve T-shirts (raglan, horseshoe, crosses)
    10040: {"title": "Chrome Hearts Long Sleeve T-Shirt Collection", "brand": "Chrome Hearts", "category": "tshirts"},
    
    # prod_43: Grey hoodie & sweatpants matching set
    10043: {"title": "Minimalist Logo Hoodie & Sweatpants Set", "brand": "Other", "category": "sets"},
    
    # prod_47: Corteiz baby blue crewneck sweatshirt
    10047: {"title": "Corteiz Classic Crewneck Sweatshirt", "brand": "Corteiz", "category": "hoodies"},
    
    # prod_48: Corteiz Alcatraz trucker caps (star logo, multiple colors)
    10048: {"title": "Corteiz Alcatraz Trucker Cap", "brand": "Corteiz", "category": "accessories"},
    
    # prod_176: Stussy logo beanie (burgundy with yellow text)
    10176: {"title": "Stussy Logo Beanie", "brand": "Stussy", "category": "accessories"},
    
    # prod_178: Burberry check collar polo shirt (black with plaid collar)
    10178: {"title": "Burberry Check Collar Polo Shirt", "brand": "Burberry", "category": "tshirts"},
    
    # prod_207: Balmain Paris logo knit sweaters (9 colorways)
    10207: {"title": "Balmain Paris Logo Knit Sweater Collection", "brand": "Balmain", "category": "hoodies"},
    
    # prod_209: Sweatpants with circular logo (multiple colors)
    10209: {"title": "Logo Print Drawstring Sweatpants Collection", "brand": "Other", "category": "pants"},
    
    # prod_269: Nike x CLOT Air Force 1 Rose Gold Silk
    10269: {"title": "Nike x CLOT Air Force 1 Rose Gold Silk", "brand": "Nike", "category": "shoes"},
    
    # prod_329: Nike Pro training compression tops (white, long/short/sleeveless)
    10329: {"title": "Nike Pro Training Compression Top Collection", "brand": "Nike", "category": "tshirts"},
    
    # prod_335: Stone Island compass crewneck sweatshirts (many colors)
    10335: {"title": "Stone Island Compass Logo Crewneck Sweatshirt", "brand": "Stone Island", "category": "hoodies"},
    
    # ===== CATEGORY-ONLY FIXES =====
    
    # prod_186: Hellstar tracksuit SET (hoodie + pants) - was "pants"
    10186: {"category": "sets"},
    
    # prod_138: Retro NBA jerseys from MANY teams, not just Warriors
    10138: {"title": "Retro NBA Hardwood Classics Basketball Jersey Collection", "brand": "NBA", "category": "jerseys"},
    
    # prod_55: Denim Tears cotton wreath T-shirt & shorts sets
    10055: {"title": "Denim Tears Cotton Wreath T-Shirt & Shorts Set", "brand": "Denim Tears", "category": "sets"},
}

fix_count = 0
for pid, fix_data in fixes.items():
    if pid not in products_by_id:
        print(f"  ⚠ ID {pid} not found")
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
        print(f"  ✓ {pid}: {'; '.join(changes)}")

print(f"\nApplied {fix_count} fixes")

products_json = json.dumps(products, indent=2, ensure_ascii=False)
new_version = 'v35_name_fix_v3'
new_content = f'const initialProducts = {products_json};\n'
new_content += '// Price Conversion Complete (CNY -> USD)\n'
new_content += f"const DB_VERSION = '{new_version}';\n"
new_content += '''try {
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
'''

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✅ data.js updated! DB_VERSION = '{new_version}'")
