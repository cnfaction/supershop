import json
import re

def check_data():
    with open('data.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check initialProducts
    match = re.search(r'const initialProducts = (\[.*?\]);', content, re.DOTALL)
    if not match:
        print("FAILED: could not find initialProducts")
        return
    
    try:
        products = json.loads(match.group(1))
        print(f"SUCCESS: found {len(products)} products")
        if len(products) > 0:
            print(f"First product: {products[0]['title']}")
    except Exception as e:
        print(f"FAILED to parse products: {str(e)}")
        # Print snippet to find error
        js = match.group(1)
        # Try to find where it breaks
        for i in range(1, len(js)):
            try:
                json.loads(js[:i] + ']') # simplistic
            except:
                pass
    
if __name__ == "__main__":
    check_data()
