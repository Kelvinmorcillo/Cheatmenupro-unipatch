#!/usr/bin/env python
f = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', errors='replace')
content = f.read()
f.close()

lines = content.split('\n')
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_coal_mine' in stripped:
        last_chars = stripped[-10:]
        print('Last 10 chars (repr):', repr(last_chars))
        print('Last char:', repr(stripped[-1]))
        print('2nd to last:', repr(stripped[-2]))
        print('3rd to last:', repr(stripped[-3]))
        print('4th to last:', repr(stripped[-4]))
        print()
        # Check if there's double ]]
        if stripped[-2] == ']' and stripped[-3] == ']':
            print('HAS DOUBLE ]] before "')
        elif stripped[-2] == ']':
            print('HAS SINGLE ] before "')
        else:
            print('UNEXPECTED ENDING')
        break