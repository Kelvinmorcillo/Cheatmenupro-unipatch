#!/usr/bin/env python
import re

# Verify sakuya_main.gui onclick handlers
filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
count_correct = 0
count_wrong = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        # Check: onclick = "[...]" format with ] before closing "
        if stripped.endswith(']') and not stripped.endswith(']]'):
            count_correct += 1
        else:
            count_wrong += 1
            print('  WRONG: ' + stripped[:120])

print('Onclick handlers - Correct: ' + str(count_correct) + ', Wrong: ' + str(count_wrong))

# Verify cmpu_select_X scripted GUIs
filepath2 = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\scripted_guis\zz_cmpu_scripted_guis.txt'
with open(filepath2, 'r', errors='replace') as f:
    content2 = f.read()

remaining = content2.count('sakuya_b6_build_select_building_effect')
set_vars = content2.count('set_variable = { name = sakuya_b6_build_sel')
print()
print('Scripted GUIs - undefined effects remaining: ' + str(remaining))
print('Scripted GUIs - set_variable entries: ' + str(set_vars))

# Verify script values
filepath3 = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\script_values\cmpu_feedback_values.txt'
with open(filepath3, 'r', errors='replace') as f:
    content3 = f.read()

has_list = 'cmpu_fb_marked_states_list = {}' in content3
print()
print('Script values - cmpu_fb_marked_states_list present: ' + str(has_list))