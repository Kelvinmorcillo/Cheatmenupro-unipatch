#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
fixed = 0

for line in lines:
    stripped = line.strip()
    # Check if onclick with cmpu_select_ but missing closing ]
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        if not stripped.endswith(']")'):
            # Missing ] before closing "
            indent = line[:len(line) - len(line.lstrip())]
            new_line = indent + stripped[:-1] + ']")'
            new_lines.append(new_line)
            fixed += 1
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_lines))
print('Added ] to ' + str(fixed) + ' onclick handlers')

# Final verification
count_correct = 0
count_missing = 0
for line in new_lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped and stripped.endswith(']")'):
        count_correct += 1
    elif stripped.startswith('onclick = "') and 'cmpu_select_' in stripped:
        count_missing += 1
        print('  STILL BROKEN: ' + stripped[:100])
print('Correct format: ' + str(count_correct))
print('Still missing: ' + str(count_missing))
print()
print('DONE')