#!/usr/bin/env python3
"""Extract all product titles, brands, categories and image paths from data.js for review."""
import re
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the array content
match = re.search(r'const initialProducts = (\[.*?\]);', content, re.DOTALL)
if not match:
    print("Could not find initialProducts array")
    exit(1)

products = json.loads(match.group(1))
print(f"Total products: {len(products)}")
print("=" * 130)
print(f"{'ID':<8} {'Brand':<25} {'Category':<15} {'Title':<60} {'Folder'}")
print("=" * 130)

for p in products:
    img = p.get('image', '') or (p.get('images', [''])[0] if p.get('images') else '')
    folder_match = re.search(r'p_images/(prod_\d+)/', img)
    folder = folder_match.group(1) if folder_match else 'N/A'
    
    title = p['title'][:58]
    brand = p.get('brand','')[:23]
    cat = p.get('category','')[:13]
    
    print(f"{p['id']:<8} {brand:<25} {cat:<15} {title:<60} {folder}")

print("\n\n=== POTENTIAL MISMATCHES ===")
print("Products where brand/title may not match category:")
for p in products:
    title_lower = p['title'].lower()
    brand_lower = p.get('brand','').lower()
    cat = p.get('category','')
    
    issues = []
    
    # Check shoe products that don't have shoe-related words
    if cat == 'shoes' and not any(w in title_lower for w in ['shoe', 'sneaker', 'boot', 'slipper', 'loafer', 'slide', 'clog', 'sandal', 'trainer', 'runner', 'dunk', 'jordan', 'air max', 'yeezy', 'force']):
        issues.append(f"Category is 'shoes' but title doesn't seem shoe-related")
    
    # Check jacket products
    if cat == 'jackets' and any(w in title_lower for w in ['bag', 'sneaker', 'shoe', 'backpack']):
        issues.append(f"Category is 'jackets' but title mentions bags/shoes")
    
    # Check pants products  
    if cat == 'pants' and any(w in title_lower for w in ['sneaker', 'shoe', 'hoodie', 'jacket', 'ramones']):
        issues.append(f"Category is 'pants' but title seems wrong")
    
    # Check if brand appears disconnected from title
    if brand_lower and brand_lower not in title_lower:
        # Check common abbreviations
        brand_words = brand_lower.split()
        title_words = title_lower.split()
        if not any(bw in ' '.join(title_words) for bw in brand_words):
            if brand_lower not in ['jordan', 'fear of god']:  # These are often shortened
                issues.append(f"Brand '{p.get('brand','')}' not found in title")
    
    if issues:
        img = p.get('image', '') or (p.get('images', [''])[0] if p.get('images') else '')
        folder_match = re.search(r'p_images/(prod_\d+)/', img)
        folder = folder_match.group(1) if folder_match else 'N/A'
        print(f"\nID: {p['id']} | {folder}")
        print(f"  Title: {p['title']}")
        print(f"  Brand: {p.get('brand','')} | Category: {cat}")
        for issue in issues:
            print(f"  ⚠ {issue}")
