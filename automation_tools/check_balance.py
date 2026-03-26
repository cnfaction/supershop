import os

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print("File Length: " + str(len(text)))
print("Left Braces: " + str(text.count('{')))
print("Right Braces: " + str(text.count('}')))
print("Left Brackets: " + str(text.count('[')))
print("Right Brackets: " + str(text.count(']')))
print("Double Quotes: " + str(text.count('"')))
