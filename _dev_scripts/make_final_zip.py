#!/usr/bin/env python
import zipfile, os

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
    
    # README
    with open('readme_temp.txt', 'w', encoding='utf-8') as f:
        f.write('CMPU UNIPOLAR PATCH - FINAL FIX\r\n')
        f.write('========================\r\n\r\n')
        f.write('This fix makes the feedback GUI reflect the building selected in the CMPU mod selector.\r\n\r\n')
        f.write('Root cause: cmpu_select_X scripted GUIs called an undefined effect (sakuya_b6_build_select_building_effect),\r\n')
        f.write('so no building variable was ever set. The feedback panel fell back to the same four fixed buildings.\r\n\r\n')
        f.write('Files included:\r\n')
        f.write('1. common/script_values/cmpu_feedback_values.txt - cmpu_fb_marked_states_list = {} (fixes GetList error)\r\n')
        f.write('2. gui/main/sakuya_main.gui - Fixed onclick handlers (set building var + call cmpu_select_X)\r\n')
        f.write('3. common/scripted_guis/cmpu_feedback_guis.txt - Feedback panel visibility checks\r\n')
        f.write('4. common/scripted_effects/zz_cmpu_clear_selection_effects.txt - Clear all selection variables\r\n')
        f.write('5. common/scripted_guis/zz_cmpu_scripted_guis.txt - cmpu_select_X with set_variable (FIXED)\r\n\r\n')
        f.write('INSTALLATION:\r\n')
        f.write('1. Close Victoria 3 completely\r\n')
        f.write('2. Extract this zip to: C:\\Users\\kelvi\\OneDrive\\Documents\\Paradox Interactive\\Victoria 3\\mod\\cmp_unipolar_patch_v2\\\r\n')
        f.write('3. Choose "Replace" all files\r\n')
        f.write('4. Launch Victoria 3 with cmp_unipolar_patch_v2 mod\r\n\r\n')
        f.write('HOW IT WORKS:\r\n')
        f.write('Clicking a building sets sakuya_b6_selected_building variable and runs cmpu_select_X.\r\n')
        f.write('cmpu_select_X clears all selection variables and sets sakuya_b6_build_sel_X = 1 via set_variable.\r\n')
        f.write('The feedback panel reads this variable and displays the selected building with correct counts.\r\n')
    
    zf.write('readme_temp.txt', 'README.txt')
    os.remove('readme_temp.txt')

print('Created ' + zip_path + ' ' + str(os.path.getsize(zip_path)) + ' bytes')