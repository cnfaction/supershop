import json
import re
import urllib.request
import time

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

def fetch_weidian_title(item_id):
    """Fetch the Chinese title from a Weidian item page."""
    url = f'https://weidian.com/item.html?itemID={item_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        m = re.search(r'class="item-name"[^>]*>(.*?)</span>', html, re.DOTALL)
        if m:
            raw = m.group(1).strip()
            # Remove HTML tags
            raw = re.sub(r'<[^>]+>', '', raw).strip()
            return raw
    except Exception as e:
        return None
    return None

# Brand keyword → English brand name mapping
BRAND_MAP = {
    'balenciaga': ('Balenciaga', 'sneakers'),
    'b*l*enc': ('Balenciaga', 'sneakers'),
    'gucci': ('Gucci', 'sneakers'),
    'louis vuitton': ('Louis Vuitton', 'accessories'),
    'lv': ('Louis Vuitton', 'accessories'),
    'dior': ('Dior', 'general'),
    'chanel': ('Chanel', 'general'),
    'nike': ('Nike', 'general'),
    'n1k': ('Nike', 'sneakers'),
    'air max': ('Nike', 'sneakers'),
    'jordan': ('Jordan', 'sneakers'),
    'adidas': ('Adidas', 'sneakers'),
    'yeezy': ('Adidas', 'sneakers'),
    'prada': ('Prada', 'general'),
    'corteiz': ('Corteiz', 'hoodies'),
    'crtz': ('Corteiz', 'hoodies'),
    'stone island': ('Stone Island', 'jackets'),
    'chrome hearts': ('Chrome Hearts', 'general'),
    'ch': ('Chrome Hearts', 'general'),
    'fear of god': ('Fear of God', 'hoodies'),
    'fog': ('Fear of God', 'hoodies'),
    'essentials': ('Fear of God', 'hoodies'),
    'canada goose': ('Canada Goose', 'jackets'),
    'moncler': ('Moncler', 'jackets'),
    'mon家': ('Moncler', 'jackets'),
    'burberry': ('Burberry', 'general'),
    'ralph lauren': ('Polo Ralph Lauren', 'general'),
    '小马': ('Polo Ralph Lauren', 'general'),
    'stussy': ('Stussy', 'general'),
    'bape': ('BAPE', 'hoodies'),
    'sp5der': ('Sp5der', 'hoodies'),
    'hellstar': ('Hellstar', 'hoodies'),
    'gallery dept': ('Gallery Dept.', 'pants'),
    'carhartt': ('Carhartt', 'jackets'),
    'c卡哈': ('Carhartt', 'jackets'),
    'ami paris': ('Ami Paris', 'general'),
    'new balance': ('New Balance', 'sneakers'),
    'nb': ('New Balance', 'sneakers'),
    'asics': ('ASICS', 'sneakers'),
    'alo': ('Alo Yoga', 'hoodies'),
    'denim tears': ('Denim Tears', 'general'),
    'derschutze': ('Derschutze', 'pants'),
    '梅花': ('Derschutze', 'pants'),
    'purple brand': ('Purple Brand', 'pants'),
    'palm angels': ('Palm Angels', 'jackets'),
    'supreme': ('Supreme', 'general'),
    'comme des': ('Comme des Garçons', 'hoodies'),
    'cp公司': ('C.P. Company', 'jackets'),
    'cp棉': ('C.P. Company', 'jackets'),
    'c.p.': ('C.P. Company', 'jackets'),
    'vlone': ('Vlone', 'hoodies'),
    'vetements': ('Vetements', 'general'),
    'syna': ('Syna World', 'jackets'),
    'cas': ('Casablanca', 'general'),
    'fendi': ('Fendi', 'general'),
    'valentino': ('Valentino', 'jackets'),
    'mcm': ('MCM', 'bags'),
    'moose knuckles': ('Moose Knuckles', 'jackets'),
    'rick owens': ('Rick Owens', 'general'),
    'acne': ('Acne Studios', 'general'),
    'zadig': ('Zadig & Voltaire', 'bags'),
    'arc\'teryx': ('Arc\'teryx', 'jackets'),
    'gymshark': ('Gymshark', 'general'),
    '运动': ('Nike', 'general'),
    '球衣': ('Jersey', 'general'),
    '足球': ('Soccer', 'general'),
    '篮球': ('Basketball', 'general'),
    '卫衣': (None, 'hoodies'),
    '裤': (None, 'pants'),
    '夹克': (None, 'jackets'),
    '鞋': (None, 'sneakers'),
    '包': (None, 'bags'),
}

# Title templates based on Chinese category keywords
CATEGORY_NAMES = {
    '卫衣': 'Hoodie',
    '连帽': 'Hoodie',
    '夹克': 'Jacket',
    '外套': 'Jacket',
    '裤子': 'Pants',
    '裤': 'Pants',
    '短裤': 'Shorts',
    '鞋子': 'Sneakers',
    '运动鞋': 'Sneakers',
    '板鞋': 'Sneakers',
    'T恤': 'T-Shirt',
    '球衣': 'Jersey',
    '毛衣': 'Sweater',
    '针织': 'Knit Sweater',
    '背包': 'Backpack',
    '包': 'Bag',
    '钱包': 'Wallet',
    '皮带': 'Belt',
    '帽子': 'Cap',
    '毛线帽': 'Beanie',
    '袜子': 'Socks',
    '套装': 'Set',
}

def detect_brand_and_cat(zh_title):
    """Detect brand and category from Chinese title."""
    lower = zh_title.lower()
    brand = None
    category = None
    
    for keyword, (b, c) in BRAND_MAP.items():
        if keyword.lower() in lower:
            if b:
                brand = b
            if c:
                category = c
            break
    
    if not category:
        for zh_kw, en_cat in CATEGORY_NAMES.items():
            if zh_kw in zh_title:
                category = en_cat.lower()
                break
    
    return brand, category

def build_english_title(brand, category_name, zh_title):
    """Build a simple English title."""
    # Get category display name
    cat_display = 'Item'
    for zh_kw, en_nm in CATEGORY_NAMES.items():
        if zh_kw in zh_title:
            cat_display = en_nm
            break
    
    if brand:
        return f"{brand} {cat_display}"
    return cat_display

def extract_item_id(link):
    m = re.search(r'itemID=(\d+)', link)
    return m.group(1) if m else None

print("Starting global alignment scan...")
print(f"Total products: {len(products)}")

updated = 0
failed = []

for i, p in enumerate(products):
    item_id = extract_item_id(p.get('link', ''))
    if not item_id:
        continue
    
    zh_title = fetch_weidian_title(item_id)
    if not zh_title:
        failed.append(p['id'])
        print(f"[{i+1}/{len(products)}] ID {p['id']}: FAILED to fetch")
        time.sleep(0.3)
        continue
    
    brand, category = detect_brand_and_cat(zh_title)
    
    # Build English title
    en_title = build_english_title(brand, category, zh_title)
    
    # Only update if we detected a brand and the current title doesn't match
    if brand and brand.lower() not in p['title'].lower():
        old_title = p['title']
        p['title'] = en_title
        if brand:
            p['brand'] = brand
        updated += 1
        print(f"[{i+1}/{len(products)}] FIXED ID {p['id']}: '{old_title}' -> '{en_title}'")
    else:
        print(f"[{i+1}/{len(products)}] OK ID {p['id']}: '{p['title']}'")
    
    time.sleep(0.2)  # Rate limit

print(f"\nDone. Updated {updated} products. Failed: {len(failed)}")
print(f"Failed IDs: {failed}")

# Save
output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
output += """
// Global Alignment Complete
const DB_VERSION = 'v24_global_alignment';
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

with open(path, 'w', encoding='utf-8') as f:
    f.write(output)

print("Data saved to data.js successfully!")
