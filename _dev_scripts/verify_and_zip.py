#!/usr/bin/env python
import zipfile, os

# Verify GUI onclick
f = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', errors='replace')
c = f.read()
f.close()
lines = c.split('\n')
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_coal_mine' in stripped:
        print('Coal mine onclick:')
        print(stripped)
        break

# Verify cmpu_select_X
f2 = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\scripted_guis\zz_cmpu_scripted_guis.txt', 'r', errors='replace')
c2 = f2.read()
f2.close()
lines2 = c2.split(chr(10))
for i, line in enumerate(lines2):
    if 'cmpu_select_coal_mine' in line:
        for j in range(i, min(i+5, len(lines2))):
            print(lines2[j])
        break

# Create zip
mod_dir = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'
zip_path = os.path.join(mod_dir, 'clean_fix_final.zip')

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(os.path.join(mod_dir, 'common', 'script_values', 'cmpu_feedback_values.txt'), 
             'common/script_values/cmpu_feedback_values.txt')
    zf.write(os.path.join(mod_dir, 'gui', 'main', 'sakuya_main.gui'), 
             'gui/main/sakuya_main.gui')
    zf.write(os.path.join(mod_dir, 'common', 'scripted_guis', 'cmpu_feedback_guis.txt'), 
             'common/scripted_guis/cmpu_feedback_guis.txt')
    zf.write(os.path.join(mod_dir, 'common', 'scripted_effects', 'zz_cmpu_clear_selection_effects.txt'), 
             'common/scripted_effects/zz_cmpu_clear_selection_effects.txt')
    zf.write(os.path.join(mod_dir, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt'), 
             'common/scripted_guis/zz_cmpu_scripted_guis.txt')
    
    with open('readme_temp.txt', 'w', encoding='utf-8') as f:
        f.write('CMPU UNIPOLAR PATCH - FINAL FIX\r\n')
        f.write('========================\r\n\r\n')
        f.write('Root cause: cmpu_select_X called undefined effect sakuya_b6_build_select_building_effect.\r\n')
        f.write('No building variable was ever set. Feedback fell back to four fixed industries.\r\n\r\n')
        f.write('Fix 1: Onclick handlers directly set sakuya_b6_selected_building + sakuya_b6_build_sel_X\r\n')
        f.write('       and clear the four industry variables before setting the selected building.\r\n')
        f.write('Fix 2: cmpu_select_X uses set_variable instead of undefined effect.\r\n')
        f.write('Fix 3: cmpu_fb_marked_states_list = {} fixes GetList error.\r\n\r\n')
        f.write('INSTALLATION:\r\n')
        f.write('1. Close Victoria 3 completely.\r\n')
        f.write('2. Extract to: C:\\Users\\kelvi\\OneDrive\\Documents\\Paradox Interactive\\Victoria 3\\mod\\cmp_unipolar_patch_v2\\\r\n')
        f.write('3. Choose \"Replace\" all files.\r\n')
        f.write('4. Launch Victoria 3 with cmp_unipolar_patch_v2 mod.\r\n\r\n')
        f.write('Clicking a building sets sakuya_b6_build_sel_X = 1 and clears industry vars.\r\n')
        f.write('Feedback panel shows the selected building, not the same four fixed ones.\r\n')
    
    zf.write('readme_temp.txt', 'README.txt')
    os.remove('readme_temp.txt')

print()
print('Created ' + zip_path + ' ' + str(os.path.getsize(zip_path)) + ' bytes')