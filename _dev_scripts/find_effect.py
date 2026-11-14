#!/usr/bin/env python
import os

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'
target = 'sakuya_b6_build_select_building_effect'

for root, dirs, files in os.walk(base):
    for f in files:
        fpath = os.path.join(root, f)
        try:
            with open(fpath, 'r', errors='replace') as fh:
                content = fh.read()
            if target in content:
                print('FOUND in: ' + fpath)
        except:
            pass

print('Search complete.')