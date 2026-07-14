import re
import sys

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace('add_page_to_lru_list_tail(page, lruvec));', 'add_page_to_lru_list_tail(page, lruvec);')
    content = content.replace('add_page_to_lru_list(page_tail, lruvec));', 'add_page_to_lru_list(page_tail, lruvec);')
    content = content.replace('add_page_to_lru_list(page, lruvec));', 'add_page_to_lru_list(page, lruvec);')
            
    with open(filepath, 'w') as f:
        f.write(content)

process_file('mm/swap.c')
process_file('mm/memcontrol.c')
print("Done")
