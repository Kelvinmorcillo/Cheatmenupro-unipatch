#!/usr/bin/env python
import re

sfx_filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\scripted_guis\zz_cmpu_scripted_guis.txt'
with open(sfx_filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
fixed = 0
i = 0
while i < len(lines):
    line = lines[i]
    # Find lines with set_variable = { name = sakuya_b6_build_sel_X value = 1 }
    m = re.search(r"set_variable = \{ name = (sakuya_b6_build_sel_\w+) value = 1 \}", line)
    if m:
        build_var = m.group(1)
        building_name = build_var.replace('sakuya_b6_build_sel_', 'building_')
        indent = line[:len(line) - len(line.lstrip())]
        # Keep the existing line
        new_lines.append(line)
        # Add set_variable for sakuya_b6_selected_building after it
        new_lines.append(indent + "set_variable = { name = sakuya_b6_selected_building value = " + building_name + " }")
        fixed += 1
    else:
        new_lines.append(line)
    i += 1

with open(sfx_filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_lines))
print('Added set_variable = { name = sakuya_b6_selected_building } to ' + str(fixed) + ' cmpu_select_X entries')

# Verify
with open(sfx_filepath, 'r', errors='replace') as f:
    check = f.read()
selected_count = check.count('set_variable = { name = sakuya_b6_selected_building')
build_count = check.count('set_variable = { name = sakuya_b6_build_sel')
undefined = check.count('sakuya_b6_build_select_building_effect')
print('set_variable (selected_building): ' + str(selected_count))
print('set_variable (build_sel): ' + str(build_count))
print('undefined effects remaining: ' + str(undefined))

# Show one example
for line in new_lines:
    if 'sakuya_b6_selected_building' in line and 'set_variable' in line:
        print()
        print('Example: ' + line)
        break