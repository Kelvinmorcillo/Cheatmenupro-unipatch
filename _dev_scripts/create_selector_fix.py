#!/usr/bin/env python
import zipfile, os

mod_dir = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'
zip_path = os.path.join(mod_dir, 'clean_fix_selector.zip')

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Add script values file
    src = os.path.join(mod_dir, 'common', 'script_values', 'cmpu_feedback_values.txt')
    zf.write(src, 'common/script_values/cmpu_feedback_values.txt')
    
    # Add README
    readme = "CMPU UNIPOLAR PATCH - SELECTOR FIX\n"
    readme += "========================\n"
    readme += "\n"
    readme += "This zip contains the ESSENTIAL fix:\n"
    readme += "\n"
    readme += "1. common/script_values/cmpu_feedback_values.txt\n"
    readme += "   Adds: cmpu_fb_marked_states_list = {}\n"
    readme += "   Fixes: GetList() error from pdx_persistent_reader\n"
    readme += "   Enables: Refresh and selector counting functionality\n"
    readme += "\n"
    readme += "2. gui/main/sakuya_main.gui\n"
    readme += "   ORIGINAL/UNCHANGED - building selector works as before\n"
    readme += "\n"
    readme += "INSTALLATION:\n"
    readme += "1. Close Victoria 3 completely\n"
    readme += "2. Extract this zip to: C:\\Users\\kelvi\\OneDrive\\Documents\\Paradox Interactive\\Victoria 3\\mod\\cmp_unipolar_patch_v2\\ \n"
    readme += "3. Choose \"Replace\" all files\n"
    readme += "4. Launch Victoria 3 with cmp_unipolar_patch_v2 mod\n"
    readme += "\n"
    readme += "WHAT THIS FIXES:\n"
    readme += "- \"Failed to read key reference: : ,\" error\n"
    readme += "- Refresh button functionality\n"
    readme += "- Selector clicking shows marked state count\n"
    readme += "\n"
    readme += "RESULT:\n"
    readme += "- Core error fixed\n"
    readme += "- Selector clicking shows marked state count\n"
    readme += "- Panel stays visible\n"
    
    zf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    zf.write(os.path.join(mod_dir, 'common', 'script_values', 'cmpu_feedback_values.txt'), 'common/script_values/cmpu_feedback_values.txt')
    zf.write(os.path.join(mod_dir, 'gui', 'main', 'sakuya_main.gui'), 'gui/main/sakuya_main.gui')
    zf.writestr('README.txt', readme)
    zf.close()
    
print('Created', zip_path, os.path.getsize(zip_path), 'bytes')
PYEOF