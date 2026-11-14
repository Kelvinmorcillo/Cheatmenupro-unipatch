#!/usr/bin/env python
import zipfile

z = zipfile.ZipFile(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\clean_fix_final.zip', 'r')

print('Files in zip:')
for name in z.namelist():
    print('  ' + name + ' (' + str(z.getinfo(name).file_size) + ' bytes)')

# Verify GUI onclick in zip
content = z.read('gui/main/sakuya_main.gui').decode('utf-8', errors='replace')
lines = content.split('\n')
count = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        count += 1
print()
print('GUI onclick handlers in zip: ' + str(count))

# Verify coal mine onclick in zip
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_coal_mine' in stripped:
        print()
        print('Coal mine onclick in zip:')
        print(stripped)
        break

# Verify scripted GUIs in zip
sfx = z.read('common/scripted_guis/zz_cmpu_scripted_guis.txt').decode('utf-8', errors='replace')
print()
print('Scripted GUIs undefined effects: ' + str(sfx.count('sakuya_b6_build_select_building_effect')))
print('Scripted GUIs set_variable entries: ' + str(sfx.count('set_variable = { name = sakuya_b6_build_sel')))

# Verify script values in zip
sv = z.read('common/script_values/cmpu_feedback_values.txt').decode('utf-8', errors='replace')
print('Script values list init: ' + str('cmpu_fb_marked_states_list = {}' in sv))

z.close()