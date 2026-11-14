#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')

print('=== Verifying onclick handler format ===')
print()

# Check coal_mine onclick
for i, line in enumerate(lines):
    if 'cmpu_select_coal_mine' in line:
        print('Coal mine onclick (first 250 chars):')
        print(line[:250])
        print()
        
        # Check format
        if '); GetScriptedGui' in line:
            print('* Has ; GetScriptedGui - CORRECT')
        else:
            print('* MISSING ; GetScriptedGui - BROKEN')
        
        if 'sakuya_b6_selected_building' in line:
            print('* Has sakuya_b6_selected_building')
        else:
            print('* Missing sakuya_b6_selected_building')
        
        if 'GetVariableSystem.Clear' in line:
            print('* Has GetVariableSystem.Clear (clears industry vars)')
        else:
            print('* Missing GetVariableSystem.Clear')
        break

# Count format status
combined = 0
broken = 0
for line in lines:
    if 'sakuya_b6_selected_building' in line and 'GetScriptedGui' in line:
        if '); GetScriptedGui' in line:
            combined += 1
        else:
            broken += 1

print(f'\n=== Format Summary ===')
print(f'Correct format (with ); GetScriptedGui): {combined}')
print(f'Broken format (missing );): {broken}')
print(f'Total handlers with sakuya_b6_selected_building and GetScriptedGui: {combined + broken}')

# Check script values
with open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\script_values\cmpu_feedback_values.txt', 'r', errors='replace') as f:
    sv_content = f.read()
print(f'\n=== Script Values ===')
print(f'cmpu_fb_marked_states_list = {{}} present: {"cmpu_fb_marked_states_list = {}" in sv_content}')