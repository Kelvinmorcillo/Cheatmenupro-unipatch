#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')

print('=== Checking onclick format ===')
print()

# Find lines with sakuya_b6_selected_building
for i, line in enumerate(lines):
    if 'sakuya_b6_selected_building' in line:
        print(f'Line {i}:')
        # Check for the format patterns
        if '); GetScriptedGui' in line:
            print('  [OK] Has ); GetScriptedGui')
        else:
            print('  [MISSING] ; GetScriptedGui')
        
        if 'GetScriptedGui' in line:
            # Find position of GetScriptedGui
            gp = line.find('GetScriptedGui')
            # Check what's before it
            before = line[gp-10:gp]
            print(f'  Before GetScriptedGui: ...{before}...')
        
        print()
        # Only show first 3
        if i >= 2:
            break