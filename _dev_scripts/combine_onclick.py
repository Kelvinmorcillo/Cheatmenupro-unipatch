#!/usr/bin/env python
import re

with open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
fixed = 0
i = 0

while i < len(lines):
    line = lines[i]
    # Check if this line has GetVariableSystem.Set with sakuya_b6_selected_building
    if 'GetVariableSystem.Set' in line and 'sakuya_b6_selected_building' in line:
        # Check if this is the FIRST part of a separate pair (no ; GetScriptedGui in this line)
        if '; GetScriptedGui' not in line:
            # Look ahead for the GetScriptedGui onclick on the next line(s)
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                # Check if next line has GetScriptedGui with cmpu_select
                if '; GetScriptedGui' in next_line and 'cmpu_select_' in next_line:
                    # Extract building name from first line
                    building_match = re.search(r"'([^']+)'\)", line)
                    if building_match:
                        building_name = building_match.group(1)
                        # Extract GUI name from second line
                        gui_match = re.search(r"'cmpu_select_([a-z_]+)'\)", next_line)
                        if gui_match:
                            gui_name = 'cmpu_select_' + gui_match.group(1)
                            # Create combined onclick
                            combined = "onclick = \"[GetVariableSystem.Set('sakuya_b6_selected_building', '" + building_name + "'); GetScriptedGui('" + gui_name + "').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)]\""
                            new_lines.append(combined)
                            fixed += 1
                            i = j + 1  # Skip past the second line
                            break
                j += 1
            else:
                # No matching GetScriptedGui found, keep both lines
                new_lines.append(line)
                new_lines.append(lines[j] if j < len(lines) else '')
                i += 1
                continue
        else:
            # Already combined, keep as-is
            new_lines.append(line)
            i += 1
            continue
    else:
        new_lines.append(line)
        i += 1

with open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print(f'Combined {fixed} onclick handlers')