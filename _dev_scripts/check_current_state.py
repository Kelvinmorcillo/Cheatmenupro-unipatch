#!/usr/bin/env python
f = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', errors='replace')
c = f.read()
f.close()
lines = c.split('\n')

# Find coal mine onclick
for i, line in enumerate(lines):
    if 'cmpu_select_coal_mine' in line and 'onclick' in line.lower():
        print('Current coal mine onclick:')
        print(line)
        print()
        break

# Count onclick with cmpu_select_
count = sum(1 for line in lines if 'onclick' in line.lower() and 'cmpu_select_' in line)
print('Total onclick with cmpu_select_: ' + str(count))

# Check if any onclick has GetVariableSystem.Set for build_sel
set_build_sel = sum(1 for line in lines if 'sakuya_b6_build_sel' in line and 'onclick' in line.lower() and 'Set' in line)
print('Onclick with Set for build_sel: ' + str(set_build_sel))

# Check for clear statements
clear_count = sum(1 for line in lines if 'GetVariableSystem.Clear' in line and 'onclick' in line.lower())
print('Onclick with Clear: ' + str(clear_count))