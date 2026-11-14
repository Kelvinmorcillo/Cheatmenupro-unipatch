#!/usr/bin/env python
with open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\script_values\cmpu_feedback_values.txt', 'r', errors='replace') as f:
    c = f.read()
print(c[2000:4000])