import os

path = 'c:/Users/Administrator/Desktop/新建文件夹/网站/data.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

new_footer = """
// Sync with localStorage 
const DB_VERSION = 'v14_final_fix';
try {
    const val = localStorage.getItem('db_version');
    if (val !== DB_VERSION) {
        localStorage.setItem('products', JSON.stringify(initialProducts));
        localStorage.setItem('db_version', DB_VERSION);
        console.log('Database synced to ' + DB_VERSION);
    }
} catch (e) {
    console.warn('LocalStorage error:', e);
}

function getProducts() {
    try {
        const stored = localStorage.getItem('products');
        if (stored) return JSON.parse(stored);
    } catch (e) {
        console.warn('LocalStorage parse error:', e);
    }
    return initialProducts;
}

function saveProducts(products) {
    try {
        localStorage.setItem('products', JSON.stringify(products));
    } catch (e) {
        console.warn('LocalStorage save error:', e);
    }
}
"""

end_idx = text.find('];') # Use find instead of rfind to be sure we get the FIRST one if there are multiple (should only be one)
# Actually, wait, initialProducts ends at the LAST ]; if it's nested?
# No, it's the top level one.

if end_idx != -1:
    content_until_array = text[:end_idx + 2]
    # Clean up any trailing stuff after ]; that might have been partially written
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content_until_array + "\n" + new_footer)
    print("Updated data.js Successfully")
else:
    print("Could not find array end")
