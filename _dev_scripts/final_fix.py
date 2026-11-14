#!/usr/bin/env python
import os, re

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

print("=" * 60)
print("FINAL FIX - Add GetVariableSystem.Set back to onclick")
print("=" * 60)

# ============================================================
# FIX 1: onclick handlers - Set GUI variable AND call cmpu_select_X
# ============================================================
gui_filepath = os.path.join(base, 'gui', 'main', 'sakuya_main.gui')
with open(gui_filepath, 'r', errors='replace') as f:
    gui_content = f.read()

gui_lines = gui_content.split('\n')
new_gui_lines = []
gui_fixed = 0

for line in gui_lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetScriptedGui') and 'cmpu_select_' in stripped:
        m = re.search(r"GetScriptedGui\('cmpu_select_(\w+)'\)", stripped)
        if m:
            select_name = m.group(0).replace("GetScriptedGui('", "").replace("')", "")
            building_name = 'building_' + select_name.replace('cmpu_select_', '')
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
print('Fix 1: Fixed ' + str(gui_fixed) + ' onclick handlers (Set GUI var + call cmpu_select_X)')

# Verify
with open(gui_filepath, 'r', errors='replace') as f:
    check = f.read()
lines = check.split('\n')
count = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        count += 1
        if count <= 2:
            print('  ' + stripped[:120])
print('  Total correct onclick: ' + str(count))

# Show coal mine onclick
for line in lines:
    stripped = line.strip()
    if 'onclick' in stripped and 'cmpu_select_coal_mine' in stripped:
        print()
        print('Coal mine onclick: ' + stripped[:150])
        break

# ============================================================
# FIX 2: Verify cmpu_select_X scripted GUIs
# ============================================================
sfx_filepath = os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt')
with open(sfx_filepath, 'r', errors='replace') as f:
    sfx_content = f.read()

# Verify all cmpu_select_X entries exist
gui_buildings = set()
for line in check.split('\n'):
    m = re.search(r"GetScriptedGui\('cmpu_select_(\w+)'\)", line)
    if m:
        gui_buildings.add(m.group(1))

sfx_buildings = set()
for match in re.finditer(r'cmpu_select_(\w+) =', sfx_content):
    sfx_buildings.add(match.group(1))

print()
print('Fix 2: cmpu_select_X entries in scripted GUIs: ' + str(len(sfx_buildings)))
print('  Buildings in GUI: ' + str(len(gui_buildings)))
missing = gui_buildings - sfx_buildings
print('  Missing scripted GUI entries: ' + str(len(missing)))
if missing:
    for b in sorted(missing):
        print('    ' + b)

# ============================================================
# FIX 3: Verify feedback GUI
# ============================================================
fb_filepath = os.path.join(base, 'common', 'scripted_guis', 'cmpu_feedback_guis.txt')
with open(fb_filepath, 'r', errors='replace') as f:
    fb_content = f.read()

# Count has_variable checks
has_var = fb_content.count('has_variable = sakuya_b6_build_sel')
print()
print('Fix 3: Feedback GUI - has_variable checks: ' + str(has_var))

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
print('  1. Click building -> onclick sets sakuya_b6_selected_building (GUI var)')
print('  2. onclick also calls cmpu_select_X (country scope)')
print('  3. cmpu_select_X clears ALL build_sel vars to 0, sets selected to 1')
print('  4. Feedback GUI checks has_variable = sakuya_b6_build_sel_X')
print('  5. Only ONE variable is set to 1 -> only selected building shows')
print('  6. Selector shows selected building via sakuya_b6_selected_building GUI var')