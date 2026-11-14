#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

# Find coal_mine onclick
idx = content.find('cmpu_select_coal_mine')
# Print the full onclick line
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'cmpu_select_coal_mine' in line:
        print('Full onclick line:')
        print(line)
        print()
        # Analyze the format
        # Check for Set(
        if "GetVariableSystem.Set" in line:
            print('Contains GetVariableSystem.Set')
        
        # Check for );
        if ');' in line:
            print('Contains );')
        
        # Check for GetScriptedGui
        if 'GetScriptedGui' in line:
            print('Contains GetScriptedGui')
            gp = line.find('GetScriptedGui')
            print('  GetScriptedGui position: ' + str(gp))
            # Show context
            ctx = line[gp-30:gp+80]
            print('  Context: ...' + ctx + '...')
        
        break

# Also check for the four industry clears
print()
print('=== Checking industry clears ===')
for var in ['sakuya_b6_build_sel_bank', 'sakuya_b6_build_sel_food_service', 
            'sakuya_b6_build_sel_pharmaceutical_services', 'sakuya_b6_build_sel_software_industry']:
    if var in content:
        count = content.count(var)
        print('  ' + var + ': ' + str(count) + ' occurrences')