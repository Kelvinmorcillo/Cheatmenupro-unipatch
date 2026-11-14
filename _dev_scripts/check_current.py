#!/usr/bin/env python
f = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', errors='replace')
c = f.read()
f.close()
lines = c.split('\n')
# Check coal mine onclick
for i, line in enumerate(lines):
    if 'cmpu_select_coal_mine' in line and 'onclick' in line.lower():
        print('Current coal mine onclick:')
        print(line)
        break
# Check format
count_correct = 0
count_missing = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped and '); GetScriptedGui' in stripped and stripped.endswith(']")'):
        count_correct += 1
    elif stripped.startswith('onclick = "') and 'cmpu_select_' in stripped:
        count_missing += 1
        print('  BROKEN: ' + stripped[:100])
print()
print('Correct onclick format: ' + str(count_correct))
print('Missing/broken format: ' + str(count_missing))