import re
import os

def sanitize_data():
    with open('data.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Nuke all control characters except \n and spaces
    # \t -> space, \r -> nothing
    content = content.replace('\r', '')
    content = content.replace('\t', ' ')
    
    # regex for all ASCII control characters [\x00-\x1F]
    # At this point only \x0a (\n) should remain of interest for formatting.
    # Nuke the rest
    fixed = re.sub(r'[\x00-\x09\x0b-\x1f]', '', content)
    
    with open('data.js', 'w', encoding='utf-8', newline='\n') as f:
        f.write(fixed)
    
    print("Sanitization complete. (Final v3)")

if __name__ == "__main__":
    sanitize_data()
