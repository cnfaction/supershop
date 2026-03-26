import json

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('= [') + 2
end = text.rfind('];') + 1
products = json.loads(text[start:end])

# Check range around 10056
print("Range 10050-10065:")
for p in products:
    if 10050 <= p['id'] <= 10065:
        print(f"ID {p['id']}: {p['title']} | DESC prefix: {p.get('description', '')[:20]}")

# Check range around 10234
print("\nRange 10230-10245:")
for p in products:
    if 10230 <= p['id'] <= 10245:
        print(f"ID {p['id']}: {p['title']} | DESC prefix: {p.get('description', '')[:20]}")
