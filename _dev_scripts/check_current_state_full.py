#!/usr/bin/env python
import os, re

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

# 1. Check GUI onclick handlers
print("=== GUI ONCLICK HANDLERS ===")
f = open(os.path.join(base, 'gui', 'main', 'sakuya_main.gui'), 'r', errors='replace')
c = f.read()
f.close()
lines = c.split('\n')
coal_onclick = None
count = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        count += 1
        if 'cmpu_select_coal_mine' in stripped:
            coal_onclick = stripped
print('Total onclick with cmpu_select_: ' + str(count))
if coal_onclick:
    print('Coal mine onclick:')
    print(coal_onclick[:200])
else:
    print('WARNING: No coal mine onclick found!')

# 2. Check scripted GUIs
print()
print("=== SCRIPTED GUIS ===")
f2 = open(os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt'), 'r', errors='replace')
c2 = f2.read()
f2.close()
print('Undefined effects remaining: ' + str(c2.count('sakuya_b6_build_select_building_effect')))
print('set_variable entries: ' + str(c2.count('set_variable = { name = sakuya_b6_build_sel')))

# 3. Check feedback GUI panel - how buildings are displayed
print()
print("=== FEEDBACK GUI PANEL STRUCTURE ===")
# Look at lines around the building feedback section
fb_start = None
fb_end = None
for i, line in enumerate(lines):
    if 'cmpu_fb_build_sel_level_0' in line:
        fb_start = i
        break
if fb_start:
    # Find where the building sections start (first building check)
    for i in range(fb_start - 100, fb_start):
        if i >= 0 and 'cmpu_fb_sel_' in lines[i] and 'is_shown' in lines[i]:
            fb_end = i
            break
    print('Feedback panel starts around line ' + str(fb_start))
    # Show first few building sections
    for i in range(max(0, fb_start - 50), min(len(lines), fb_start + 30)):
        print(lines[i][:150])