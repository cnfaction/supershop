import re
import json
import os
import shutil
from datetime import datetime

# Master dictionary for Round 4 fixes
fixes = {
    10100: ("Burberry Logo T-Shirt & Polo Collection", "Burberry", "tshirts"),
    10021: ("Nike Air Max Solo Sneakers", "Nike", "shoes"),
    10030: ("Dior B27 Sneaker Collection", "Dior", "shoes"),
    10038: ("Burberry Prorsum Knight Crewneck Sweatshirt", "Burberry", "hoodies"),
    10211: ("Denim Tears Cotton Wreath Hoodie & Pants Suit", "Denim Tears", "sets"),
    10228: ("Logo Embroidery Lounge Sweatpants", "Other", "pants"),
    10240: ("Designer MagSafe Leather Card Holder (LV/Gucci)", "Other", "accessories"),
    10245: ("Saint Laurent (YSL) Embroidered Logo Denim Jeans", "Saint Laurent", "pants"),
    10250: ("Chanel CC Logo Knit Beanie", "Chanel", "accessories"),
    10255: ("Corteiz Alcatraz and Graphic T-Shirt Collection", "Corteiz", "tshirts"),
    10260: ("Streetwear Graphic Knit Sweater Collection", "Other", "hoodies"),
    10288: ("Polo Ralph Lauren Swim Shorts Collection", "Polo Ralph Lauren", "pants"),
    10291: ("Yves Saint Laurent (YSL) Mon Paris Eau de Parfum", "Saint Laurent", "accessories"),
    10302: ("Alo Yoga Wide-Leg Sweatpants", "Other", "pants"),
    10309: ("Hermes H Buckle Leather Belt", "Hermes", "accessories"),
    10323: ("Fear of God Essentials Hoodie & Sweatshirt Collection", "Fear of God", "hoodies"),
    10326: ("Balenciaga BB Logo Leather Belt", "Balenciaga", "accessories"),
    10333: ("Gucci GG Canvas Baseball Cap", "Gucci", "accessories"),
    10339: ("Supreme x Ducati Logo T-Shirt Collection", "Supreme", "tshirts"),
    10342: ("Supreme x Ducati Logo T-Shirt (Back Graphics)", "Supreme", "tshirts"),
    10284: ("Celine Fluffy Mohair Knit Sweater", "Celine", "hoodies"),
    10285: ("Ami Paris Heart Logo Knit Sweater", "Ami Paris", "hoodies"),
    10286: ("Louis Vuitton LV Logo Knit Sweater", "Louis Vuitton", "hoodies"),
    10353: ("LEGO Star Wars Millennium Falcon (75375)", "LEGO", "general"),
    10028: ("ASICS Gel-Kayano 14 Sneakers (Pink)", "ASICS", "shoes"),
    10389: ("Cole Buxton Logo Knit Hoodie & Pants Set", "Cole Buxton", "sets"),
    10004: ("Chrome Hearts Prescription Glasses (Model 6235)", "Chrome Hearts", "accessories"),
    10321: ("Arc'teryx Bird Head Beanie Collection", "Arc'teryx", "accessories"),
    10385: ("Canada Goose Fur-Trimmed Down Jacket (Pink)", "Canada Goose", "jackets"),
    10195: ("Louis Vuitton Low Key Shoulder Bag", "Louis Vuitton", "bags"),
    10241: ("Goyard Senat Clutch Bag (Green)", "Goyard", "bags"),
    10039: ("Burberry Check Lined Zip Hoodie", "Burberry", "hoodies"),
    10041: ("Carhartt WIP Denim Jeans Collection", "Carhartt", "pants"),
    10379: ("Needles Wide Track Pants Collection", "Needles", "pants"),
    10187: ("Isabel Marant Sabe Aran Studded Shoulder Bag", "Isabel Marant", "bags"),
    10171: ("Carhartt WIP Kickflip Backpack", "Carhartt", "bags"),
    10177: ("Adidas x Clot (Edison Chen) Gazelle Track Jacket", "Adidas", "jackets"),
    10168: ("Unknown London Graphic Hoodie & Sweatpants Set", "Unknown London", "sets"),
    10218: ("Luxury Down Jacket & Vest Collection (Moncler/Canada Goose)", "Other", "jackets"),
    10319: ("Stone Island Logo Patch Knit Sweater", "Stone Island", "hoodies"),
    10279: ("Pastel Life 'Protect' Embroidered Denim Shorts", "Other", "pants"),
    10205: ("Under Armour Threadborne Tech T-Shirt", "Under Armour", "tshirts"),
    10190: ("Synaworld Logo Puffer Jacket Collection", "Synaworld", "jackets"),
    10325: ("Fear of God Essentials 1977 Athletic Shorts", "Fear of God", "pants"),
    10032: ("Prada Re-Edition 2005 Nylon Mini Bag", "Prada", "bags"),
    10008: ("Canada Goose Expedition Down Parka Collection", "Canada Goose", "jackets"),
    10282: ("Balenciaga Boxer-Waist Sweatpants", "Balenciaga", "pants"),
    10194: ("Dior Oblique Quilted Puffer Jacket", "Dior", "jackets"),
    10367: ("Nike Tech Fleece Hoodie & Joggers Set", "Nike", "sets"),
    10239: ("Balenciaga Suede City Bag (Khaki)", "Balenciaga", "bags"),
    10341: ("Gucci GG Jacquard Wool Cardigan", "Gucci", "hoodies"),
    10016: ("Loewe Anagram Embroidered Track Pants", "Loewe", "pants"),
    10010: ("Canada Goose Freestyle Down Vest Collection", "Canada Goose", "jackets"),
    10199: ("Palace Pertex Quantum Down Puffa Jacket", "Palace", "jackets"),
    10294: ("Vintage Wash Tribal Print Denim Jeans", "Other", "pants"),
    10037: ("Balenciaga Boxer-Waist Athletic Shorts", "Balenciaga", "pants"),
}

def apply_fixes():
    data_file = 'data.js'
    
    # Backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy(data_file, f'{data_file}.backup_{timestamp}')
    
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract products
    products_match = re.search(r'const initialProducts = (\[.*?\]);', content, re.DOTALL)
    if not products_match:
        print("Could not find initialProducts array")
        return
    
    products = json.loads(products_match.group(1))
    
    updated_count = 0
    for p in products:
        pid = p['id']
        if pid in fixes:
            new_title, new_brand, new_cat = fixes[pid]
            print(f"Updating ID {pid}: '{p['title']}' -> '{new_title}'")
            p['title'] = new_title
            p['brand'] = new_brand
            p['category'] = new_cat
            updated_count += 1
            
    if updated_count == 0:
        print("No products updated. Checks IDs correctly.")
        return

    # Prepare JS array string manually to preserve formatting or just use json.dumps
    # Using json.dumps with intent and ensuring correct escapes
    new_products_js = json.dumps(products, indent=4, ensure_ascii=False)
    
    # Replace in content
    new_content = re.sub(
        r'const initialProducts = \[.*?\];', 
        f'const initialProducts = {new_products_js};', 
        content, 
        flags=re.DOTALL
    )
    
    # Bump DB_VERSION
    new_version = 'v36_name_fix_v4'
    new_content = re.sub(
        r"const DB_VERSION = '.*?';", 
        f"const DB_VERSION = '{new_version}';", 
        new_content
    )
    
    with open(data_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Successfully updated {updated_count} products.")
    print(f"DB_VERSION bumped to {new_version}")

if __name__ == "__main__":
    apply_fixes()
