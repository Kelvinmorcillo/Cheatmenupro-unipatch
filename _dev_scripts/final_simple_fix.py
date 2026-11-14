#!/usr/bin/env python
import re

# ============================================================
# FINAL SIMPLE FIX
# Restore from backup was already done.
# Fix: onclick handlers directly set sakuya_b6_build_sel_X + sakuya_b6_selected_building
# Fix: cmpu_select_X uses set_variable instead of undefined effect
# ============================================================

# ---- Fix 1: onclick handlers ----
gui_filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(gui_filepath, 'r', errors='replace') as f:
    gui_content = f.read()

gui_lines = gui_content.split('\n')
new_gui_lines = []
gui_fixed = 0

# The four industry variables to clear on every click
industry_vars = [
    'sakuya_b6_build_sel_bank',
    'sakuya_b6_build_sel_food_service',
    'sakuya_b6_build_sel_pharmaceutical_services',
    'sakuya_b6_build_sel_software_industry',
]

for line in gui_lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        m = re.search(r"GetVariableSystem\.Set\('sakuya_b6_selected_building',\s*'([^']+)'", stripped)
        if m:
            building_name = m.group(1)  # e.g., 'building_coal_mine'
            select_name = 'cmpu_select_' + building_name.replace('building_', '')
            build_sel_var = 'sakuya_b6_build_sel_' + building_name.replace('building_', '')
            
            # Clear all four industry variables
            clear_stmts = ''
            for iv in industry_vars:
                clear_stmts += "GetVariableSystem.Clear('" + iv + "'); "
            
            # Set the specific building variable + selected_building variable
            set_stmts = "GetVariableSystem.Set('" + build_sel_var + "', 1); GetVariableSystem.Set('sakuya_b6_selected_building', '" + building_name + "'); "
            
            new_stripped = 'onclick = "[GetVariableSystem.Set(\'sakuya_b6_selected_building\', \'' + building_name + '\'); ' + clear_stmts + set_stmts + 'GetScriptedGui(\'' + select_name + '\').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"'
            
            indent = line[:len(line) - len(line.lstrip())]
            new_gui_lines.append(indent + new_stripped)
            gui_fixed += 1
        else:
            new_gui_lines.append(line)
    else:
        new_gui_lines.append(line)

with open(gui_filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_gui_lines))
print('GUI: Fixed ' + str(gui_fixed) + ' onclick handlers')

# Verify GUI fix
gui_lines2 = new_gui_lines
gui_correct = 0
gui_wrong = 0
for line in gui_lines2:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        if len(stripped) >= 2 and stripped[-2] == ']' and stripped[-1] == '"':
            if len(stripped) >= 3 and stripped[-3] != ']':
                gui_correct += 1
            else:
                gui_wrong += 1
                print('  GUI WRONG (double ]): ' + stripped[:80])
        else:
            gui_wrong += 1
            print('  GUI WRONG (bad end): ' + stripped[:80] + ' ... last: ' + repr(stripped[-5:]))
print('GUI Correct: ' + str(gui_correct) + ', Wrong: ' + str(gui_wrong))

# ---- Fix 2: cmpu_select_X in zz_cmpu_scripted_guis.txt ----
sfx_filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\scripted_guis\zz_cmpu_scripted_guis.txt'
with open(sfx_filepath, 'r', errors='replace') as f:
    sfx_content = f.read()

pattern = r"sakuya_b6_build_select_building_effect = \{ VAR = (sakuya_b6_build_sel_\w+) \}"
replacement = r"set_variable = { name = \1 value = 1 }"

new_sfx_content = re.sub(pattern, replacement, sfx_content)
sfx_count = len(re.findall(pattern, sfx_content))

with open(sfx_filepath, 'w', errors='replace') as f:
    f.write(new_sfx_content)
print('Scripted GUIs: Replaced ' + str(sfx_count) + ' undefined effects with set_variable')

sfx_remaining = new_sfx_content.count('sakuya_b6_build_select_building_effect')
sfx_setvars = new_sfx_content.count('set_variable = { name = sakuya_b6_build_sel')
print('Scripted GUIs Remaining undefined: ' + str(sfx_remaining))
print('Scripted GUIs set_variable entries: ' + str(sfx_setvars))

# ---- Verify script values ----
sv_filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\script_values\cmpu_feedback_values.txt'
with open(sv_filepath, 'r', errors='replace') as f:
    sv_content = f.read()
sv_has_list = 'cmpu_fb_marked_states_list = {}' in sv_content
print('Script Values - cmpu_fb_marked_states_list: ' + str(sv_has_list))

print()
print('=== ALL FIXES COMPLETE ===')