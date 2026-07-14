import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove `lru += LRU_ACTIVE;`
    content = content.replace('lru += LRU_ACTIVE;', '')
    
    with open(filepath, 'w') as f:
        f.write(content)

process_file('mm/swap.c')
print("Done")
