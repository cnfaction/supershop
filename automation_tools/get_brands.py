import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

brands = sorted(list(set(re.findall(r'"brand"\s*:\s*"(.*?)"', text))))
with open('brands.txt', 'w', encoding='utf-8') as f:
    for b in brands:
        if b:
            f.write(b + '\n')
