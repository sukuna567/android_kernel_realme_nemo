import re
import sys

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Regex to match add_page_to_lru_list or add_page_to_lru_list_tail with 3 arguments
    # We want to match: add_page_to_lru_list(arg1, arg2, arg3)
    # Since arg3 might be multi-word or function call (like page_lru(page)), we need a careful regex.
    # Actually, a simpler regex for the specific lines is easier.
    
    lines = content.split('\n')
    for i in range(len(lines)):
        line = lines[i]
        if 'add_page_to_lru_list' in line:
            # We match `add_page_to_lru_list(a, b, c)` and replace with `add_page_to_lru_list(a, b)`
            # Because we might have nested parens (e.g. `page_lru(page)`), we split by comma carefully or just use regex.
            # Known patterns from grep:
            # add_page_to_lru_list_tail(page, lruvec, page_lru(page));
            # add_page_to_lru_list(page, lruvec, lru);
            # add_page_to_lru_list(page, lruvec, LRU_UNEVICTABLE);
            # add_page_to_lru_list(page, lruvec, LRU_INACTIVE_FILE);
            # add_page_to_lru_list(page_tail, lruvec, page_lru(page_tail));
            # add_page_to_lru_list(page, lruvec);  <- already fixed
            
            line = re.sub(r'(add_page_to_lru_list_tail\([^,]+,\s*[^,]+),\s*[^)]+(?:\([^)]*\))?\)', r'\1)', line)
            line = re.sub(r'(add_page_to_lru_list\([^,]+,\s*[^,]+),\s*[^)]+(?:\([^)]*\))?\)', r'\1)', line)
            lines[i] = line
            
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines))

process_file('mm/swap.c')
process_file('mm/memcontrol.c')
print("Done")
