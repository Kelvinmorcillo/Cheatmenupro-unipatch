#!/usr/bin/env python
f = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', errors='replace')
content = f.read()
f.close()

lines = content.split('\n')
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_coal_mine' in stripped:
        print('Coal mine onclick (repr):')
        print(repr(stripped))
        print()
        print('Last 5 chars:', repr(stripped[-5:]))
        print('Last char:', repr(stripped[-1]))
        print('2nd to last:', repr(stripped[-2]))
        print('3rd to last:', repr(stripped[-3]))
        print('4th to last:', repr(stripped[-4]))
        break