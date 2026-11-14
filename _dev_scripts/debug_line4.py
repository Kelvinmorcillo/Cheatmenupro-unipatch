#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

# Search for the onclick with building_coal_mine - get the full line
# Find position of 'building_coal_mine'
idx = content.find("'building_coal_mine'")
print(f"Found at position: {idx}")

# Get the onclick line - we need to find the line containing this
lines = content.split('\n')
for i, line in enumerate(lines):
    if "'building_coal_mine'" in line:
        print(f'Line {i}:')
        print(line)
        # Print the full line content
        print()
        print('Full line content:')
        print(line)
        break