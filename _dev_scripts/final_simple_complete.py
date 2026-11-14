#!/usr/bin/env python
import os, re

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

print("=== FINAL COMPLETE FIX ===")
print()

# ============================================================
# FIX 1: onclick handlers in sakuya_main.gui - ONLY call cmpu_select_X
# ============================================================
gui_filepath = os.path.join(base, 'gui', 'main', 'sakuya_main.gui')
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
            new_stripped = 'onclick = "[GetScriptedGui(\'' + select_name + '\').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"'
            indent = line[:len(line) - len(line.lstrip())]
            new_gui_lines.append(indent + new_stripped)
            gui_fixed += 1
        else:
            new_gui_lines.append(line)
    else:
        new_gui_lines.append(line)

with open(gui_filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_gui_lines))
print('Fix 1: Fixed ' + str(gui_fixed) + ' onclick handlers (call cmpu_select_X only)')

# ============================================================
# FIX 2: cmpu_select_X scripted GUIs - use set_variable
# ============================================================
sfx_filepath = os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt')
with open(sfx_filepath, 'r', errors='replace') as f:
    sfx_content = f.read()

# Simple line-by-line replacement
sfx_lines = sfx_content.split('\n')
new_sfx_lines = []
sfx_fixed = 0
i = 0
while i < len(sfx_lines):
    line = sfx_lines[i]
    if "sakuya_b6_build_select_building_effect = { VAR = " in line:
        # Extract building variable name
        m = re.search(r"VAR = (sakuya_b6_build_sel_\w+)", line)
        if m:
            build_var = m.group(1)
            building_name = build_var.replace('sakuya_b6_build_sel_', 'building_')
            # Replace this line with set_variable for building + selected_building
            indent = line[:len(line) - len(line.lstrip())]
            new_sfx_lines.append(indent + "cmpu_b6_build_clear_all_selected_effect = yes")
            new_sfx_lines.append(indent + "set_variable = { name = " + build_var + " value = 1 }")
            new_sfx_lines.append(indent + "set_variable = { name = sakuya_b6_selected_building value = " + building_name + " }")
            sfx_fixed += 1
        else:
            new_sfx_lines.append(line)
    else:
        new_sfx_lines.append(line)
    i += 1

with open(sfx_filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_sfx_lines))
print('Fix 2: Fixed ' + str(sfx_fixed) + ' cmpu_select_X scripted GUIs')

# Verify sfx fix
with open(sfx_filepath, 'r', errors='replace') as f:
    sfx_check = f.read()
sfx_remaining = sfx_check.count('sakuya_b6_build_select_building_effect')
sfx_setvars = sfx_check.count('set_variable = { name = sakuya_b6_build_sel')
sfx_selected = sfx_check.count('set_variable = { name = sakuya_b6_selected_building')
print('  Remaining undefined effects: ' + str(sfx_remaining))
print('  set_variable (build_sel) entries: ' + str(sfx_setvars))
print('  set_variable (selected_building) entries: ' + str(sfx_selected))

# ============================================================
# FIX 3: cmpu_feedback_guis.txt - change ALL checks to read sakuya_b6_selected_building
# ============================================================
fb_filepath = os.path.join(base, 'common', 'scripted_guis', 'cmpu_feedback_guis.txt')
with open(fb_filepath, 'r', errors='replace') as f:
    fb_content = f.read()

# Simple replacement: has_variable = sakuya_b6_build_sel_XXX -> variable = sakuya_b6_selected_building value = XXX
# We need to extract the building name from the variable name
fb_lines = fb_content.split('\n')
new_fb_lines = []
fb_fixed = 0

for line in fb_lines:
    m = re.search(r"has_variable = (sakuya_b6_build_sel_\w+)", line)
    if m:
        build_var = m.group(1)
        building_name = build_var.replace('sakuya_b6_build_sel_', 'building_')
        new_line = re.sub(r"has_variable = sakuya_b6_build_sel_\w+", "variable = sakuya_b6_selected_building value = " + building_name, line)
        new_fb_lines.append(new_line)
        fb_fixed += 1
    else:
        new_fb_lines.append(line)

with open(fb_filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_fb_lines))
print('Fix 3: Changed ' + str(fb_fixed) + ' feedback GUI checks to read sakuya_b6_selected_building')

# Verify fb fix
with open(fb_filepath, 'r', errors='replace') as f:
    fb_check = f.read()
fb_remaining_has = len(re.findall(r'has_variable = sakuya_b6_build_sel', fb_check))
fb_new_var = len(re.findall(r'variable = sakuya_b6_selected_building value =', fb_check))
print('  Remaining has_variable checks: ' + str(fb_remaining_has))
print('  New variable checks: ' + str(fb_new_var))

# ============================================================
# FIX 4: Verify script values
# ============================================================
sv_filepath = os.path.join(base, 'common', 'script_values', 'cmpu_feedback_values.txt')
with open(sv_filepath, 'r', errors='replace') as f:
    sv_content = f.read()
sv_has_list = 'cmpu_fb_marked_states_list = {}' in sv_content
print('Fix 4: Script values - cmpu_fb_marked_states_list: ' + str(sv_has_list))

print()
print('=== ALL FIXES COMPLETE ===')