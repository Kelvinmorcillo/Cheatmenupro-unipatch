#!/usr/bin/env python
# Fix broken onclick handlers - restore '); ' before GetVariableSystem.Clear
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
fixed = 0

for i, line in enumerate(lines):
    # Check if this line has the broken format:
    # 'building_X' GetVariableSystem.Clear (missing '); ' before GetVariableSystem.Clear
    if 'sakuya_b6_selected_building' in line and 'GetVariableSystem.Clear' in line and '\", ' not in line:
        # Find position of 'GetVariableSystem.Clear'
        clear_pos = line.find('GetVariableSystem.Clear')
        if clear_pos >= 0:
            # Insert '); ' before GetVariableSystem.Clear
            new_line = line[:clear_pos] + '); ' + line[clear_pos:]
            lines[i] = new_line
            fixed += 1

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'Fixed {fixed} lines')