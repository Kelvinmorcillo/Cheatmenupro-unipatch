#!/usr/bin/env python
import zipfile

z = zipfile.ZipFile(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\clean_fix_final.zip', 'r')
content = z.read('gui/main/sakuya_main.gui').decode('utf-8', errors='replace')
lines = content.split('\n')
# Check coal mine onclick
for i, line in enumerate(lines):
    if 'cmpu_select_coal_mine' in line and 'onclick' in line.lower():
        print('Coal mine onclick:')
        print(line)
        break
# Count
count = sum(1 for line in lines if 'onclick' in line.lower() and 'cmpu_select_' in line and line.strip().startswith('onclick = "[GetVariableSystem.Set') and '); GetScriptedGui' in line and line.strip().endswith(']")'))
print()
print('Correct onclick format: ' + str(count) + ' / 118')
z.close()