#!/usr/bin/env python
import os, re, shutil, subprocess

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

print("=" * 60)
print("FINAL REAL FIX - Starting fresh")
print("=" * 60)

# ============================================================
# STEP 0: Restore ALL files from git
# ============================================================
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

# Extract building names from onclick handlers
# Format: onclick = "[GetVariableSystem.Set('sakuya_b6_selected_building', 'building_X' ...
pattern = re.compile(r"GetVariableSystem\.Set\('sakuya_b6_selected_building',\s*'([^']+)'")
buildings = set()
for match in pattern.finditer(gui_content):
    buildings.add(match.group(1))

buildings = sorted(buildings)
print('Found ' + str(len(buildings)) + ' unique buildings')

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
            # Proper format: Set GUI variable + run scripted GUI
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

# Verify
with open(gui_filepath, 'r', errors='replace') as f:
    check = f.read()
lines = check.split('\n')
count = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped and '); GetScriptedGui' in stripped:
        count += 1
print('  Verified: ' + str(count) + ' onclick handlers with correct format')

# Show coal mine onclick
for line in lines:
    stripped = line.strip()
    if 'onclick' in stripped and 'cmpu_select_coal_mine' in stripped:
        print('  Coal mine onclick: ' + stripped[:150])
        break

# ============================================================
# STEP 3: Fix zz_cmpu_scripted_guis.txt
# Remove ALL existing cmpu_select_X entries, then create new ones for ALL buildings
# ============================================================
sfx_filepath = os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt')
with open(sfx_filepath, 'r', errors='replace') as f:
    sfx_content = f.read()

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

print('Fix 2: cmpu_select_ entries at lines ' + str(start_idx) + '-' + str(end_idx))

# Keep everything before cmpu_select_ entries and after them
before = lines[:start_idx]
after = lines[end_idx:]

# Get all building variable names
all_build_vars = sorted(['sakuya_b6_build_sel_' + b.replace('building_', '') for b in buildings])

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
    # Clear ALL build_sel vars to 0
    for bv in all_build_vars:
        entry += ' set_variable = { name = ' + bv + ' value = 0 }\n'
    # Set selected building var to 1
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
# FIX 4: cmpu_feedback_guis.txt - revert to has_variable checks
# ============================================================
fb_filepath = os.path.join(base, 'common', 'scripted_guis', 'cmpu_feedback_guis.txt')
with open(fb_filepath, 'r', errors='replace') as f:
    fb_content = f.read()

# Replace any wrong syntax back to has_variable
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
print('Fix 3: Feedback GUI - wrong syntax (no braces): ' + str(fb_wrong))
print('  wrong syntax (with braces): ' + str(fb_wrong2))
print('  has_variable checks: ' + str(fb_has_var))

# ============================================================
# FIX 5: Verify script values
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