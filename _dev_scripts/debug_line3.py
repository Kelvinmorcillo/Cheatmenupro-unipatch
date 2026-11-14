#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

# Search for onclick with building_coal_mine
pattern = r'GetVariableSystem\.Set.*building_coal_mine'
matches = re.findall(pattern, content)
if matches:
    print('Found', len(matches), 'matches')
    for m in matches[:1]:
        print('Full onclick:')
        print(m)
else:
    print('No matches found')
    # Try direct search
    idx = content.find("'building_coal_mine'")
    print(f"Found 'building_coal_mine' at position {idx}")
    if idx >= 0:
        # Print 300 chars before and 300 after
        start = max(0, idx - 200)
        end = min(len(content), idx + 300)
        print("Context:")
        print(content[start:end])