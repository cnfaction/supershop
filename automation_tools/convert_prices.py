import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# 设定汇率 (1 USD = 7.2 CNY 左右)
# 我们将价格除以 7.2
EXCHANGE_RATE = 7.2

print("Starting price conversion (CNY -> USD)...")

for p in products:
    old_price = p.get('price', 0)
    # 计算美金价格并保留两位小数，或者取整让其看起来更像美金标价
    # 我们选择保留到 0.99 这种风格或者直接取整
    new_price = round(old_price / EXCHANGE_RATE, 2)
    
    # 打印前几个看看效果
    if products.index(p) < 5:
        print(f"ID {p['id']}: Original {old_price} CNY -> {new_price} USD")
    
    p['price'] = new_price

output = "const initialProducts = " + json.dumps(products, indent=2, ensure_ascii=False) + ";"
output += """
// Price Conversion Complete (CNY -> USD)
const DB_VERSION = 'v32_price_usd_final';
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

print(f"\nSuccessfully converted {len(products)} products to USD.")
