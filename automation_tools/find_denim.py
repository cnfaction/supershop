import re

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Denim Tears" in line:
        print("Line " + str(i+1) + ": " + line.strip())
