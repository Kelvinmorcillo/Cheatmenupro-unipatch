#!/usr/bin/env python
"""
FINAL FIX - Focused ONLY on making the feedback GUI reflect the selected building.

The problem: onclick handlers were adding GetVariableSystem.Set/Clear calls that
don't work properly in onclick context. The cmpu_select_X scripted GUIs already
do everything needed (clear all + set specific building variable).

The fix: Make each onclick handler ONLY call GetScriptedGui('cmpu_select_X').Execute(...)
This lets cmpu_select_X handle: clear all selection vars + set the selected building var.
The feedback panel then reads has_variable = sakuya_b6_build_sel_X and shows that building.
"""

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
fixed = 0

for line in lines:
    # Check if this line has an onclick with sakuya_b6_selected_building
    if 'sakuya_b6_selected_building' in line and 'onclick' in line:
        # Extract the building name from the Set() call
        # Pattern: GetVariableSystem.Set('sakuya_b6_selected_building', 'building_X')
        import re
        match = re.search(r"GetVariableSystem\.Set\('sakuya_b6_selected_building',\s*'([^']+)'\)", line)
        if match:
            building_var = match.group(1)  # e.g., 'building_coal_mine'
            # Derive the cmpu_select name: building_coal_mine -> cmpu_select_coal_mine
            select_name = 'cmpu_select_' + building_var.replace('building_', '')
            # Replace the entire onclick with just the GetScriptedGui call
            new_onclick = 'onclick = "GetScriptedGui(\'' + select_name + '\').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)"'
            new_lines.append(new_onclick)
            fixed += 1
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_lines))

print('Fixed ' + str(fixed) + ' onclick handlers')
print('Total lines: ' + str(len(lines)))