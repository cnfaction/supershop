import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

check_ids = [10354, 10226, 10107, 10034, 10056, 10296, 10140, 10093, 10273]
for p in products:
    if p['id'] in check_ids:
        print(f"ID {p['id']}: {p['title']} | brand={p['brand']}")

nike_count = sum(1 for p in products if p.get('brand') == 'Nike')
print(f"\nTotal Nike-branded products: {nike_count}")

# Show which have Nike brand
print("\nNike-branded products:")
for p in products:
    if p.get('brand') == 'Nike':
        print(f"  ID {p['id']}: {p['title']}")
