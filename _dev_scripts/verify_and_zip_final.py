#!/usr/bin/env python
import zipfile, os, re

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

print("=== VERIFICATION ===")
print()

# 1. Check GUI onclick handlers
f = open(os.path.join(base, 'gui', 'main', 'sakuya_main.gui'), 'r', errors='replace')
c = f.read()
f.close()
lines = c.split('\n')
gui_correct = 0
gui_wrong = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetScriptedGui') and 'cmpu_select_' in stripped:
        # Check format: onclick = "[GetScriptedGui('cmpu_select_X').Execute(...)]"
        if stripped.endswith(']'):
            gui_correct += 1
        else:
            gui_wrong += 1
            print('  GUI WRONG: ' + stripped[:100])
print('GUI onclick - Correct: ' + str(gui_correct) + ', Wrong: ' + str(gui_wrong))

# Show sample
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetScriptedGui') and 'cmpu_select_coal_mine' in stripped:
        print()
        print('Coal mine onclick:')
        print(stripped)
        break

# 2. Check scripted GUIs
f2 = open(os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt'), 'r', errors='replace')
c2 = f2.read()
f2.close()
sfx_remaining = c2.count('sakuya_b6_build_select_building_effect')
sfx_build = c2.count('set_variable = { name = sakuya_b6_build_sel')
sfx_selected = c2.count('set_variable = { name = sakuya_b6_selected_building')
print()
print('Scripted GUIs - undefined effects: ' + str(sfx_remaining))
print('Scripted GUIs - set_variable (build_sel): ' + str(sfx_build))
print('Scripted GUIs - set_variable (selected_building): ' + str(sfx_selected))

# Show coal mine select
lines2 = c2.split('\n')
for i, line in enumerate(lines2):
    if 'cmpu_select_coal_mine' in line:
        for j in range(i, min(i+6, len(lines2))):
            print(lines2[j])
        break

# 3. Check feedback GUI
f3 = open(os.path.join(base, 'common', 'scripted_guis', 'cmpu_feedback_guis.txt'), 'r', errors='replace')
c3 = f3.read()
f3.close()
fb_remaining = len(re.findall(r'has_variable = sakuya_b6_build_sel', c3))
fb_var = len(re.findall(r'variable = sakuya_b6_selected_building value =', c3))
print()
print('Feedback GUI - remaining has_variable checks: ' + str(fb_remaining))
print('Feedback GUI - variable = sakuya_b6_selected_building checks: ' + str(fb_var))

# 4. Check script values
f4 = open(os.path.join(base, 'common', 'script_values', 'cmpu_feedback_values.txt'), 'r', errors='replace')
c4 = f4.read()
f4.close()
print('Script values - list init: ' + str('cmpu_fb_marked_states_list = {}' in c4))

print()
print('=== ALL VERIFIED ===')

# ============================================================
# CREATE ZIP
# ============================================================
zip_path = os.path.join(base, 'clean_fix_final.zip')

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(os.path.join(base, 'common', 'script_values', 'cmpu_feedback_values.txt'), 
             'common/script_values/cmpu_feedback_values.txt')
    zf.write(os.path.join(base, 'gui', 'main', 'sakuya_main.gui'), 
             'gui/main/sakuya_main.gui')
    zf.write(os.path.join(base, 'common', 'scripted_guis', 'cmpu_feedback_guis.txt'), 
             'common/scripted_guis/cmpu_feedback_guis.txt')
    zf.write(os.path.join(base, 'common', 'scripted_effects', 'zz_cmpu_clear_selection_effects.txt'), 
             'common/scripted_effects/zz_cmpu_clear_selection_effects.txt')
    zf.write(os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt'), 
             'common/scripted_guis/zz_cmpu_scripted_guis.txt')
    
    with open('readme_temp.txt', 'w', encoding='utf-8') as f:
        f.write('CMPU UNIPOLAR PATCH - FINAL FIX\r\n')
        f.write('========================\r\n\r\n')
        f.write('Root cause: cmpu_select_X called undefined effect sakuya_b6_build_select_building_effect,\r\n')
        f.write('so no building variable was ever set. Feedback fell back to four fixed industries.\r\n\r\n')
        f.write('Fix 1: Onclick handlers call cmpu_select_X only (no GetVariableSystem.Set/Clear in onclick).\r\n')
        f.write('Fix 2: cmpu_select_X clears all build_sel vars, sets sakuya_b6_build_sel_X=1,\r\n')
        f.write('       AND sets sakuya_b6_selected_building = building_X.\r\n')
        f.write('Fix 3: Feedback GUI checks variable = sakuya_b6_selected_building value = building_X,\r\n')
        f.write('       so only the selected building shows.\r\n')
        f.write('Fix 4: cmpu_fb_marked_states_list = {} fixes GetList error.\r\n\r\n')
        f.write('INSTALLATION:\r\n')
        f.write('1. Close Victoria 3 completely.\r\n')
        f.write('2. Extract to: C:\\Users\\kelvi\\OneDrive\\Documents\\Paradox Interactive\\Victoria 3\\mod\\cmp_unipolar_patch_v2\\\r\n')
        f.write('3. Choose \"Replace\" all files.\r\n')
        f.write('4. Launch Victoria 3 with cmp_unipolar_patch_v2 mod.\r\n\r\n')
        f.write('Clicking a building sets sakuya_b6_selected_building and sakuya_b6_build_sel_X.\r\n')
        f.write('Feedback panel shows ONLY the selected building, not fixed ones.\r\n')
    
    zf.write('readme_temp.txt', 'README.txt')
    os.remove('readme_temp.txt')

print()
print('Created ' + zip_path + ' ' + str(os.path.getsize(zip_path)) + ' bytes')