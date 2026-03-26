import re
import json
import os
import shutil
from datetime import datetime

# Master dictionary for Round 8 precise fixes based on NEW USER IMAGES
fixes = {
    10116: ("Supreme Box Logo Hoodie (Beige)", "Supreme", "hoodies"),
    10097: ("Casablanca Floral Graphic Silk Shirt", "Casablanca", "tshirts"),
    10096: ("Palm Angels Classic Tracksuit Set (Navy)", "Palm Angels", "sets"),
    10150: ("Eric Emanuel (EE) Skyline Mesh Shorts", "Eric Emanuel", "pants"),
    10115: ("Synaworld Logo Hoodie & Pants Set", "Synaworld", "sets"),
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
        print("No products updated.")
        return

    # Prepare JS array string manually to preserve formatting
    new_products_js = json.dumps(products, indent=4, ensure_ascii=False)
    
    # Replace in content
    new_content = re.sub(
        r'const initialProducts = \[.*?\];', 
        f'const initialProducts = {new_products_js};', 
        content, 
        flags=re.DOTALL
    )
    
    # Bump DB_VERSION
    new_version = 'v40_user_image_fix'
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
