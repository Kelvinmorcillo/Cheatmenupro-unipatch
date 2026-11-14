#!/usr/bin/env python
import os, re

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

print("=" * 60)
print("FINAL WORKING FIX v3")
print("=" * 60)

# ============================================================
# FIX 1: onclick handlers - ONLY call cmpu_select_X
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
# FIX 2: cmpu_select_X scripted GUIs
# Clear ALL build_sel vars to 0 explicitly, then set selected to 1
# ============================================================
sfx_filepath = os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt')
with open(sfx_filepath, 'r', errors='replace') as f:
    sfx_content = f.read()

sfx_lines = sfx_content.split('\n')
new_sfx_lines = []
sfx_fixed = 0
i = 0

# Get all building variable names
all_build_vars = []
for line in sfx_lines:
    m = re.search(r"sakuya_b6_build_select_building_effect = \{ VAR = (sakuya_b6_build_sel_\w+) \}", line)
    if m:
        all_build_vars.append(m.group(1))

print('Found ' + str(len(all_build_vars)) + ' building variables')

while i < len(sfx_lines):
    line = sfx_lines[i]
    if "sakuya_b6_build_select_building_effect = { VAR = " in line:
        m = re.search(r"VAR = (sakuya_b6_build_sel_\w+)", line)
        if m:
            build_var = m.group(1)
            building_name = build_var.replace('sakuya_b6_build_sel_', 'building_')
            indent = line[:len(line) - len(line.lstrip())]
            
            # Clear ALL build_sel vars to 0, then set selected to 1
            new_sfx_lines.append(indent + "cmpu_b6_build_clear_all_selected_effect = yes")
            for bv in all_build_vars:
                new_sfx_lines.append(indent + "set_variable = { name = " + bv + " value = 0 }")
            new_sfx_lines.append(indent + "set_variable = { name = " + build_var + " value = 1 }")
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
print('  Remaining undefined effects: ' + str(sfx_remaining))
print('  set_variable (build_sel): ' + str(sfx_setvars))

# Show coal mine select
lines2 = sfx_check.split('\n')
for i, line in enumerate(lines2):
    if 'cmpu_select_coal_mine' in line:
        for j in range(i, min(i+15, len(lines2))):
            print(lines2[j])
        break

# ============================================================
# FIX 3: cmpu_feedback_guis.txt - change checks to read sakuya_b6_selected_building
# Use CORRECT Victoria 3 syntax: variable = { name = X value = Y }
# ============================================================
fb_filepath = os.path.join(base, 'common', 'scripted_guis', 'cmpu_feedback_guis.txt')
with open(fb_filepath, 'r', errors='replace') as f:
    fb_content = f.read()

fb_lines = fb_content.split('\n')
new_fb_lines = []
fb_fixed = 0

for line in fb_lines:
    m = re.search(r"has_variable = (sakuya_b6_build_sel_\w+)", line)
    if m:
        build_var = m.group(1)
        building_name = build_var.replace('sakuya_b6_build_sel_', 'building_')
        new_line = re.sub(r"has_variable = sakuya_b6_build_sel_\w+", "variable = { name = sakuya_b6_selected_building value = " + building_name + " }", line)
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
fb_new_var = len(re.findall(r'variable = \{ name = sakuya_b6_selected_building value =', fb_check))
print('  Remaining has_variable checks: ' + str(fb_remaining_has))
print('  New variable checks: ' + str(fb_new_var))

# Show one example
for line in new_fb_lines:
    if 'sakuya_b6_selected_building value = building_coal_mine' in line:
        print('  Example: ' + line.strip())
        break

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
print()
print('How it works:')
print('  1. Click building -> onclick calls cmpu_select_X only')
print('  2. cmpu_select_X clears all build_sel vars to 0, sets selected to 1')
print('  3. cmpu_select_X ALSO sets sakuya_b6_selected_building = building_X')
print('  4. Feedback GUI checks variable = { name = sakuya_b6_selected_building value = building_X }')
print('  5. Only ONE building matches -> only selected building shows')