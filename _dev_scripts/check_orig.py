#!/usr/bin/env python
f = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui.orig', 'r', errors='replace')
c = f.read()
f.close()
# Find coal mine onclick
idx = c.find("'building_coal_mine'")
if idx >= 0:
    lines = c.split('\n')
    for i, line in enumerate(lines):
        if "'building_coal_mine'" in line:
            print('ORIGINAL coal mine onclick:')
            print(line)
            break
else:
    print("Not found in orig")
    idx2 = c.find('building_coal_mine')
    if idx2 >= 0:
        lines = c.split('\n')
        for i, line in enumerate(lines):
            if 'building_coal_mine' in line:
                print('ORIGINAL (alt):')
                print(line[:200])
                break