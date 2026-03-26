import re
import json
import os
import shutil
from datetime import datetime

# Master dictionary for Round 11 precise fixes based on NEW USER IMAGES
fixes = {
    10226: ("Gucci Run Technical Mesh Sneaker (Grey)", "Gucci", "shoes"),
    10012: ("Autry Medalist Low Sneakers (Black/White)", "Autry", "shoes"),
    10203: ("Crocs x Disney Cars 'Mater' Classic Clog", "Crocs", "shoes"),
    10028: ("Balenciaga 10XL Sneaker (Pink/Grey)", "Balenciaga", "shoes"),
    10268: ("Hermès Bouncing Sneaker (Beige/White)", "Hermès", "shoes"),
    10170: ("Louis Vuitton LV Skate Sneaker (Maritime Blue)", "Louis Vuitton", "shoes"),
    10106: ("ASICS Gel-Kayano 14 (Black/Silver)", "ASICS", "shoes"),
    10145: ("Balenciaga Runner Sneaker (Silver/Pink/White)", "Balenciaga", "shoes"),
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
    new_version = 'v43_final_shoe_audit'
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
