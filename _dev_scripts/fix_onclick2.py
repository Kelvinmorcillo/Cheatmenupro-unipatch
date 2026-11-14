#!/usr/bin/env python
# Fix: Enhance onclick handlers to clear four industry variables
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
enhanced = 0

for line in lines:
    # Check if this is a combined onclick for a building selection
    # Format: onclick = "[GetVariableSystem.Set('sakuya_b6_selected_building', 'X'); GetScriptedGui('cmpu_select_Y')...]"
    if 'GetVariableSystem.Set' in line and 'sakuya_b6_selected_building' in line:
        # Check if it already has GetScriptedGui (combined format)
        if '; GetScriptedGui' in line:
            # Extract the building name from the first onclick part
            building_match = re.search(r"'([^']+)'\)", line)
            if building_match:
                building_name = building_match.group(1)
                
                # Add variable clearing before GetScriptedGui
                # Insert: ; GetVariableSystem.Clear('sakuya_b6_build_sel_bank');
                #         GetVariableSystem.Clear('sakuya_b6_build_sel_food_service');
                #         GetVariableSystem.Clear('sakuya_b6_build_sel_pharmaceutical_services');
                #         GetVariableSystem.Clear('sakuya_b6_build_sel_software_industry');
                clear_code = " GetVariableSystem.Clear('sakuya_b6_build_sel_bank'); GetVariableSystem.Clear('sakuya_b6_build_sel_food_service'); GetVariableSystem.Clear('sakuya_b6_build_sel_pharmaceutical_services'); GetVariableSystem.Clear('sakuya_b6_build_sel_software_industry')"
                
                # Replace ; GetScriptedGui with the clear code + ; GetScriptedGui
                new_line = line.replace(
                    '); GetScriptedGui',
                    clear_code + '; GetScriptedGui'
                )
                new_lines.append(new_line)
                enhanced += 1
                continue
    
    new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print(f'Enhanced {enhanced} onclick handlers')