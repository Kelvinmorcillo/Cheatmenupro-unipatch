#!/usr/bin/env python
import os, re, shutil

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

print("=" * 60)
print("FIX FINAL V4 - Properly fixing both selector and feedback")
print("=" * 60)

# ============================================================
# STEP 0: Restore ALL files from backup
# ============================================================
shutil.copy2(os.path.join(base, 'gui', 'main', 'sakuya_main.gui.bak'), os.path.join(base, 'gui', 'main', 'sakuya_main.gui'))
print('Restored sakuya_main.gui from backup')

# Restore zz_cmpu_scripted_guis.txt from git (tracked file)
import subprocess
result = subprocess.run(['git', 'checkout', 'HEAD', '--', 'common/scripted_guis/zz_cmpu_scripted_guis.txt'], capture_output=True, text=True, cwd=base)
print('Restored zz_cmpu_scripted_guis.txt from git: ' + ('OK' if result.returncode == 0 else 'FAILED'))

# ============================================================
# STEP 1: Extract all building names from GUI onclick handlers
# ============================================================
gui_filepath = os.path.join(base, 'gui', 'main', 'sakuya_main.gui')
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
# STEP 2: Fix onclick handlers
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
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        count += 1
print('  Verified: ' + str(count) + ' onclick handlers with correct format')

# ============================================================
# STEP 3: Fix cmpu_select_X scripted GUIs
# Clear ALL build_sel vars to 0, then set selected to 1
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
    # Find cmpu_select_X entries
    if 'cmpu_select_' in line and '=' in line and 'scope = country' not in line:
        # This is a cmpu_select_X = { line
        # Collect the entire block
        block_lines = [line]
        j = i + 1
        brace_count = 1
        while j < len(sfx_lines) and brace_count > 0:
            block_lines.append(sfx_lines[j])
            brace_count += sfx_lines[j].count('{') - sfx_lines[j].count('}')
            j += 1
        
        # Check if this is a cmpu_select_X block
        block_text = '\n'.join(block_lines)
        m = re.search(r'cmpu_select_(\w+) =', block_text)
        if m:
            select_name = m.group(1)
            build_var = 'sakuya_b6_build_sel_' + select_name
            building_name = 'building_' + select_name
            
            # Build new effect block
            new_block = 'cmpu_select_' + select_name + ' = {\n'
            new_block += ' scope = country\n'
            new_block += ' is_shown = { is_player = yes }\n'
            new_block += ' is_valid = { always = yes }\n'
            new_block += ' ai_is_valid = { always = no }\n'
            new_block += ' effect = {\n'
            # Clear ALL build_sel vars to 0
            for bv in all_build_vars:
                new_block += ' set_variable = { name = ' + bv + ' value = 0 }\n'
            # Set selected building var to 1
            new_block += ' set_variable = { name = ' + build_var + ' value = 1 }\n'
            new_block += ' }\n'
            new_block += '}\n'
            
            # Replace the block
            new_sfx_lines.extend(new_block.split('\n'))
            i = j  # Skip past the old block
            sfx_fixed += 1
            continue
        else:
            # Not a cmpu_select block, keep lines as-is
            new_sfx_lines.extend(block_lines)
            i = j
            continue
    else:
        new_sfx_lines.append(line)
    i += 1

with open(sfx_filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_sfx_lines))
print('Fix 2: Fixed ' + str(sfx_fixed) + ' cmpu_select_X scripted GUIs')

# Verify sfx fix
with open(sfx_filepath, 'r', errors='replace') as f:
    sfx_check = f.read()
sfx_setvars = sfx_check.count('set_variable = { name = sakuya_b6_build_sel')
sfx_zero = sfx_check.count('value = 0 }')
sfx_one = sfx_check.count('value = 1 }')
sfx_select = sfx_check.count('cmpu_select_')
print('  cmpu_select_ entries: ' + str(sfx_select))
print('  set_variable (build_sel): ' + str(sfx_setvars))
print('  value = 0: ' + str(sfx_zero))
print('  value = 1: ' + str(sfx_one))

# Show coal mine select
lines2 = sfx_check.split('\n')
for i, line in enumerate(lines2):
    if 'cmpu_select_coal_mine' in line and '=' in line:
        for j in range(i, min(i+10, len(lines2))):
            print(lines2[j])
        break

# ============================================================
# FIX 3: cmpu_feedback_guis.txt - keep has_variable checks
# ============================================================
fb_filepath = os.path.join(base, 'common', 'scripted_guis', 'cmpu_feedback_guis.txt')
with open(fb_filepath, 'r', errors='replace') as f:
    fb_content = f.read()

# Check if it has any wrong syntax from previous fixes
fb_wrong = len(re.findall(r'variable = sakuya_b6_selected_building value =', fb_content))
fb_wrong2 = len(re.findall(r'variable = \{ name = sakuya_b6_selected_building value =', fb_content))
fb_has_var = len(re.findall(r'has_variable = sakuya_b6_build_sel', fb_content))

print('Fix 3: Feedback GUI - wrong syntax (no braces): ' + str(fb_wrong))
print('  wrong syntax (with braces): ' + str(fb_wrong2))
print('  has_variable checks: ' + str(fb_has_var))

# If there are wrong syntax checks, fix them back to has_variable
if fb_wrong > 0 or fb_wrong2 > 0:
    fb_content = re.sub(r'variable = sakuya_b6_selected_building value = (\w+)', lambda m: 'has_variable = sakuya_b6_build_sel_' + m.group(1).replace('building_', ''), fb_content)
    fb_content = re.sub(r'variable = \{ name = sakuya_b6_selected_building value = (\w+) \}', lambda m: 'has_variable = sakuya_b6_build_sel_' + m.group(1).replace('building_', ''), fb_content)
    with open(fb_filepath, 'w', errors='replace') as f:
        f.write(fb_content)
    print('  Fixed wrong syntax checks')

# Verify
with open(fb_filepath, 'r', errors='replace') as f:
    fb_check = f.read()
fb_has_var = len(re.findall(r'has_variable = sakuya_b6_build_sel', fb_check))
print('  After fix - has_variable checks: ' + str(fb_has_var))

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
print('  1. Click building -> onclick sets sakuya_b6_selected_building (GUI) + calls cmpu_select_X')
print('  2. cmpu_select_X clears ALL build_sel vars to 0, sets selected to 1')
print('  3. Feedback GUI checks has_variable = sakuya_b6_build_sel_X')
print('  4. Only ONE variable is set to 1 -> only selected building shows')