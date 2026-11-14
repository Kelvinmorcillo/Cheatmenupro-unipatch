#!/usr/bin/env python
import re

with open('C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', encoding='utf-8') as f:
    content = f.read()

# Count onclick patterns with sakuya_b6_selected_building
pattern = r".*sakuya_b6_selected_building.*"
matches = re.findall(pattern, content)
print(f'Total lines with sakuya_b6_selected_building: {len(matches)}')

# Check how many have the combined format (; GetScriptedGui)
combined = 0
separate = 0
for line in content.split('\n'):
    if 'GetVariableSystem.Set' in line and 'sakuya_b6_selected_building' in line:
        if '; GetScriptedGui' in line:
            combined += 1
        else:
            separate += 1

print(f'With combined format (; GetScriptedGui): {combined}')
print(f'With separate format: {separate}')

# Show a few examples of each
print('\n--- Combined format examples ---')
count = 0
for line in content.split('\n'):
    if 'GetVariableSystem.Set' in line and 'sakuya_b6_selected_building' in line and '; GetScriptedGui' in line:
        print(line[:150])
        count += 1
        if count >= 3:
            break

print('\n--- Separate format examples ---')
count = 0
for line in content.split('\n'):
    if 'GetVariableSystem.Set' in line and 'sakuya_b6_selected_building' in line and '; GetScriptedGui' not in line:
        print(line[:150])
        count += 1
        if count >= 3:
            break