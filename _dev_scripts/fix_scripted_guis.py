#!/usr/bin/env python
"""
Fix cmpu_select_X scripted GUIs to use set_variable directly instead of
the undefined sakuya_b6_build_select_building_effect.

Current (broken):
    effect = {
        cmpu_b6_build_clear_all_selected_effect = yes
        sakuya_b6_build_select_building_effect = { VAR = sakuya_b6_build_sel_X }
    }

Fixed:
    effect = {
        cmpu_b6_build_clear_all_selected_effect = yes
        set_variable = { name = sakuya_b6_build_sel_X value = 1 }
    }
"""

import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\scripted_guis\zz_cmpu_scripted_guis.txt'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

# Pattern to match: sakuya_b6_build_select_building_effect = { VAR = sakuya_b6_build_sel_X }
# Replace with: set_variable = { name = sakuya_b6_build_sel_X value = 1 }
pattern = r"sakuya_b6_build_select_building_effect = \{ VAR = (sakuya_b6_build_sel_\w+) \}"
replacement = r"set_variable = { name = \1 value = 1 }"

new_content = re.sub(pattern, replacement, content)

# Count replacements
count = len(re.findall(pattern, content))

with open(filepath, 'w', errors='replace') as f:
    f.write(new_content)

print('Replaced ' + str(count) + ' occurrences of sakuya_b6_build_select_building_effect')
print('Total lines in file: ' + str(len(content.split(chr(10)))))