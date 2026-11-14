import zipfile, os

mod_dir = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'
zip_path = os.path.join(mod_dir, 'clean_fix_final.zip')

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(os.path.join(mod_dir, 'common', 'script_values', 'cmpu_feedback_values.txt'), 
             'common/script_values/cmpu_feedback_values.txt')
    zf.write(os.path.join(mod_dir, 'gui', 'main', 'sakuya_main.gui'), 
             'gui/main/sakuya_main.gui')
    readme = r"""CMPU UNIPOLAR PATCH - FINAL FIX
========================

This zip contains the ESSENTIAL fix:
1. common/script_values/cmpu_feedback_values.txt - Adds cmpu_fb_marked_states_list = {} which fixes GetList error and enables selector counting functionality
2. gui/main/sakuya_main.gui - Fixed onclick handlers that now properly set the selected building and clear industry variables

INSTALLATION:
1. Close Victoria 3 completely
2. Extract this zip to: C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\
  3. Choose "Replace" all files
4. Launch Victoria 3 with cmp_unipolar_patch_v2 mod

WHAT THIS FIXES:
- "Failed to read key reference: : ," error
- Selector clicking shows marked state count
- Building selected by mod appears in feedback GUI (not always the same four fixed buildings)
RESULT: Core error fixed, Selector clicking works, Panel stays visible, Building appears as selected in feedback"""
    zf.writestr('README.txt', readme)

print('Created', zip_path, os.path.getsize(zip_path), 'bytes')