import json
import re

def safe_rewrite():
    # Read the data.js
    with open('data.js', 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # regex extract
    match = re.search(r'const initialProducts = (\[.*?\]);', content, re.DOTALL)
    if not match:
        print("Could not find initialProducts")
        return
        
    # leniently find products
    # We'll use re to find each { ... } object to avoid one broken object nuking the whole array
    raw_array = match.group(1)
    # This is rough because of nestings but most products have a simple structure
    # Actually, let's just use Python json.loads and fix the strings first
    
    # Replace all literal newlines in strings with \n
    # and all non-ascii with \u
    
    # We'll re-parse the whole thing but carefully
    try:
        # Step 1: Nuke all control characters that are NOT newline or space
        # (already done by sanitize, but let's be sure)
        raw_array = re.sub(r'[\x00-\x1F\x7F-\x9F]', ' ', raw_array)
        
        # Now try to fix common json breaks
        # (Already mostly fine)
        # Actually, let's just eval it in a very safe sandbox? No.
        
        # We'll use json.loads but try to fix the \ue569 junk
        # by replacing any non-ASCII char with its repr?
        
        # Actually, the easiest way:
        # products = eval(raw_array) # TOO RISKY? No, it's our own data
        # BUT the data uses JSON format, not python dict (e.g. true/false vs True/False)
        fixed_js = raw_array.replace('true', 'True').replace('false', 'False').replace(': null', ': None')
        # This is also risky.
        
        # Let's try JSON loads but replace bad characters first
        import json
        
        def safe_load():
            try:
                return json.loads(raw_array)
            except Exception as e:
                print(f"DEBUG: Initial load failed: {e}")
                # Try to clean strings from control chars and other junk
                # We'll use a regex to find all values and escape them.
                # Actually, let's just strip non-ASCII in the whole raw_array for a moment
                # ONLY for the strings? No.
                
                # RECOVERY: I'll just use my backup before the errors started!
                return None

        products = safe_load()
        if not products:
             # If everything failed, try to load the backup!
             backup_file = 'data.js.backup_20260325_110152'
             print(f"Trying backup {backup_file}")
             with open(backup_file, 'r', encoding='utf-8', errors='replace') as bf:
                 bcontent = bf.read()
                 bmatch = re.search(r'const initialProducts = (\[.*?\]);', bcontent, re.DOTALL)
                 if bmatch:
                     # This backup should be clean!
                     # Wait, I'll do it safely
                     js_b = bmatch.group(1)
                     # Nuke the potentially broken chars from the backup too just in case
                     js_b = re.sub(r'[\x00-\x1f]', ' ', js_b)
                     products = json.loads(js_b)

        if not products:
            print("FAILED to recover products")
            return
            
        print(f"SUCCESS: Loaded {len(products)} products from recovery.")
        
        # RE-APPLY ALL RECENT FIXES (just to be sure)
        # Actually, I'll take the LATEST backup before the Round 11 corrupted thing.
        # Wait! Round 11 was at 15:11. Today.
        # My backups:
        # data.js.backup_20260325_145245 (Round 6/7)
        # data.js.backup_20260325_150723 (Round 10)
        # data.js.backup_20260325_151126 (Round 11) - the one that's broken?
        
        # I'll use 15:07 backup! It has 391 products and most fixes.
        with open('data.js.backup_20260325_150723', 'r', encoding='utf-8', errors='replace') as bf:
             bcontent = bf.read()
             bmatch = re.search(r'const initialProducts = (\[.*?\]);', bcontent, re.DOTALL)
             products = json.loads(bmatch.group(1))

        # Re-apply Round 11 manual corrections to the good data
        fixes_r11 = {
            10226: ("Gucci Run Technical Mesh Sneaker (Grey)", "Gucci", "shoes"),
            10012: ("Autry Medalist Low Sneakers (Black/White)", "Autry", "shoes"),
            10203: ("Crocs x Disney Cars 'Mater' Classic Clog", "Crocs", "shoes"),
            10028: ("Balenciaga 10XL Sneaker (Pink/Grey)", "Balenciaga", "shoes"),
            10268: ("Hermes Bouncing Sneaker (Beige/White)", "Hermes", "shoes"),
            10170: ("Louis Vuitton LV Skate Sneaker (Maritime Blue)", "Louis Vuitton", "shoes"),
            10106: ("ASICS Gel-Kayano 14 (Black/Silver)", "ASICS", "shoes"),
            10145: ("Balenciaga Runner Sneaker (Silver/Pink/White)", "Balenciaga", "shoes"),
        }
        
        for p in products:
            if p['id'] in fixes_r11:
                t, b, c = fixes_r11[p['id']]
                p['title'], p['brand'], p['category'] = t, b, c

        # WRITE BACK AS 100% CLEAN JSON
        new_products_js = json.dumps(products, indent=4, ensure_ascii=False)
        
        # Reconstruct data.js
        header = "const initialProducts = "
        # Keep the getProducts part from tail
        # I'll just write it manually
        final_js = f"const initialProducts = {new_products_js};\n\nconst DB_VERSION = 'v44_recovery_final';\n\ntry {{\n    const val = localStorage.getItem('db_version');\n    if (val !== DB_VERSION) {{\n        localStorage.setItem('products', JSON.stringify(initialProducts));\n        localStorage.setItem('db_version', DB_VERSION);\n    }}\n}} catch (e) {{\n    console.warn(e);\n}}\n\nfunction getProducts() {{\n    try {{\n        const stored = localStorage.getItem('products');\n        if (stored) return JSON.parse(stored);\n    }} catch (e) {{}}\n    return initialProducts;\n}}\n\nfunction saveProducts(products) {{\n    try {{\n        localStorage.setItem('products', JSON.stringify(products));\n    }} catch (e) {{}}\n}}\n"
        
        with open('data.js', 'w', encoding='utf-8') as f:
            f.write(final_js)
            
        print("data.js successfully RECONSTRUCTED from good backup + Round 11 fixes.")

    except Exception as e:
        print(f"RECOVERY FAILED: {e}")

if __name__ == "__main__":
    safe_rewrite()
