#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

# Replace )]]" with )]" in onclick lines only
# Pattern: onclick = "[...Execute(...).End)]]"
# Replace with: onclick = "[...Execute(...).End)]"
lines = content.split('\n')
new_lines = []
fixed = 0

for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        # Check for double ]] before closing "
        if stripped.endswith(']"]') and ']]' in stripped:
            # Replace )]]" with )]"
            indent = line[:len(line) - len(line.lstrip())]
            # Find the position of the last ) before the ]]"
            # Replace )]]" with )]"
            new_stripped = stripped.replace(')]"]', ')]"')
            new_line = indent + new_stripped
            new_lines.append(new_line)
            fixed += 1
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_lines))
print('Fixed double bracket in ' + str(fixed) + ' onclick handlers')

# Final verification
count_correct = 0
count_wrong = 0
for line in new_lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        if stripped.endswith(']")') and ']]' not in stripped:
            count_correct += 1
        else:
            count_wrong += 1
            print('  WRONG: ' + stripped[:120])
print('Correct format: ' + str(count_correct))
print('Wrong format: ' + str(count_wrong))
print()
print('DONE')