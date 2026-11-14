#!/usr/bin/env python
import zipfile, os

mod_dir = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'
zip_path = os.path.join(mod_dir, 'clean_fix_final.zip')

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Add script values file
    src = os.path.join(mod_dir, 'common', 'script_values', 'cmpu_feedback_values.txt')
    zf.write(src, 'common/script_values/cmpu_feedback_values.txt')
    
    # Add README
    readme = '# CMPU UNIPOLAR PATCH - CLEAN FIX\n'
    readme += '#\n'
    readme += '# Fix: common/script_values/cmpu_feedback_values.txt\n'
    readme += '# Adds: cmpu_fb_marked_states_list = {}\n'
    readme += '#\n'
    readme += '# Purpose: Fixes GetList() error from pdx_persistent_reader\n'
    readme += '#        Enables Refresh button to clear/rebuild marked states list\n'
    readme += '#\n'
    readme += '# GUI onclick handlers are ORIGINAL/UNCHANGED\n'
    readme += '# Building selector functions as before\n'
    zf.writestr('README.txt', readme)

print('Created', zip_path, os.path.getsize(zip_path), 'bytes')
PYEOF