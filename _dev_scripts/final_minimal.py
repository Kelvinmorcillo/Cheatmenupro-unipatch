#!/usr/bin/env python
import re

# Fix 1: onclick handlers in sakuya_main.gui
filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
fixed = 0
for line in lines:
    if 'onclick' in line.lower() and 'sakuya_b6_selected_building' in line:
        match = re.search(r"GetVariableSystem\.Set\('sakuya_b6_selected_building',\s*'([^']+)'", line)
        if match:
            building_var = match.group(1)
            select_name = 'cmpu_select_' + building_var.replace('building_', '')
            new_line = 'onclick = "GetScriptedGui(\'' + select_name + '\').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)"'
            new_lines.append(new_line)
            fixed += 1
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_lines))
print('Fix 1: Fixed ' + str(fixed) + ' onclick handlers')

# Fix 2: cmpu_select_X scripted GUIs - replace undefined effect with set_variable
filepath2 = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\scripted_guis\zz_cmpu_scripted_guis.txt'
with open(filepath2, 'r', errors='replace') as f:
    content2 = f.read()

pattern = r"sakuya_b6_build_select_building_effect = \{ VAR = (sakuya_b6_build_sel_\w+) \}"
replacement = r"set_variable = { name = \1 value = 1 }"

new_content2 = re.sub(pattern, replacement, content2)
count = len(re.findall(pattern, content2))

with open(filepath2, 'w', errors='replace') as f:
    f.write(new_content2)
print('Fix 2: Replaced ' + str(count) + ' occurrences of undefined effect')
print()
print('DONE - both files fixed')