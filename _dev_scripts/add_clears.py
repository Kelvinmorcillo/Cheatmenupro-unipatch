#!/usr/bin/env python
"""
Add the four industry clear codes to the onclick handlers.

The current format has:
  onclick = "[GetVariableSystem.Set('sakuya_b6_selected_building', 'X'); GetScriptedGui('cmpu_select_X').Execute(...)"

The fix adds after the Set() call:
  GetVariableSystem.Clear('sakuya_b6_build_sel_bank');
  GetVariableSystem.Clear('sakuya_b6_build_sel_food_service');
  GetVariableSystem.Clear('sakuya_b6_build_sel_pharmaceutical_services');
  GetVariableSystem.Clear('sakuya_b6_build_sel_software_industry')
"""

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
fixed = 0

for line in lines:
    # Check if this line has the Set() call but missing the clear codes
    if 'GetVariableSystem.Set' in line and 'sakuya_b6_selected_building' in line and 'GetScriptedGui' in line:
        # Check if the clear codes are already present
        if 'sakuya_b6_build_sel_bank' in line:
            # Clear codes already present, keep as-is
            new_lines.append(line)
        else:
            # Add the clear codes after '); '
            # The pattern is: ...building_X'); GetScriptedGui...
            # We need to insert the clears after '); ' and before 'GetScriptedGui'
            
            # First, ensure '); ' is present
            if '); ' not in line:
                # Add '); ' before GetScriptedGui
                line = line.replace('GetScriptedGui', '); GetScriptedGui')
            
            # Now add the clear codes after '); '
            # Find position of '); GetScriptedGui'
            marker = '); GetScriptedGui'
            if marker in line:
                # Insert the clear codes after '); '
                clears = (" GetVariableSystem.Clear('sakuya_b6_build_sel_bank'); "
                          "GetVariableSystem.Clear('sakuya_b6_build_sel_food_service'); "
                          "GetVariableSystem.Clear('sakuya_b6_build_sel_pharmaceutical_services'); "
                          "GetVariableSystem.Clear('sakuya_b6_build_sel_software_industry')")
                # Insert: '); GetScriptedGui' -> '); ' + clears + ' GetScriptedGui'
                line = line.replace(marker, '); ' + clears + ' GetScriptedGui')
                fixed += 1
            
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_lines))

print('Fixed ' + str(fixed) + ' lines')
print('Total lines: ' + str(len(lines)))