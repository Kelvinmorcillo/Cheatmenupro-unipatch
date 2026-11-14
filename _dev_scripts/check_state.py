#!/usr/bin/env python
import os, re

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

# Check GUI onclick
f = open(os.path.join(base, 'gui', 'main', 'sakuya_main.gui'), 'r', errors='replace')
c = f.read()
f.close()
lines = c.split('\n')
coal_onclick = None
count = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetScriptedGui') and 'cmpu_select_' in stripped:
        count += 1
        if 'cmpu_select_coal_mine' in stripped:
            coal_onclick = stripped
print('GUI onclick count: ' + str(count))
if coal_onclick:
    print('Coal mine onclick: ' + coal_onclick[:150])
else:
    print('No coal mine onclick found!')

# Check scripted GUIs
f2 = open(os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt'), 'r', errors='replace')
c2 = f2.read()
f2.close()
print()
print('Scripted GUIs:')
print('  sakuya_b6_build_select_remaining: ' + str(c2.count('sakuya_b6_build_select_building_effect')))
print('  set_variable build_sel: ' + str(c2.count('set_variable = { name = sakuya_b6_build_sel')))
print('  set_variable selected_building: ' + str(c2.count('set_variable = { name = sakuya_b6_selected_building')))

# Show coal mine select
lines2 = c2.split('\n')
for i, line in enumerate(lines2):
    if 'cmpu_select_coal_mine' in line:
        for j in range(i, min(i+8, len(lines2))):
            print(lines2[j])
        break

# Check feedback GUI
f3 = open(os.path.join(base, 'common', 'scripted_guis', 'cmpu_feedback_guis.txt'), 'r', errors='replace')
c3 = f3.read()
f3.close()
print()
print('Feedback GUI:')
print('  has_variable remaining: ' + str(c3.count('has_variable = sakuya_b6_build_sel')))
print('  variable = sakuya_b6_selected_building: ' + str(c3.count('variable = sakuya_b6_selected_building value =')))

# Check script values
f4 = open(os.path.join(base, 'common', 'script_values', 'cmpu_feedback_values.txt'), 'r', errors='replace')
c4 = f4.read()
f4.close()
print()
print('Script values - list init: ' + str('cmpu_fb_marked_states_list = {}' in c4))