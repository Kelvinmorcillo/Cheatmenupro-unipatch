#!/usr/bin/env python
import re

# ============================================================
# FINAL APPROACH - Modify feedback GUI to read selected building
# directly from sakuya_b6_selected_building variable
# ============================================================

# ---- Fix 1: onclick handlers - properly set sakuya_b6_selected_building ----
gui_filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(gui_filepath, 'r', errors='replace') as f:
    gui_content = f.read()

gui_lines = gui_content.split('\n')
new_gui_lines = []
gui_fixed = 0

for line in gui_lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        m = re.search(r"GetVariableSystem\.Set\('sakuya_b6_selected_building',\s*'([^']+)'", stripped)
        if m:
            building_name = m.group(1)
            select_name = 'cmpu_select_' + building_name.replace('building_', '')
            # Clean onclick: Set building var + run cmpu_select_X
            new_stripped = 'onclick = "[GetVariableSystem.Set(\'sakuya_b6_selected_building\', \'' + building_name + '\'); GetScriptedGui(\'' + select_name + '\').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"'
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

# ---- Fix 2: Modify cmpu_fb_sel_X_check to check sakuya_b6_selected_building ----
sfx_filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\scripted_guis\cmpu_feedback_guis.txt'
with open(sfx_filepath, 'r', errors='replace') as f:
    sfx_content = f.read()

# Replace: cmpu_fb_sel_X_check = { scope = country is_shown = { has_variable = sakuya_b6_build_sel_X } ... }
# With:    cmpu_fb_sel_X_check = { scope = country is_shown = { variable = sakuya_b6_selected_building value = building_X } ... }

# Pattern: cmpu_fb_sel_XXX_check = { scope = country is_shown = { has_variable = sakuya_b6_build_sel_XXX } is_valid = { always = yes } ai_is_valid = { always = no } effect = { } }
pattern = r"(cmpu_fb_sel_(\w+)_check = \{ scope = country is_shown = \{ )has_variable = sakuya_b6_build_sel_\2( \} is_valid = \{ always = yes \} ai_is_valid = \{ always = no \} effect = \{ \} \})"

def replace_check(m):
    prefix = m.group(1)
    building_var = m.group(2)
    suffix = m.group(3)
    return prefix + "variable = sakuya_b6_selected_building value = " + building_var + suffix

new_sfx_content = re.sub(pattern, replace_check, sfx_content)
sfx_count = len(re.findall(pattern, sfx_content))

with open(sfx_filepath, 'w', errors='replace') as f:
    f.write(new_sfx_content)
print('Feedback GUI: Changed ' + str(sfx_count) + ' selection checks to read sakuya_b6_selected_building')

# Verify
sfx_remaining_has = len(re.findall(r'has_variable = sakuya_b6_build_sel', new_sfx_content))
sfx_new_var = len(re.findall(r'variable = sakuya_b6_selected_building value =', new_sfx_content))
print('Feedback GUI - Remaining has_variable checks: ' + str(sfx_remaining_has))
print('Feedback GUI - New variable checks: ' + str(sfx_new_var))

# ---- Fix 3: Also fix cmpu_select_X scripted GUIs (as backup) ----
sfx2_filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\scripted_guis\zz_cmpu_scripted_guis.txt'
with open(sfx2_filepath, 'r', errors='replace') as f:
    sfx2_content = f.read()

pattern2 = r"sakuya_b6_build_select_building_effect = \{ VAR = (sakuya_b6_build_sel_\w+) \}"
replacement2 = r"set_variable = { name = \1 value = 1 }"

new_sfx2_content = re.sub(pattern2, replacement2, sfx2_content)
sfx2_count = len(re.findall(pattern2, sfx2_content))

with open(sfx2_filepath, 'w', errors='replace') as f:
    f.write(new_sfx2_content)
print('Scripted GUIs: Replaced ' + str(sfx2_count) + ' undefined effects with set_variable')

# ---- Verify script values ----
sv_filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\script_values\cmpu_feedback_values.txt'
with open(sv_filepath, 'r', errors='replace') as f:
    sv_content = f.read()
sv_has_list = 'cmpu_fb_marked_states_list = {}' in sv_content
print('Script Values - cmpu_fb_marked_states_list: ' + str(sv_has_list))

print()
print('=== ALL FIXES COMPLETE ===')
print()
print('Summary:')
print('  1. Onclick handlers set sakuya_b6_selected_building directly')
print('  2. Feedback GUI checks read sakuya_b6_selected_building (not sakuya_b6_build_sel_X)')
print('  3. cmpu_select_X uses set_variable instead of undefined effect')
print('  4. cmpu_fb_marked_states_list = {} present')