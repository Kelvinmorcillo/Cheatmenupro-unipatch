import re

filepath = 'C:\\Users\\kelvi\\OneDrive\\Documents\\Paradox Interactive\\Victoria 3\\mod\\cmp_unipolar_patch_v2\\gui\\main\\sakuya_main.gui'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    # Check if this line has the GetVariableSystem.Set pattern for selected building
    vs_match = re.search(r"onclick = \"\[GetVariableSystem\.Set\('sakuya_b6_selected_building', '([^']+)'\)\]\"", line)
    if vs_match:
        building_name = vs_match.group(1)
        # Look ahead for the GetScriptedGui onclick
        j = i + 1
        while j < len(lines):
            next_line = lines[j]
            gs_match = re.search(r"onclick = \"\[GetScriptedGui\('cmpu_select_([a-z_]+)'\)\.Execute\(GuiScope\.SetRoot\(GetPlayer\.MakeScope\)\.End\)\]\"", next_line)
            if gs_match:
                gui_name = 'cmpu_select_' + gs_match.group(1)
                # Combine both onto one onclick
                combined = f"onclick = \"[GetVariableSystem.Set('sakuya_b6_selected_building', '{building_name}'); GetScriptedGui('{gui_name}').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)]\""
                new_lines.append(combined)
                i = j + 1  # Skip past the second onclick
                break
            else:
                new_lines.append(next_line)
                i = j + 1
                break
        else:
            new_lines.append(line)
            i += 1
    else:
        new_lines.append(line)
        i += 1

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print('Done fixing double onclick patterns')