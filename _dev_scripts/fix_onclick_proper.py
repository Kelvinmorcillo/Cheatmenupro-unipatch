#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
enhanced = 0

for line in lines:
    # Check if this is a combined onclick for building selection
    # Format: onclick = "[GetVariableSystem.Set('sakuya_b6_selected_building', 'X'); GetScriptedGui('cmpu_select_Y')...]"
    if 'GetVariableSystem.Set' in line and 'sakuya_b6_selected_building' in line and '; GetScriptedGui' in line:
        # Extract building name for verification
        building_match = re.search(r"'([^']+)'\)", line)
        building_name = building_match.group(1) if building_match else 'unknown'
        
        # Replace '); GetScriptedGui' with clear codes + '); GetScriptedGui'
        clear_code = " GetVariableSystem.Clear('sakuya_b6_build_sel_bank'); GetVariableSystem.Clear('sakuya_b6_build_sel_food_service'); GetVariableSystem.Clear('sakuya_b6_build_sel_pharmaceutical_services'); GetVariableSystem.Clear('sakuya_b6_build_sel_software_industry')"
        
        new_line = line.replace(
            '); GetScriptedGui',
            clear_code + '; GetScriptedGui'
        )
        new_lines.append(new_line)
        enhanced += 1
    else:
        new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print(f'Enhanced {enhanced} onclick handlers')