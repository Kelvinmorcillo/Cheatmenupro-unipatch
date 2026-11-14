#!/usr/bin/env python
import zipfile, os

mod_dir = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'
zip_path = os.path.join(mod_dir, 'clean_fix_final_v2.zip')

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Add the script values file
    zf.write(os.path.join(mod_dir, 'common', 'script_values', 'cmpu_feedback_values.txt'), 
             'common/script_values/cmpu_feedback_values.txt')
    # Add the GUI file (now with fixed onclick handlers)
    zf.write(os.path.join(mod_dir, 'gui', 'main', 'sakuya_main.gui'), 
             'gui/main/sakuya_main.gui')
    # Add README (write separately to avoid unicode issues)
    with open('readme_temp.txt', 'w', encoding='utf-8') as f:
        f.write('CMPU UNIPOLAR PATCH - FINAL FIX v2\n========================\n\n')
        f.write('This zip contains the ESSENTIAL fix for the building selector feedback:\n\n')
        f.write('1. common/script_values/cmpu_feedback_values.txt\n')
        f.write('   Adds cmpu_fb_marked_states_list = {}\n')
        f.write('   Fixes the GetList error and enables selector counting functionality\n\n')
        f.write('2. gui/main/sakuya_main.gui\n')
        f.write('   Fixed onclick handlers that now properly:\n')
        f.write('   a) Set the selected building variable (sakuya_b6_selected_building)\n')
        f.write('   b) Clear all four industry variables (bank, food service, pharma, software)\n')
        f.write('   c) Run the CMPU select script\n')
        f.write('   - Proper ; separators ensure Victoria 3 executes all actions\n\n')
        f.write('3. Installation:\n')
        f.write('   1. Close Victoria 3 completely\n')
        f.write('   2. Extract this zip to: C:\\Users\\kelvi\\OneDrive\\Documents\\Paradox Interactive\\Victoria 3\\mod\\cmp_unipolar_patch_v2\\\n')
        f.write('   3. Choose "Replace" all files\n')
        f.write('   4. Launch Victoria 3 with cmp_unipolar_patch_v2 mod\n\n')
        f.write('WHAT THIS FIXES:\n')
        f.write('- Building selected in CMPU mod selector appears in feedback GUI\n')
        f.write('- Numbers update correctly for the selected building\n')
        f.write('- NOT the four fixed buildings showing randomly (bank, food services, pharma, software)\n')
        f.write('- "Failed to read key reference: : ," error fixed\n')
        f.write('- Refresh button works properly\n\n')
        f.write('RESULT: Core error fixed, Selector clicking works, Panel stays visible, ')
        f.write('Building appears as selected in feedback GUI (not always the same four fixed industries)')

    zf.write('readme_temp.txt', 'README.txt')
    os.remove('readme_temp.txt')

print('Created ' + zip_path + ' ' + str(os.path.getsize(zip_path)) + ' bytes')