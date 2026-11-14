#!/usr/bin/env python
import re

# Fix onclick handlers: proper [ ] brackets, combine Set + cmpu_select_X
filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
fixed = 0

for line in lines:
    if 'onclick' in line.lower() and 'cmpu_select_' in line:
        # Check if already has correct format: onclick = "[GetVariableSystem.Set(...); GetScriptedGui(...)]"
        if line.startswith('onclick = "[GetVariableSystem.Set') and '); GetScriptedGui' in line:
            new_lines.append(line)  # Already correct
        elif line.startswith('onclick = "GetScriptedGui'):
            # Missing [ ] brackets and Set call - need to rebuild
            bn_match = re.search(r"cmpu_select_([^']+)", line)
            if bn_match:
                building_name = 'building_' + bn_match.group(1)
                new_line = 'onclick = "[GetVariableSystem.Set(\'sakuya_b6_selected_building\', \'' + building_name + '\'); ' + line[len('onclick = "'):]
                new_lines.append(new_line)
                fixed += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_lines))
print('Fixed ' + str(fixed) + ' onclick handlers')

# Verify
lines2 = new_lines
count_correct = 0
count_missing = 0
for line in lines2:
    if 'onclick' in line.lower() and 'cmpu_select_' in line:
        if line.startswith('onclick = "[GetVariableSystem.Set') and '); GetScriptedGui' in line:
            count_correct += 1
        else:
            count_missing += 1
            print('  MISSING: ' + line[:100])
print('Correct format: ' + str(count_correct))
print('Missing format: ' + str(count_missing))