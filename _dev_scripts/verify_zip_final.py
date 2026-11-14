#!/usr/bin/env python
import zipfile

z = zipfile.ZipFile(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\clean_fix_final.zip', 'r')

# Check GUI onclick
content = z.read('gui/main/sakuya_main.gui').decode('utf-8', errors='replace')
lines = content.split('\n')
correct = 0
wrong = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        if len(stripped) >= 2 and stripped[-2] == ']' and stripped[-1] == '"':
            if len(stripped) >= 3 and stripped[-3] != ']':
                correct += 1
            else:
                wrong += 1
        else:
            wrong += 1
print('GUI onclick - Correct: ' + str(correct) + ', Wrong: ' + str(wrong))

# Check scripted GUIs
sfx = z.read('common/scripted_guis/zz_cmpu_scripted_guis.txt').decode('utf-8', errors='replace')
print('Scripted GUIs - undefined effects: ' + str(sfx.count('sakuya_b6_build_select_building_effect')))
print('Scripted GUIs - set_variable entries: ' + str(sfx.count('set_variable = { name = sakuya_b6_build_sel')))

# Check script values
sv = z.read('common/script_values/cmpu_feedback_values.txt').decode('utf-8', errors='replace')
print('Script values - list init: ' + str('cmpu_fb_marked_states_list = {}' in sv))

# Show sample onclick
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_coal_mine' in stripped:
        print()
        print('Sample onclick:')
        print(stripped)
        break

z.close()