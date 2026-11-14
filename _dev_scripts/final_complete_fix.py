#!/usr/bin/env python
import re, os

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

print("=== FINAL COMPLETE FIX ===")
print()

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
# FIX 2: cmpu_select_X scripted GUIs - use set_variable + set selected_building
# ============================================================
sfx_filepath = os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt')
with open(sfx_filepath, 'r', errors='replace') as f:
    sfx_content = f.read()

# Replace: sakuya_b6_build_select_building_effect = { VAR = sakuya_b6_build_sel_X }
# With:    set_variable = { name = sakuya_b6_build_sel_X value = 1 }
# AND add: set_variable = { name = sakuya_b6_selected_building value = building_X }

pattern = r"(cmpu_select_(\w+) = \{\s*scope = country\n\s*is_shown = \{ is_player = yes \}\n\s*is_valid = \{ always = yes \}\n\s*ai_is_valid = \{ always = no \}\n\s*effect = \{\n\s*)cmpu_b6_build_clear_all_selected_effect = yes\n\s*)sakuya_b6_build_select_building_effect = \{ VAR = (sakuya_b6_build_sel_\w+) \}(\s*\})"

def replace_select(m):
    prefix = m.group(1)
    select_name = m.group(2)
    build_var = m.group(3)
    building_name = build_var.replace('sakuya_b6_build_sel_', 'building_')
    suffix = m.group(4)
    return (prefix + 'cmpu_b6_build_clear_all_selected_effect = yes\n'
            '        set_variable = { name = ' + build_var + ' value = 1 }\n'
            '        set_variable = { name = sakuya_b6_selected_building value = ' + building_name + ' }\n'
            + suffix)

new_sfx_content = re.sub(pattern, replace_select, sfx_content)
sfx_count = len(re.findall(pattern, sfx_content))

with open(sfx_filepath, 'w', errors='replace') as f:
    f.write(new_sfx_content)
print('Fix 2: Fixed ' + str(sfx_count) + ' cmpu_select_X scripted GUIs')

# Verify sfx fix
sfx_remaining = new_sfx_content.count('sakuya_b6_build_select_building_effect')
sfx_setvars = new_sfx_content.count('set_variable = { name = sakuya_b6_build_sel')
sfx_selected = new_sfx_content.count('set_variable = { name = sakuya_b6_selected_building')
print('  Remaining undefined effects: ' + str(sfx_remaining))
print('  set_variable (build_sel) entries: ' + str(sfx_setvars))
print('  set_variable (selected_building) entries: ' + str(sfx_selected))

# ============================================================
# FIX 3: cmpu_feedback_guis.txt - change ALL checks to read sakuya_b6_selected_building
# ============================================================
fb_filepath = os.path.join(base, 'common', 'scripted_guis', 'cmpu_feedback_guis.txt')
with open(fb_filepath, 'r', errors='replace') as f:
    fb_content = f.read()

# Replace ALL has_variable = sakuya_b6_build_sel_X with variable = sakuya_b6_selected_building value = building_X
# Pattern: cmpu_fb_sel_XXX_check = { ... is_shown = { has_variable = sakuya_b6_build_sel_XXX } ... }
fb_pattern = r"(cmpu_fb_sel_(\w+)_check = \{[^}]*is_shown = \{ )has_variable = sakuya_b6_build_sel_\2( \})"

def replace_fb_check(m):
    prefix = m.group(1)
    building_var = m.group(2)
    suffix = m.group(3)
    return prefix + "variable = sakuya_b6_selected_building value = " + building_var + suffix

new_fb_content = re.sub(fb_pattern, replace_fb_check, fb_content)
fb_count = len(re.findall(fb_pattern, fb_content))

with open(fb_filepath, 'w', errors='replace') as f:
    f.write(new_fb_content)
print('Fix 3: Changed ' + str(fb_count) + ' feedback GUI checks to read sakuya_b6_selected_building')

# Verify fb fix
fb_remaining_has = len(re.findall(r'has_variable = sakuya_b6_build_sel', new_fb_content))
fb_new_var = len(re.findall(r'variable = sakuya_b6_selected_building value =', new_fb_content))
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
print()
print('Summary:')
print('  1. Onclick handlers call cmpu_select_X only (clean, simple)')
print('  2. cmpu_select_X clears all build_sel vars + sets sakuya_b6_build_sel_X = 1 + sets sakuya_b6_selected_building')
print('  3. Feedback GUI reads sakuya_b6_selected_building (not sakuya_b6_build_sel_X)')
print('  4. cmpu_fb_marked_states_list = {} present')