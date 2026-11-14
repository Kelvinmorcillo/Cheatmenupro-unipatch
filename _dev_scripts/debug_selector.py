#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')

print('=== Debugging selector onclick handlers ===')
print()

# Find all onclick lines with sakuya_b6_selected_building
for i, line in enumerate(lines):
    if 'sakuya_b6_selected_building' in line and 'onclick' in line:
        print(f'Line {i}:')
        print(f'  {line[:250]}')
        print()
        if '); GetScriptedGui' in line:
            print('  [OK] Has ; GetScriptedGui')
        else:
            print('  [MISSING] ; GetScriptedGui')
        break

# Check for the confirm/close pattern
print('=== Checking for confirm/close patterns ===')
for term in ['confirm', 'close', 'accept', 'end', 'scope']:
    count = content.count(term)
    print(f'  "{term}": {count} occurrences')

# Check for GetPlayer.MakeScope
count = content.count('GetPlayer.MakeScope')
print(f'  "GetPlayer.MakeScope": {count} occurrences')

# Check for GuiScope.SetRoot
count = content.count('GuiScope.SetRoot')
print(f'  "GuiScope.SetRoot": {count} occurrences')