import re

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

sku_images = re.findall(r'\"(p_images/prod_.*?/SKU_.*?\.jpg)\"', text)
bad_sku = [s for s in sku_images if '?' in s]
print("Total SKU images: " + str(len(sku_images)))
print("Broken SKU images: " + str(len(bad_sku)))
for s in bad_sku[:20]:
    print("  " + s)
