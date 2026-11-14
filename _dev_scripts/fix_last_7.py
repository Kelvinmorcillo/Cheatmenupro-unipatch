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
    # Check for onclick with [GetScriptedGui('cmpu_select_X')] pattern (missing Set call)
    if stripped.startswith('onclick = "[GetScriptedGui') and 'cmpu_select_' in stripped:
        bn_match = re.search(r"cmpu_select_([^']+)", stripped)
        if bn_match:
            building_name = 'building_' + bn_match.group(1)
            indent = line[:len(line) - len(line.lstrip())]
            # Replace onclick = "[GetScriptedGui('cmpu_select_X').Execute(...)]"
            # With:    onclick = "[GetVariableSystem.Set('sakuya_b6_selected_building', 'building_X'); GetScriptedGui('cmpu_select_X').Execute(...)]"
            old_part = 'onclick = "[GetScriptedGui(\'' + bn_match.group(0).split(\"cmpu_select_\")[1].split(\"'\")[0] + '\')'
            # Simpler: just replace the onclick prefix
            new_onclick_prefix = "onclick = \"[GetVariableSystem.Set('sakuya_b6_selected_building', '" + building_name + "'); "
            # Find the position after onclick = "[
            after_prefix = line.index('onclick = "[') + len('onclick = "[')
            # Everything after "onclick = "[
            rest = line[after_prefix:]
            # rest starts with GetScriptedGui('cmpu_select_X')...
            # We want to insert GetVariableSystem.Set(...) before GetScriptedGui
            new_line = indent + 'onclick = "[GetVariableSystem.Set(\'sakuya_b6_selected_building\', \'' + building_name + '\'); ' + rest
            new_lines.append(new_line)
            fixed += 1
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_lines))
print('Fixed ' + str(fixed) + ' remaining onclick handlers')

# Final verification
count_correct = 0
count_missing = 0
for line in new_lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped and '); GetScriptedGui' in stripped:
        count_correct += 1
    elif stripped.startswith('onclick = "') and 'cmpu_select_' in stripped:
        count_missing += 1
        print('  STILL MISSING: ' + stripped[:100])
print('Correct format: ' + str(count_correct))
print('Still missing: ' + str(count_missing))
print()
print('DONE')