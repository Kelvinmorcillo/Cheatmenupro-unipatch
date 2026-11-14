#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

# Find the coal mine onclick line
idx = content.find('cmpu_select_coal_mine')
# Print 500 chars from that position
print('Coal mine onclick (500 chars from find):')
print(content[idx:idx+500])