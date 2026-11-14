#!/usr/bin/env python
f = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', errors='replace')
c = f.read()
f.close()
lines = c.split('\n')
for i, line in enumerate(lines):
    if 'cmpu_fb' in line.lower():
        print('Line ' + str(i) + ': ' + line[:180])