import re
import os

def sanitize_data():
    with open('data.js', 'rb') as f:
        content_bin = f.read()
    
    # Try to decode safely, replacing bad bytes
    content = content_bin.decode('utf-8', errors='replace')
    
    # Find the array content
    start_tag = 'const initialProducts = ['
    end_tag = '];'
    
    start_idx = content.find(start_tag)
    end_idx = content.rfind(end_tag)
    
    if start_idx == -1 or end_idx == -1:
        print("Could not find delimiters")
        return
        
    prefix = content[:start_idx + len(start_tag)]
    array_content = content[start_idx + len(start_tag):end_idx]
    suffix = content[end_idx:]
    
    # Remove literal control characters inside strings that break JSON
    # ASCII 0-31 are control chars. We want to keep space (32) and etc.
    # But literal tabs or newlines inside JSON values are forbidden.
    # Wait, indenting whitespace is fine, but INSIDE "..." it's not.
    # We'll just replace all non-printables except for standard whitespace used in formatting.
    
    # Regex to find unescaped control characters
    # Actually, a simpler way: preserve \n and spaces, but kill others like \r, \x00, etc.
    cleaned_items = []
    # Preserve \x0a (newline) and \x20-\x7e (printables) and higher (utf-8)
    def clean_char(c):
        o = ord(c)
        if o < 32 and c not in ['\n', '\r', '\t']:
            return '' # Nuke control char
        return c
        
    cleaned_array = "".join(clean_char(c) for c in array_content)
    
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(prefix + cleaned_array + suffix)
    
    print("Sanitization complete.")

if __name__ == "__main__":
    sanitize_data()
