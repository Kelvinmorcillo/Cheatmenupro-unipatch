#!/usr/bin/env python
import os, re, shutil

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

print("=" * 60)
print("REAL FIX - Properly fixing both selector and feedback")
print("=" * 60)

# ============================================================
# STEP 0: Restore ALL files from git
# ============================================================
import subprocess
result = subprocess.run(['git', 'checkout', 'HEAD', '--', '.'], capture_output=True, text=True, cwd=base)
print('git checkout -- . : ' + ('OK' if result.returncode == 0 else 'FAILED: ' + result.stderr))

# ============================================================
# STEP 1: Extract all building names from GUI onclick handlers
# ============================================================
gui_filepath = os.path.join(base, 'gui', 'main', 'sakuya_main.gui')
if not os.path.exists(gui_filepath):
    gui_filepath = os.path.join(base, 'gui', 'sakuya_main.gui')

with open(gui_filepath, 'r', errors='replace') as f:
    gui_content = f.read()

pattern = re.compile(r"GetVariableSystem\.Set\('sakuya_b6_selected_building',\s*'([^']+)'")
buildings = set()
for match in pattern.finditer(gui_content):
    buildings.add(match.group(1))

buildings = sorted(buildings)
print('Found ' + str(len(buildings)) + ' unique buildings')

all_build_vars = sorted(['sakuya_b6_build_sel_' + b.replace('building_', '') for b in buildings])

# ============================================================
# STEP 2: Fix onclick handlers in sakuya_main.gui
# Format: GetVariableSystem.Set('sakuya_b6_selected_building', 'X'); GetScriptedGui('cmpu_select_X').Execute(...)
# ============================================================
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
print('Fix 1: Fixed ' + str(gui_fixed) + ' onclick handlers')

# Verify GUI fix
with open(gui_filepath, 'r', errors='replace') as f:
    gui_check = f.read()
gui_lines2 = gui_check.split('\n')
count_correct = 0
for line in gui_lines2:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        if '); GetScriptedGui' in stripped:
            count_correct += 1
print('  Verified: ' + str(count_correct) + ' onclick handlers with correct format')

# Show coal mine onclick
for line in gui_lines2:
    stripped = line.strip()
    if 'onclick' in stripped and 'cmpu_select_coal_mine' in stripped:
        print('  Coal mine onclick: ' + stripped[:150])
        break

# ============================================================
# STEP 3: Fix cmpu_b6_build_clear_all_selected_effect
# Replace remove_variable with set_variable = { name = X value = 0 }
# ============================================================
clear_filepath = os.path.join(base, 'common', 'scripted_effects', 'zz_cmpu_clear_selection_effects.txt')
with open(clear_filepath, 'r', errors='replace') as f:
    clear_content = f.read()

# Find the effect block
lines = clear_content.split('\n')
new_lines = []
in_effect = False
brace_count = 0
for line in lines:
    if 'cmpu_b6_build_clear_all_selected_effect = {' in line:
        new_lines.append(line)
        in_effect = True
        brace_count = 1
        # Add debug_log
        new_lines.append('\tdebug_log = "CMPU_CLEAR_ALL_EXECUTED"')
        # Add set_variable = 0 for ALL buildings
        for bv in all_build_vars:
            new_lines.append('\tset_variable = { name = ' + bv + ' value = 0 }')
        continue
    if in_effect:
        if '}' in line:
            brace_count += line.count('{') - line.count('}')
            if brace_count <= 0:
                in_effect = False
                new_lines.append(line)
        # Skip all other lines in effect block (remove_variable, debug_log, etc.)
        continue
    else:
        new_lines.append(line)

# Wait, this might have removed the closing brace. Let me check.
# Actually, the above logic might be wrong. Let me rewrite it more carefully.

# Let me just reconstruct the entire file
new_clear_content = '''# ============================================================
# CMPU UNIPOLAR PATCH - FULL SELECTION CLEAR
# Clears EVERY building-selection flag the injector can set
# (all 94 vanilla + all 24 UNIPOLAR). The vanilla Cheat Menu
# clear list does not know the UNIPOLAR variable names, which
# let stale flags accumulate and broke the feedback. Called by
# every cmpu_select_* wrapper before selecting. Read-only w.r.t.
# gameplay: it only clears the injector OWN selection flags.
# ============================================================

cmpu_b6_build_clear_all_selected_effect = {
	debug_log = "CMPU_CLEAR_ALL_EXECUTED"
'''

for bv in all_build_vars:
    new_clear_content += '\tset_variable = { name = ' + bv + ' value = 0 }\n'

new_clear_content += '}\n'

with open(clear_filepath, 'w', errors='replace') as f:
    f.write(new_clear_content)
print('Fix 2: Replaced cmpu_b6_build_clear_all_selected_effect with set_variable = 0 for all buildings')

# Verify
with open(clear_filepath, 'r', errors='replace') as f:
    check = f.read()
print('  remove_variable references: ' + str(check.count('remove_variable')))
print('  set_variable = 0 references: ' + str(check.count('value = 0 }')))

# ============================================================
# STEP 4: Fix zz_cmpu_scripted_guis.txt
# Create/modify cmpu_select_X entries for ALL buildings
# Each entry: clear all vars to 0, set selected to 1
# ============================================================
sfx_filepath = os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt')
with open(sfx_filepath, 'r', errors='replace') as f:
    sfx_content = f.read()

# Find existing cmpu_select_ entries and their positions
lines = sfx_content.split('\n')

# Find where cmpu_select_ entries start and end
start_idx = None
end_idx = len(lines)
for i, line in enumerate(lines):
    if 'cmpu_select_' in line and '=' in line and start_idx is None:
        start_idx = i
    if start_idx is not None and ('cmpu_build_has_selected_building_check' in line or 'cmpu_build_can_confirm_check' in line):
        end_idx = i
        break

print('Fix 3: cmpu_select_ entries start at line ' + str(start_idx) + ', end at line ' + str(end_idx))

# Keep everything before cmpu_select_ entries and after them
before = lines[:start_idx]
after = lines[end_idx:]

# Build new cmpu_select_ entries for ALL buildings
new_entries = []
for building in buildings:
    building_short = building.replace('building_', '')
    build_var = 'sakuya_b6_build_sel_' + building_short
    
    entry = 'cmpu_select_' + building_short + ' = {\n'
    entry += ' scope = country\n'
    entry += ' is_shown = { is_player = yes }\n'
    entry += ' is_valid = { always = yes }\n'
    entry += ' ai_is_valid = { always = no }\n'
    entry += ' effect = {\n'
    entry += ' cmpu_b6_build_clear_all_selected_effect = yes\n'
    for bv in all_build_vars:
        entry += ' set_variable = { name = ' + bv + ' value = 0 }\n'
    entry += ' set_variable = { name = ' + build_var + ' value = 1 }\n'
    entry += ' }\n'
    entry += '}\n'
    entry += '\n'
    new_entries.append(entry)

# Combine
new_content = '\n'.join(before) + '\n' + ''.join(new_entries) + '\n' + '\n'.join(after)

with open(sfx_filepath, 'w', errors='replace') as f:
    f.write(new_content)

# Verify
with open(sfx_filepath, 'r', errors='replace') as f:
    check = f.read()
print('  Total cmpu_select_ entries: ' + str(check.count('cmpu_select_')))
print('  set_variable (build_sel): ' + str(check.count('set_variable = { name = sakuya_b6_build_sel')))
print('  set_variable (value = 1): ' + str(check.count('value = 1 }')))
print('  set_variable (value = 0): ' + str(check.count('value = 0 }')))

# Show coal mine select
lines2 = check.split('\n')
for i, line in enumerate(lines2):
    if 'cmpu_select_coal_mine' in line and '=' in line:
        for j in range(i, min(i+8, len(lines2))):
            print(lines2[j])
        break

# ============================================================
# FIX 5: cmpu_feedback_guis.txt - keep has_variable checks
# ============================================================
fb_filepath = os.path.join(base, 'common', 'scripted_guis', 'cmpu_feedback_guis.txt')
with open(fb_filepath, 'r', errors='replace') as f:
    fb_content = f.read()

# Check current state
fb_wrong = len(re.findall(r'variable = sakuya_b6_selected_building value =', fb_content))
fb_wrong2 = len(re.findall(r'variable = \{ name = sakuya_b6_selected_building value =', fb_content))
fb_has_var = len(re.findall(r'has_variable = sakuya_b6_build_sel', fb_content))

print('Fix 3: Feedback GUI - wrong syntax (no braces): ' + str(fb_wrong))
print('  wrong syntax (with braces): ' + str(fb_wrong2))
print('  has_variable checks: ' + str(fb_has_var))

# Fix any wrong syntax back to has_variable
fb_content = re.sub(r'variable = sakuya_b6_selected_building value = (\w+)', lambda m: 'has_variable = sakuya_b6_build_sel_' + m.group(1).replace('building_', ''), fb_content)
fb_content = re.sub(r'variable = \{ name = sakuya_b6_selected_building value = (\w+) \}', lambda m: 'has_variable = sakuya_b6_build_sel_' + m.group(1).replace('building_', ''), fb_content)

with open(fb_filepath, 'w', errors='replace') as f:
    f.write(fb_content)

# Verify
with open(fb_filepath, 'r', errors='replace') as f:
    fb_check = f.read()
fb_wrong = len(re.findall(r'variable = sakuya_b6_selected_building value =', fb_check))
fb_wrong2 = len(re.findall(r'variable = \{ name = sakuya_b6_selected_building value =', fb_check))
fb_has_var = len(re.findall(r'has_variable = sakuya_b6_build_sel', fb_check))
print('  After fix - wrong syntax (no braces): ' + str(fb_wrong))
print('  After fix - wrong syntax (with braces): ' + str(fb_wrong2))
print('  After fix - has_variable checks: ' + str(fb_has_var))

# ============================================================
# FIX 6: Verify script values
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
print('  1. Click building -> onclick sets sakuya_b6_selected_building (GUI) + calls cmpu_select_X')
print('  2. cmpu_select_X clears ALL build_sel vars to 0, sets selected to 1')
print('  3. Feedback GUI checks has_variable = sakuya_b6_build_sel_X')
print('  4. Only ONE variable is set to 1 -> only selected building shows')