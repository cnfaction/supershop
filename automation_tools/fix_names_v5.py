import re
import json
import os
import shutil
from datetime import datetime

# Master dictionary for Round 5 fixes
fixes = {
    # New Visual Cleanups
    10280: ("Corteiz Alcatraz Logo Denim Shorts", "Corteiz", "pants"),
    10222: ("Gucci GG Supreme Monogram Baseball Cap Collection", "Gucci", "accessories"),
    10214: ("Stone Island Apparel Collection (Hoodies & Vests)", "Stone Island", "hoodies"),
    10216: ("Designer Knit Beanie Collection (Moncler/LV/TNF)", "Other", "accessories"),
    10164: ("Broken Planet Market Graphic T-Shirt Collection", "Broken Planet Market", "tshirts"),
    10166: ("Essential Heavyweight Oversized Hoodie & Sweatpants Set", "Other", "sets"),
    10180: ("Arc'teryx Bird Head & Grotto Toque Collection", "Arc'teryx", "accessories"),
    10384: ("VLONE x Palm Angels Graphic T-Shirt", "VLONE", "tshirts"),
    10185: ("New Era 59FIFTY MLB Fitted Hat Collection", "New Era", "accessories"),
    10382: ("Broken Planet Market 'Trust Your Universe' Graphic T-Shirt", "Broken Planet Market", "tshirts"),
    10188: ("Off-White Arrows Logo Graphic T-Shirt Collection", "Off-White", "tshirts"),
    10272: ("Montbell Highland Down Jacket (Black)", "Montbell", "jackets"),
    10246: ("Celine Teen Triomphe Leather Bag", "Celine", "bags"),
    10370: ("Polo Ralph Lauren Lunar New Year Bear Knit Sweater", "Polo Ralph Lauren", "hoodies"),
    10215: ("Sp5der Worldwide Hoodie & Pants Collection", "Sp5der", "sets"),
    10338: ("Polo Ralph Lauren Quarter-Zip Merino Wool Sweater", "Polo Ralph Lauren", "hoodies"),
    10258: ("Acne Studios Distressed Loose-Fit Jeans", "Acne Studios", "pants"),
    10261: ("Adidas Handball Spezial Sneakers (Green/Gum)", "Adidas", "shoes"),
    10025: ("Corteiz Logo Graphic Sweatpants Collection", "Corteiz", "pants"),
    10371: ("Neutral Toned Texture Knit Sweater Collection", "Other", "hoodies"),
    10376: ("Corteiz Alcatraz Embroidered Denim Jeans Collection", "Corteiz", "pants"),
    10202: ("Miu Miu Gold Buckle Leather Belt", "Miu Miu", "accessories"),
    10197: ("Palm Angels Bear & Graphic T-Shirt Collection", "Palm Angels", "tshirts"),
    10184: ("Ami Paris Heart Logo Polo Shirt Collection", "Ami Paris", "tshirts"),
    10308: ("Polo Ralph Lauren Big Pony Polo Shirt (Norway)", "Polo Ralph Lauren", "tshirts"),
    10369: ("Louis Vuitton Checkerboard Knit Beanie Collection", "Louis Vuitton", "accessories"),
    10196: ("Salvatore Ferragamo Gancini Reversible Leather Belt", "Salvatore Ferragamo", "accessories"),
    10277: ("Louis Vuitton Damier Graphite Knit Beanie Collection", "Louis Vuitton", "accessories"),
    10243: ("C.P. Company Goggle Beanie Collection", "C.P. Company", "accessories"),
    10262: ("Sp5der Spider Web Graphic T-Shirt", "Sp5der", "tshirts"),
    10297: ("Stussy Graphic Soccer Jersey Collection", "Stussy", "tshirts"),
    10173: ("Prada Logo Patch Classic Leather Belt Collection", "Prada", "accessories"),
    10204: ("Balenciaga BB Logo Leather Belt", "Balenciaga", "accessories"),
    10312: ("Chrome Hearts Cross Patch Leather Belt Collection", "Chrome Hearts", "accessories"),
    10092: ("Ethika Staple Boxer Briefs", "Ethika", "accessories"),
    10252: ("Louis Vuitton Initiales Reversible Belt Collection", "Louis Vuitton", "accessories"),
    10181: ("Van Cleef & Arpels Alhambra 5-Motif Bracelet Collection", "Van Cleef & Arpels", "accessories"),

    # Category/Brand Cleanups for existing correct titles
    10099: ("Nike Tech Fleece Suit", "Nike", "sets"),
    10322: ("Polo Ralph Lauren Cable-Knit Sweater", "Polo Ralph Lauren", "hoodies"),
    10157: ("Moose Knuckles Fur-Trimmed Puffer Jacket", "Moose Knuckles", "jackets"),
    10290: ("UGG Tasman Slipper", "UGG", "shoes"),
    10027: ("Apple AirPods Pro (2nd Generation)", "Apple", "accessories"),
    10135: ("Designer Knitwear Collection (Dior/LV/Celine)", "Other", "hoodies"),
    10086: ("New Balance 1906R Sneakers", "New Balance", "shoes"),
    10219: ("Saint Laurent Script Logo Mohair Sweater", "Saint Laurent", "hoodies"),
    10102: ("Nike Spark Lightweight Socks", "Nike", "accessories"),
    10156: ("Valentino Born in Roma Intense Perfume", "Valentino", "accessories"),
    10373: ("Rimowa Style Aluminum Carry-On Suitcase", "Other", "bags"),
    10070: ("Nike Air Max Plus TN 'Pink Blast'", "Nike", "shoes"),
    10154: ("Chrome Hearts Cross Patch Waffle Henley", "Chrome Hearts", "tshirts"),
    10063: ("Fendi Watermark Monogram Shorts", "Fendi", "pants"),
    10087: ("New Balance 2002R Sneakers", "New Balance", "shoes"),
    10033: ("Gucci Screener GG Canvas Sneaker", "Gucci", "shoes"),
    10128: ("Louis Vuitton Keepall Bandouliere 50", "Louis Vuitton", "bags"),
    10081: ("MCM Stark Monogram Backpack", "MCM", "bags"),
    10071: ("Nike Air Zoom Vomero 5", "Nike", "shoes"),
    10103: ("Nike Mid-Cut Crew Socks", "Nike", "accessories"),
    10328: ("Timberland 6-Inch Premium Waterproof Boot", "Timberland", "shoes"),
    10112: ("Stussy Basic Stock Hoodie Gray", "Stussy", "hoodies"),
    10053: ("Nike Air Vapormax Plus 'Triple Black'", "Nike", "shoes"),
    10127: ("Louis Vuitton Christopher Backpack MM", "Louis Vuitton", "bags"),
    10097: ("Prada Cloudbust Thunder 'Black'", "Prada", "shoes"),
    10096: ("Nike Stussy Spiridon Cage 2 'Fossil'", "Nike", "shoes"),
    10124: ("Supreme Box Logo Tee White", "Supreme", "tshirts"),
    10117: ("Louis Vuitton Water-Reactive Monogram Swim Shorts", "Louis Vuitton", "pants"),
    10278: ("Chrome Hearts Cross Logo Hat", "Chrome Hearts", "accessories"),
    10142: ("Ami Paris Heart Embroidered Sweater", "Ami Paris", "hoodies"),
    10155: ("Stone Island Ghost Piece Overshirt", "Stone Island", "jackets"),
    10115: ("Nike Air Max Plus TN Gradient Blue", "Nike", "shoes"),
    10098: ("Prada Cloudbust Thunder 'Grey'", "Prada", "shoes"),
    10121: ("Nike x Nocta Cardinal Stock Hoodie", "Nike", "hoodies"), # Fixing category for previous ones too
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
            if p['title'] != new_title or p['brand'] != new_brand or p['category'] != new_cat:
                print(f"Updating ID {pid}: '{p['title']}' -> '{new_title}'")
                p['title'] = new_title
                p['brand'] = new_brand
                p['category'] = new_cat
                updated_count += 1
            
    if updated_count == 0:
        print("No products updated. Checks IDs correctly.")
        # We still want to bump version if we made changes in previous rounds but somehow version was lost
        # But here let's actually just bump it if count > 0

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
    new_version = 'v37_cleanup_v5'
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
