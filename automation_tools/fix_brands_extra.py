import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Additional brand corrections for undetected ones
extra_fixes = {
    "10131": "Apple",
    "10290": "UGG",
    "10275": "Defcropped",
    "10042": "Christian Louboutin",
    "10027": "Apple",
    "10303": "Christian Louboutin",
    "10060": "Christian Louboutin",
    "10059": "Christian Louboutin",
    "10026": "Amiri",
    "10219": "Saint Laurent",
    "10360": "Saint Alexander",
    "10163": "The North Face",
    "10118": "Dior",
    "10136": "Balenciaga",
    "10251": "Arc'teryx",
    "10109": "Arc'teryx",
    "10301": "Nike",
    "10102": "Nike",
    "10101": "Nike",
    "10049": "C.P. Company",
    "10036": "Corteiz",
    "10019": "Multi-Club",
    "10093": "Rick Owens",
    "10074": "Stussy",
    "10083": "Dior",
    "10104": "Stussy",
    "10113": "Syna World",
    "10117": "Louis Vuitton",
    "10138": "NBA",
    "10142": "Ami Paris",
    "10148": "New Balance",
    "10147": "New Balance",
    "10150": "ASICS",
    "10151": "ASICS",
    "10154": "Chrome Hearts",
    "10157": "Moose Knuckles",
    "10162": "C.P. Company",
    "10182": "Acne Studios",
    "10197": "Nike",
    "10200": "Corteiz",
    "10201": "Corteiz",
    "10202": "Louis Vuitton",
    "10204": "Gucci",
    "10233": "Stone Island",
    "10237": "Nike",
    "10243": "Chrome Hearts",
    "10248": "Casablanca",
    "10250": "Chrome Hearts",
    "10253": "Burberry",
    "10254": "Chanel",
    "10261": "Nike",
    "10263": "American Vintage",
    "10281": "Louis Vuitton",
    "10282": "Chrome Hearts",
    "10283": "Chrome Hearts",
    "10289": "Hellstar",
    "10292": "Nike",
    "10296": "Prada",
    "10298": "Nike",
    "10300": "Retro Football",
    "10304": "Polo Ralph Lauren",
    "10306": "Nike",
    "10307": "Hellstar",
    "10308": "Chrome Hearts",
    "10310": "Chanel",
    "10311": "Chrome Hearts",
    "10312": "Gucci",
    "10314": "Balenciaga",
    "10318": "Purple Brand",
    "10319": "Stussy",
    "10320": "Nike",
    "10321": "Versace",
    "10322": "Polo Ralph Lauren",
    "10324": "Comme des Garçons",
    "10329": "Nike",
    "10333": "Fear of God",
    "10334": "Fear of God",
    "10341": "Polo Ralph Lauren",
    "10342": "Fear of God",
    "10343": "Alo Yoga",
    "10344": "Adidas",
    "10354": "Denim Tears",
    "10356": "Nike",
    "10358": "Denim Tears",
    "10361": "Corteiz",
    "10362": "Dior",
    "10363": "Polo Ralph Lauren",
    "10365": "Chrome Hearts",
    "10366": "Denim Tears",
    "10368": "Corteiz",
    "10370": "Polo Ralph Lauren",
    "10371": "Chrome Hearts",
    "10372": "Louis Vuitton",
    "10373": "Rimowa",
    "10374": "Acne Studios",
    "10375": "Nike",
    "10376": "Nike",
    "10377": "Prada",
    "10378": "Rick Owens",
    "10380": "Balenciaga",
    "10382": "Chrome Hearts",
    "10384": "Nike",
    "10385": "Nike",
    "10386": "Canada Goose",
    "10387": "Chrome Hearts",
    "10388": "Moncler",
    "10390": "Hermes",
    "10391": "Fear of God",
    "10392": "Hellstar",
}

updated = 0
for p in products:
    pid_str = str(int(p['id']))
    if pid_str in extra_fixes:
        if p.get('brand') != extra_fixes[pid_str]:
            p['brand'] = extra_fixes[pid_str]
            updated += 1

print(f"Extra brand fixed: {updated}")

output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
output += """
// Brand Field Final
const DB_VERSION = 'v27_brand_final';
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
