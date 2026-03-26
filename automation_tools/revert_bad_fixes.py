import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Revert all the wrong auto-fixes that produced generic names like "Nike Item", "Soccer Item" etc.
# These are obviously wrong - the script detected "nike" in zh title and overwrote a perfectly
# good English title with a generic one.
REVERT = {
    "10296": "Prada America's Cup Sneakers",
    "10276": "FOG Essentials Zip-Up Sweatpants",
    "10174": "Corteiz RTW All World Reservation Reflective Hoodie",
    "10020": "Golden Goose Super-Star Sneakers",
    "10042": "Christian Louboutin Louis Orlato Spiked Sneakers",
    "10056": "Derschutze Sakura Embroidery Jeans",
    "10336": "Stone Island Logo Patch Full-Zip Hoodie",
    "10130": "Air Jordan 4 Retro Collection",
    "10227": "Balenciaga Graffiti Print Zip-Up Hoodie",
    "10354": "Denim Tears Cotton Wreath Hoodie",
    "10226": "Dior B30 Sneaker White Mesh",
    "10264": "Palm Angels Reflective Windbreaker",
    "10134": "Balenciaga Track Sneaker White/Orange",
    "10381": "Louis Vuitton Trainer Sneaker White/Blue",
    "10311": "Chrome Hearts Horseshoe Logo Hoodie",
    "10111": "Stussy 8 Ball Logo Tee Black",
    "10348": "Moncler x Valentino Puffer Jacket",
    "10268": "Balenciaga Triple S Sneaker Clear Sole",
    "10170": "Off-White x Air Jordan 1 Retro High OG Chicago",
    "10035": "Supreme x Umbro Track Jacket",
    "10175": "Maison Margiela Replica Sneakers",
    "10307": "Hellstar Hoodie",
    "10125": "Gucci Double G Buckle Leather Belt",
    "10274": "Givenchy City Court Canvas Sneakers",
    "10303": "Christian Louboutin Louis Junior Spikes Sneaker",
    "10358": "Denim Tears Cotton Wreath Hoodie",
    "10331": "New Balance 9060 Sea Salt",
    "10340": "Travis Scott x Air Jordan 1 Low Reverse Mocha",
    "10108": "Supreme x Umbro Tracksuit",
    "10378": "Rick Owens DRKSHDW Drawstring Sweatpants",
    "10083": "Dior B23 High-Top 'Oblique'",
    "10198": "Polo Ralph Lauren Cardigan Sweater",
    "10356": "Nike Tech Fleece Tracksuit Set",
    "10287": "Nike Air Max Plus 3 TN Retro",
    "10257": "Nike ACG Sleeveless Vest",
    "10365": "Chrome Hearts Horseshoe Logo Hoodie",
    "10352": "Nike Air Max Plus TN Retro",
    "10357": "Nike Dunk Low Retro Sneakers",
    "10266": "FOG Essentials Sweat Shorts",
    "10208": "Jordan Jumpman Sweatpants",
    "10224": "Vlone Friends Mosaic Logo Hoodie",
    "10355": "Gallery Dept. Painted Flare & Splatter Sweatpants",
    "10383": "Yeezy Gap Round Jacket",
    "10278": "Chrome Hearts Cross Logo Hat",
    "10183": "Football National Team Training Tracksuit",
    "10150": "ASICS x JJJJound Gel-Kayano 14",
    "10295": "Cactus Jack x FC Barcelona 24/25 Home Jersey",
    "10006": "FOG Essentials Zip-Back Sweatpants",
    "10148": "New Balance 990v3 Core Grey",
    "10387": "Chrome Hearts T-Shirt",
    "10147": "New Balance 9060 'Rain Cloud'",
    "10129": "Chrome Hearts Cross Logo Tee",
    "10337": "Nike Football Training Jersey",
    "10225": "Nike Futura Logo Cap",
    "10114": "Syna World Classic Logo Hoodie",
    "10017": "Nike Running Pants",
    "10103": "Nike Mid-Cut Crew Socks",
    "10267": "Chrome Hearts Cross Socks",
    "10011": "Nike T-Shirt",
}

reverted = 0
for p in products:
    pid_str = str(int(p['id']))
    if pid_str in REVERT:
        p['title'] = REVERT[pid_str]
        reverted += 1

# Also fix Balenciaga 10034 which was correct
for p in products:
    if p['id'] == 10034:
        p['title'] = "Balenciaga Track Sneaker 'Graffiti'"
        p['brand'] = 'Balenciaga'

print(f"Reverted/fixed {reverted + 1} products.")

output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
output += """
// Alignment Corrected
const DB_VERSION = 'v25_alignment_corrected';
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
print("Saved.")
