import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Build a map of known brand keywords in titles
# If the title contains brand X but brand field is Y, that's a mismatch
TITLE_TO_BRAND = {
    'balenciaga': 'Balenciaga',
    'dior': 'Dior',
    'gucci': 'Gucci',
    'louis vuitton': 'Louis Vuitton',
    'chanel': 'Chanel',
    'prada': 'Prada',
    'burberry': 'Burberry',
    'valentino': 'Valentino',
    'fendi': 'Fendi',
    'versace': 'Versace',
    'givenchy': 'Givenchy',
    'off-white': 'Off-White',
    'denim tears': 'Denim Tears',
    'gallery dept': 'Gallery Dept.',
    'chrome hearts': 'Chrome Hearts',
    'fear of god': 'Fear of God',
    'fog essentials': 'Fear of God',
    'corteiz': 'Corteiz',
    'sp5der': 'Sp5der',
    'hellstar': 'Hellstar',
    'vlone': 'Vlone',
    'stussy': 'Stussy',
    'bape': 'BAPE',
    'supreme': 'Supreme',
    'carhartt': 'Carhartt',
    'purple brand': 'Purple Brand',
    'palm angels': 'Palm Angels',
    'vetements': 'Vetements',
    'casablanca': 'Casablanca',
    'ami paris': 'Ami Paris',
    'comme des': 'Comme des Garçons',
    'acne studios': 'Acne Studios',
    'syna world': 'Syna World',
    'rick owens': 'Rick Owens',
    'moncler': 'Moncler',
    'canada goose': 'Canada Goose',
    'stone island': 'Stone Island',
    'c.p. company': 'C.P. Company',
    'alo yoga': 'Alo Yoga',
    'maison margiela': 'Maison Margiela',
    'mihara yasuhiro': 'Mihara Yasuhiro',
    'golden goose': 'Golden Goose',
    'polo ralph lauren': 'Polo Ralph Lauren',
    'lacoste': 'Lacoste',
    'air jordan': 'Jordan',
    'travis scott x air jordan': 'Jordan',
    'asics': 'ASICS',
    'new balance': 'New Balance',
    'adidas': 'Adidas',
    'yeezy': 'Yeezy',
    'apple': 'Apple',
    'ugg': 'UGG',
    'christian louboutin': 'Christian Louboutin',
    'amiri': 'Amiri',
    'saint laurent': 'Saint Laurent',
    'the north face': 'The North Face',
    "arc'teryx": "Arc'teryx",
    'moose knuckles': 'Moose Knuckles',
    'mcm': 'MCM',
    'derschutze': 'Derschutze',
}

mismatches = []
for p in products:
    title_lower = p['title'].lower()
    current_brand = p.get('brand', '')
    
    for keyword, expected_brand in TITLE_TO_BRAND.items():
        if keyword in title_lower:
            if current_brand != expected_brand:
                mismatches.append({
                    'id': p['id'],
                    'title': p['title'],
                    'current_brand': current_brand,
                    'expected_brand': expected_brand
                })
            break

print(f"Brand mismatches found: {len(mismatches)}")
for m in mismatches:
    print(f"  ID {m['id']}: '{m['title'][:50]}' | brand='{m['current_brand']}' (should be '{m['expected_brand']}')")
