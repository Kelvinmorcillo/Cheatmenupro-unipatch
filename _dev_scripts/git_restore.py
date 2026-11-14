#!/usr/bin/env python
import subprocess, os

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

# Restore all tracked files from git
result = subprocess.run(['git', 'checkout', '--', '.'], capture_output=True, text=True, cwd=base)
print('git checkout -- .')
print('STDOUT:', result.stdout)
print('STDERR:', result.stderr)

# Also restore deleted files
result2 = subprocess.run(['git', 'checkout', 'HEAD', '--', 'gui/main/sakuya_main.gui'], capture_output=True, text=True, cwd=base)
print('git checkout HEAD -- gui/main/sakuya_main.gui')
print('STDOUT:', result2.stdout)
print('STDERR:', result2.stderr)

# Check what files are tracked
result3 = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, cwd=base)
tracked = result3.stdout.strip().split('\n')
print()
print('Tracked files:')
for f in tracked:
    print('  ' + f)