#!/usr/bin/env python
import re

f = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', errors='replace')
c = f.read()
f.close()
lines = c.split('\n')

print('=== Analyzing backup onclick handlers ===')
print()

# Show first 3 onclick lines
count = 0
for i, line in enumerate(lines):
    if 'onclick' in line.lower() and 'cmpu_select_' in line:
        if count < 3:
            print('Line ' + str(i) + ':')
            print(line)
            print()
        count += 1
print('Total onclick with cmpu_select_: ' + str(count))

# Count all onclick lines
total_onclick = sum(1 for line in lines if 'onclick' in line.lower())
print('Total onclick lines: ' + str(total_onclick))

# Check for the pattern in backup
has_set = sum(1 for line in lines if 'sakuya_b6_selected_building' in line and 'onclick' in line.lower())
print('Onclick with sakuya_b6_selected_building: ' + str(has_set))

has_clear = sum(1 for line in lines if 'GetVariableSystem.Clear' in line and 'onclick' in line.lower())
print('Onclick with GetVariableSystem.Clear: ' + str(has_clear))

has_getscript = sum(1 for line in lines if 'GetScriptedGui' in line and 'onclick' in line.lower())
print('Onclick with GetScriptedGui: ' + str(has_getscript))