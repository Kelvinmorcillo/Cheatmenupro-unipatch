#!/usr/bin/env python
import os

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'
targets = ['cmpu_b6_build_clear_all_selected_effect', 'sakuya_b6_build_select_building_effect', 'sakuya_b6_build_select_building_effect']

for target in targets:
    found = False
    for root, dirs, files in os.walk(base):
        for f in files:
            fpath = os.path.join(root, f)
            try:
                with open(fpath, 'r', errors='replace') as fh:
                    content = fh.read()
                if target in content:
                    if not found:
                        print('FOUND "' + target + '" in:')
                        found = True
                    print('  ' + fpath)
            except:
                pass
    if not found:
        print('NOT FOUND: "' + target + '"')

print()
print('Search complete.')