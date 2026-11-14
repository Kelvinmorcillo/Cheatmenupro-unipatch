#!/usr/bin/env python
import os, re

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

# Fix feedback GUI checks from has_variable to variable = { name = X value = 1 }
fb_filepath = os.path.join(base, 'common', 'scripted_guis', 'cmpu_feedback_guis.txt')
with open(fb_filepath, 'r', errors='replace') as f:
    fb_content = f.read()

fb_lines = fb_content.split('\n')
new_fb_lines = []
fb_fixed = 0

for line in fb_lines:
    m = re.search(r"has_variable = (sakuya_b6_build_sel_\w+)", line)
    if m:
        build_var = m.group(1)
        new_line = re.sub(r"has_variable = sakuya_b6_build_sel_\w+", "variable = { name = " + build_var + " value = 1 }", line)
        new_fb_lines.append(new_line)
        fb_fixed += 1
    else:
        new_fb_lines.append(line)

with open(fb_filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_fb_lines))
print('Fixed ' + str(fb_fixed) + ' feedback GUI checks to use variable = { name = X value = 1 }')

# Verify
with open(fb_filepath, 'r', errors='replace') as f:
    fb_check = f.read()
fb_has_var = len(re.findall(r'has_variable = sakuya_b6_build_sel', fb_check))
fb_var_check = len(re.findall(r'variable = \{ name = sakuya_b6_build_sel', fb_check))
print('  Remaining has_variable checks: ' + str(fb_has_var))
print('  New variable = { name = ... } checks: ' + str(fb_var_check))

# Show example
for line in new_fb_lines:
    if 'sakuya_b6_build_sel_coal_mine value = 1' in line:
        print('  Example: ' + line.strip())
        break