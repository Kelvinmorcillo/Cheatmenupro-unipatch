#!/usr/bin/env python
f = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', errors='replace')
c = f.read()
f.close()
lines = c.split('\n')
count = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        count += 1
        if count <= 3:
            print(str(count) + ': ' + stripped[:120])
print('Total correct: ' + str(count))

# Also check for simple onclick format
count2 = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetScriptedGui') and 'cmpu_select_' in stripped:
        count2 += 1
print('Total simple onclick: ' + str(count2))