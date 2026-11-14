#!/usr/bin/env python
import os, re

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

print("=" * 60)
print("COMPLETE FIX - Starting fresh from backup")
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
# Clear ALL build_sel vars to 0, then set selected to 1, AND set selected_building
# ============================================================
sfx_filepath = os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt')
with open(sfx_filepath, 'r', errors='replace') as f:
    sfx_content = f.read()

sfx_lines = sfx_content.split('\n')
new_sfx_lines = []
sfx_fixed = 0
i = 0

while i < len(sfx_lines):
    line = sfx_lines[i]
    if "cmpu_select_" in line and "= {" in line and "scope = country" in line:
        # This is a cmpu_select_X definition header
        m = re.search(r"(cmpu_select_\w+) = \{", line)
        if m:
            select_name = m.group(1)
            building_name = select_name.replace('cmpu_select_', 'building_')
            build_var = 'sakuya_b6_build_sel_' + building_name.replace('building_', '')
            
            # Collect all lines until we find the closing } of effect
            # We need to find where effect = { starts and ends
            block_lines = [line]
            j = i + 1
            brace_count = 1
            while j < len(sfx_lines) and brace_count > 0:
                block_lines.append(sfx_lines[j])
                brace_count += sfx_lines[j].count('{') - sfx_lines[j].count('}')
                j += 1
            
            # Check if this block already has set_variable for sakuya_b6_build_sel
            block_text = '\n'.join(block_lines)
            if 'sakuya_b6_build_select_building_effect' in block_text:
                # Replace the effect block
                # Find the effect section
                effect_start = block_text.find('effect = {')
                if effect_start >= 0:
                    # Find the closing of effect block within this block
                    # Count braces from effect = {
                    effect_text = block_text[effect_start:]
                    effect_braces = 1
                    effect_end = effect_start + 1
                    while effect_end < len(effect_text) and effect_braces > 0:
                        effect_braces += effect_text[effect_end].count('{') - effect_text[effect_end].count('}')
                        effect_end += 1
                    
                    # Build new effect block
                    new_effect = 'effect = {\n'
                    new_effect += '        cmpu_b6_build_clear_all_selected_effect = yes\n'
                    # Set ALL build_sel vars to 0 first
                    # We need to list all 118 building vars set to 0
                    # But that's too many lines. Instead, just set the selected one to 1
                    # and rely on clear_all_selected_effect to clear others
                    new_effect += '        set_variable = { name = ' + build_var + ' value = 1 }\n'
                    new_effect += '        set_variable = { name = sakuya_b6_selected_building value = ' + building_name + ' }\n'
                    new_effect += '    }\n'
                    
                    # Replace the effect block
                    new_block_text = block_text[:effect_start] + new_effect
                    # Replace the block in lines
                    # Remove old lines and insert new ones
                    block_lines_new = block_text[:effect_start].split('\n') + new_effect.split('\n')
                    # Remove old lines from i to j-1, insert new ones
                    new_sfx_lines = new_sfx_lines[:i] + block_lines_new + new_sfx_lines[j:]
                    i += len(block_lines_new)
                    sfx_fixed += 1
                    continue
    
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
print('  set_variable (build_sel): ' + str(sfx_setvars))
print('  set_variable (selected_building): ' + str(sfx_selected))

# ============================================================
# FIX 3: cmpu_feedback_guis.txt - change checks to read sakuya_b6_selected_building
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
print()
print('How it works:')
print('  1. Click building -> onclick calls cmpu_select_X only')
print('  2. cmpu_select_X clears all build_sel vars, sets sakuya_b6_build_sel_X=1')
print('  3. cmpu_select_X ALSO sets sakuya_b6_selected_building = building_X')
print('  4. Feedback GUI checks variable = sakuya_b6_selected_building value = building_X')
print('  5. Only ONE building matches -> only selected building shows')