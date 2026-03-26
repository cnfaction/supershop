import re
import os

def sanitize_data():
    with open('data.js', 'rb') as f:
        content_bin = f.read()
    
    # Try to decode safely, replacing bad bytes
    content = content_bin.decode('utf-8', errors='replace')
    
    # regex for all ASCII control characters except \n and \r
    # [\x00-\x09\x0b-\x0c\x0e-\x1f]
    # We'll replace them with space
    sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', ' ', content)
    
    # Also we'll replace literal tabs (\x09) with spaces to be extra safe for JSON parsing
    sanitized = sanitized.replace('\t', ' ')
    
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(sanitized)
    
    print("Sanitization complete.")

if __name__ == "__main__":
    sanitize_data()
