#!/usr/bin/env python
import os

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox_Interactive\Victoria_3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

# Show the key onclick pattern for coal mine
idx = content.find("'building_coal_mine'")
if idx >= 0:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "'building_coal_mine'" in line:
            print('Current onclick format:')
            print(line)
            print()
            if '); GetScriptedGui' in line:
                print('Has ); GetScriptedGui - CORRECT')
            else:
                print('Missing ); GetScriptedGui - BROKEN')
            break
else:
    print("'building_coal_mine' not found - checking alternative...")
    idx2 = content.find('building_coal_mine')
    if idx2 >= 0:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'building_coal_mine' in line:
                print('Current onclick format (alt):')
                print(line)
                break