#!/usr/bin/env python
import subprocess, os

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'
result = subprocess.run(['git', 'status'], capture_output=True, text=True, cwd=base)
print('STDOUT:')
print(result.stdout)
print('STDERR:')
print(result.stderr)