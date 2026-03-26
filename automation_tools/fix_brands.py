import json
import re

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Brand detection rules: check title for keywords (order matters - more specific first)
BRAND_RULES = [
    # Luxury
    ('Louis Vuitton', ['louis vuitton', 'lv trainer', 'lv skate', 'lv monogram', 'lv water-reactive', 'lv nano']),
    ('Chanel', ['chanel', 'chanel logo']),
    ('Dior', ['dior b30', 'dior b23', 'dior oblique', 'dior saddle', 'christian dior', 'dior bb']),
    ('Gucci', ['gucci ace', 'gucci gg', 'gucci screener', 'gucci double', 'gucci city']),
    ('Prada', ['prada america', "prada cloudbust", 'prada nylon', 'prada re-nylon']),
    ('Burberry', ['burberry check', 'burberry equestrian', 'burberry vintage', 'burberry detachable', 'burberry plaid']),
    ('Hermès', ['hermès', 'hermes']),
    ('Valentino', ['valentino v-logo', 'valentino born', "valentino garavani"]),
    ('Fendi', ['fendi watermark', 'fendi ff', 'fendi logo']),
    ('Givenchy', ['givenchy city', 'givenchy spectre']),
    ('Celine', ['celine', 'celine triomphe']),
    ('Bottega Veneta', ['bottega veneta', 'bottega']),
    ('Versace', ['versace', 'medusa']),
    ('Tom Ford', ['tom ford']),
    ('Zadig & Voltaire', ['zadig & voltaire', 'zadig']),
    
    # Streetwear brands
    ('Balenciaga', ['balenciaga track', 'balenciaga triple', 'balenciaga runner', 'balenciaga 3xl', 'balenciaga speed', 'balenciaga bb logo', 'balenciaga graffiti', 'balenciaga explorer', 'balenciaga b30']),
    ('Off-White', ['off-white', 'virgil abloh']),
    ('Denim Tears', ['denim tears']),
    ('Gallery Dept.', ['gallery dept']),
    ('Chrome Hearts', ['chrome hearts', 'chr0me']),
    ('Fear of God', ['fear of god', 'fog essentials', 'essentials 1977']),
    ('Corteiz', ['corteiz', 'crtz', 'alcatraz']),
    ('Sp5der', ['sp5der']),
    ('Hellstar', ['hellstar studios', 'hellstar pink', 'hellstar flame']),
    ('Vlone', ['vlone friends', 'vlone']),
    ('Stussy', ['stussy 8 ball', 'stussy graphic', 'stussy jennie', 'stussy hooded', 'stussy 8-ball']),
    ('BAPE', ['bape shark', 'bape college', 'bape ape']),
    ('Supreme', ['supreme x umbro', 'supreme box', 'supreme logo']),
    ('Palace', ['palace']),
    ('Carhart', ['carhartt canvas']),
    ('Purple Brand', ['purple brand flared', 'purple brand hooded', 'purple brand slim', 'purple brand distressed', 'purple brand logo']),
    ('Palm Angels', ['palm angels']),
    ('Vetements', ['vetements logo']),
    ('Casablanca', ['casablanca tennis']),
    ('Ami Paris', ['ami paris heart', 'ami paris red']),
    ("Comme des Garçons", ['comme des garçons', 'cdg play', 'cdg']),
    ('Acne Studios', ['acne studios']),
    ('Syna World', ['syna world']),
    ('Corteiz', ['devil print tracksuit']),
    ('Rick Owens', ['rick owens drkshdw', 'rick owens']),
    ('Moncler', ['moncler maya', 'moncler classic', 'moncler knit', 'moncler hybrid', 'moncler x valentino']),
    ('Canada Goose', ['canada goose']),
    ('Stone Island', ['stone island']),
    ('C.P. Company', ['c.p. company', 'cp company', 'goggle lens']),
    ('Alo Yoga', ['alo yoga']),
    ('Maison Margiela', ['maison margiela replica', 'maison margiela']),
    ('Mihara Yasuhiro', ['mihara yasuhiro', 'maison mihara']),
    ('Golden Goose', ['golden goose']),
    ('Polo Ralph Lauren', ['polo ralph lauren', 'ralph lauren cable', 'ralph lauren zip', 'ralph lauren big pony', 'ralph lauren japan', 'ralph lauren half-zip', 'ralph lauren pony', 'ralph lauren hooded']),
    ('Lacoste', ['lacoste quarter-zip', 'lacoste']),
    
    # Nike family
    ('Jordan', ['air jordan 4', 'air jordan 1', 'air jordan diamond', 'jordan mesh', 'travis scott x air jordan', 'off-white x air jordan']),
    ('Nike', ['nike air max', 'nike sb dunk', 'nike tech fleece', 'nike sportswear', 'nike dri-fit', 'nike dunk', 'nike air zoom', 'nike air force', 'nike academy', 'nike futura', 'nike windbreaker', 'nike hyperwarm', 'nike x sacai', 'nike elite', 'nike stussy', 'nike cushion', 'nike running', 'nike aerowift', 'nike barcelona', 'nike x cactus', 'nike x nocta', 'nike aeroswift']),
    
    # Adidas family
    ('Adidas', ['adidas f50', 'adidas yeezy', 'adidas spezial', 'adidas mid-cut']),
    ('Yeezy', ['yeezy gap', 'yeezy slide']),
    
    # Other brands
    ('New Balance', ['new balance 990', 'new balance 9060', 'new balance 2002', 'new balance 1906', 'asics x jjjjound', 'new balance x']),
    ('ASICS', ['asics gel-nyc', 'asics gel-kayano', 'asics gel-1130', 'asics gel-', 'asics x']),
    ('Samba', ['adidas samba']),
    ('Derschutze', ['derschutze sakura', 'derschutze angel']),
    ('Moose Knuckles', ['moose knuckles']),
    ('MCM', ['mcm stark']),
    ('Rimowa', ['rimowa']),
    
    # Sport
    ('FC Barcelona', ['cactus jack x fc barcelona', 'barcelona 24/25']),
    ('Real Madrid', ['real madrid 24/25']),
    ('Santos FC', ['santos fc']),
    
    # Misc
    ('Murtaya', ['murtaya baggy']),
    ('Scff', ['scff logo']),
]

def detect_brand(title):
    title_lower = title.lower()
    for brand, keywords in BRAND_RULES:
        for kw in keywords:
            if kw.lower() in title_lower:
                return brand
    return None

updated = 0
no_brand = []
for p in products:
    detected = detect_brand(p['title'])
    if detected:
        if p.get('brand') != detected:
            p['brand'] = detected
            updated += 1
    else:
        no_brand.append((p['id'], p['title']))

print(f"Updated brand for {updated} products.")
print(f"No brand detected for {len(no_brand)} products.")
# Show first 20 no-brand
for pid, title in no_brand[:20]:
    print(f"  ID {pid}: {title}")

output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
output += """
// Brand Field Corrected
const DB_VERSION = 'v26_brand_fixed';
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
print("Saved!")
