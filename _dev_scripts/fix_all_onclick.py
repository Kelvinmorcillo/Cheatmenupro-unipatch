#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
fixed = 0

for line in lines:
    stripped = line.strip()
    # Check if this line is an onclick with cmpu_select_ but missing Set(
    if stripped.startswith('onclick = "') and 'cmpu_select_' in stripped:
        # Check if already correct: has Set( before GetScriptedGui
        if 'GetVariableSystem.Set' in stripped and 'sakuya_b6_selected_building' in stripped:
            new_lines.append(line)  # Already correct
        else:
            # Need to fix: extract building name and rebuild onclick
            bn_match = re.search(r"cmpu_select_([^']+)", stripped)
            if bn_match:
                select_name = 'cmpu_select_' + bn_match.group(1)
                building_name = 'building_' + bn_match.group(1)
                indent = line[:len(line) - len(line.lstrip())]
                # Build new onclick line from scratch
                new_line = indent + 'onclick = "[GetVariableSystem.Set(\'sakuya_b6_selected_building\', \'' + building_name + '\'); GetScriptedGui(\'' + select_name + '\').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"'
                new_lines.append(new_line)
                fixed += 1
            else:
                new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_lines))
print('Fixed ' + str(fixed) + ' onclick handlers')

# Final verification
count_correct = 0
count_missing = 0
for line in new_lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped and '); GetScriptedGui' in stripped:
        count_correct += 1
    elif stripped.startswith('onclick = "') and 'cmpu_select_' in stripped:
        count_missing += 1
        print('  STILL MISSING: ' + stripped[:100])
print('Correct format: ' + str(count_correct))
print('Still missing: ' + str(count_missing))
print()
print('DONE')