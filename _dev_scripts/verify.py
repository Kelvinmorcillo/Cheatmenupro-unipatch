#!/usr/bin/env python
import os

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

# Check the coal_mine onclick
idx = content.find("'building_coal_mine'")
lines = content.split('\n')
for i, line in enumerate(lines):
    if "'building_coal_mine'" in line:
        print('Coal mine onclick:')
        print(line)
        break

# Check format
if '); GetScriptedGui' in content:
    print('\\nHas ); GetScriptedGui - CORRECT')
else:
    print('\\nMissing ); GetScriptedGui - BROKEN')

# Check industry clears
for var in ['sakuya_b6_build_sel_bank', 'sakuya_b6_build_sel_food_service', 
            'sakuya_b6_build_sel_pharmaceutical_services', 'sakuya_b6_build_sel_software_industry']:
    count = content.count(var)
    print(var + ': ' + str(count) + ' occurrences')

# Check script values
with open(r'C:\Users\kelvi\OneDrive\Documents\Paradox_Interactive\Victoria_3\mod\cmp_unipolar_patch_v2\common\script_values\cmpu_feedback_values.txt', 'r', errors='replace') as f:
    sv = f.read()
print('cmpu_fb_marked_states_list present: ' + str('cmpu_fb_marked_states_list = {}' in sv))