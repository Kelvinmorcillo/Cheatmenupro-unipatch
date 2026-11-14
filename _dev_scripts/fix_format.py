#!/usr/bin/env python
# Fix onclick format: ensure '); ' exists after building name before GetVariableSystem.Clear
import re

with open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
fixed = 0

for line in lines:
    # Check if this line has the broken format
    # Pattern: GetVariableSystem.Set with building name, then GetVariableSystem.Clear without '); ' in between
    if 'GetVariableSystem.Set' in line and "'building_" in line and "GetVariableSystem.Clear" in line:
        # Find position of GetVariableSystem.Clear
        clear_pos = line.find('GetVariableSystem.Clear')
        if clear_pos >= 0:
            # What's before GetVariableSystem.Clear?
            before_clear = line[:clear_pos]
            # Check if it already ends with ');'
            if before_clear.rstrip().endswith("');"):
                # Already correct, keep as-is
                new_lines.append(line)
                continue
            else:
                # Insert '); ' before GetVariableSystem.Clear
                new_line = line[:clear_pos] + '); GetVariableSystem.Clear'
                new_lines.append(new_line)
                fixed += 1
                continue
    new_lines.append(line)

with open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print(f'Fixed {fixed} lines')