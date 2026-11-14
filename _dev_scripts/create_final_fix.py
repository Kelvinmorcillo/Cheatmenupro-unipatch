#!/usr/bin/env python
import zipfile, os

mod_dir = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'
zip_path = os.path.join(mod_dir, 'clean_fix_final.zip')

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Add script values file
    src = os.path.join(mod_dir, 'common', 'script_values', 'cmpu_feedback_values.txt')
    zf.write(src, 'common/script_values/cmpu_feedback_values.txt')
    
    # Add README
    readme = "CMPU UNIPOLAR PATCH - CLEAN FIX\n"
    readme += "========================\n"
    readme += "\n"
    readme += "This zip contains the ESSENTIAL fix only:\n"
    readme += "\n"
    readme += "1. common/script_values/cmpu_feedback_values.txt\n"
    readme += "   Adds: cmpu_fb_marked_states_list = {}\n"
    readme += "   Fixes: GetList() error from pdx_persistent_reader\n"
    readme += "   Enables: Refresh button to clear/rebuild marked states list\n"
    readme += "   Does NOT modify GUI onclick handlers\n"
    readme += "\n"
    readme += "2. gui/main/sakuya_main.gui\n"
    readme += "   ORIGINAL/UNCHANGED - your backup restored\n"
    readme += "   Building selector functions exactly as before\n"
    readme += "\n"
    readme += "3. README.txt - These instructions\n"
    readme += "========================\n"
    readme += "INSTALLATION:\n"
    readme += "1. Close Victoria 3 completely\n"
    readme += "2. Extract this zip to: C:\\Users\\kelvi\\OneDrive\\Documents\\Paradox Interactive\\Victoria 3\\mod\\cmp_unipolar_patch_v2\\ \n"
    readme += "3. Choose \"Replace\" all files\n"
    readme += "4. Launch Victoria 3 with cmp_unipolar_patch_v2 mod\n"
    readme += "========================\n"
    readme += "WHAT THIS FIXES:\n"
    readme += "- \"Failed to read key reference: : ,\" error (578 occurrences)\n"
    readme += "- Panel disappearing on building click\n"
    readme += "- Refresh button not working\n"
    readme += "- Building selector works as before\n"
    readme += "\n"
    readme += "WHAT THIS DOES NOT FIX:\n"
    readme += "- Building displayed in feedback not matching selected building\n"
    readme += "- Four industries always showing wrong building data\n"
    readme += "  This requires GUI onclick handler enhancement\n"
    readme += "\n"
    readme += "RESULT:\n"
    readme += "- Core error fixed\n"
    readme += "- Panel stays visible\n"
    readme += "- Refresh works\n"
    readme += "- Selector works unchanged\n"
    readme += "- Building display issue persists (requires onclick enhancement)\n"
    readme += "\n"
    
    zf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    zf.write(os.path.join(mod_dir, 'common', 'script_values', 'cmpu_feedback_values.txt'), 'common/script_values/cmpu_feedback_values.txt')
    zf.write(os.path.join(mod_dir, 'gui', 'main', 'sakuya_main.gui'), 'gui/main/sakuya_main.gui')
    zf.writestr('README.txt', readme)
    zf.close()
    
print('Created', zip_path, os.path.getsize(zip_path), 'bytes')
PYEOF