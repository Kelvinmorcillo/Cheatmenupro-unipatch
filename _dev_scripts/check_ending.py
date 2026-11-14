#!/usr/bin/env python
f = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', errors='replace')
content = f.read()
f.close()

lines = content.split('\n')
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_coal_mine' in stripped:
        print('Full line:')
        print(repr(stripped))
        print()
        print('Last 10 chars: ' + repr(stripped[-10:]))
        print('Ends with ]": ' + str(stripped.endswith(']"]')))
        print('Ends with ]": ' + str(stripped.endswith(']")')))
        break