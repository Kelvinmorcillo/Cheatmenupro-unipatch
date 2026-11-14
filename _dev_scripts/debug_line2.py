#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

# Find the line with building_coal_mine and onclick
import re
# Search for the pattern
pattern = r'onclick.*?building_coal_mine'
matches = re.findall(pattern, content, re.DOTALL)
if matches:
    print('Found', len(matches), 'matches')
    for m in matches[:1]:
        print('Full onclick:')
        print(m[:500])
else:
    print('No matches found with that pattern')
    # Try simpler search
    idx = content.find('building_coal_mine')
    print(f'Found building_coal_mine at position {idx}')
    # Print surrounding context
    start = max(0, idx - 100)
    end = min(len(content), idx + 500)
    print('Context:')
    print(content[start:end])