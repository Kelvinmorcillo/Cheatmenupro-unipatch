#!/usr/bin/env python
import re, os

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

# Get all building names from GUI onclick handlers
gui_path = os.path.join(base, 'gui', 'main', 'sakuya_main.gui')
with open(gui_path, 'r', errors='replace') as f:
    gui_content = f.read()

# Extract building names from onclick handlers
pattern = re.compile(r"GetScriptedGui\('cmpu_select_(\w+)'\)")
gui_buildings = set()
for match in pattern.finditer(gui_content):
    gui_buildings.add(match.group(1))

print('Buildings in GUI onclick handlers: ' + str(len(gui_buildings)))

# Get all building names from zz_cmpu_scripted_guis.txt
sfx_path = os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt')
with open(sfx_path, 'r', errors='replace') as f:
    sfx_content = f.read()

sfx_buildings = set()
for match in re.finditer(r'cmpu_select_(\w+) =', sfx_content):
    sfx_buildings.add(match.group(1))

print('Buildings in scripted GUIs: ' + str(len(sfx_buildings)))

# Find missing buildings
missing_in_sfx = gui_buildings - sfx_buildings
missing_in_gui = sfx_buildings - gui_buildings

print()
if missing_in_sfx:
    print('Buildings in GUI but NOT in scripted GUIs (' + str(len(missing_in_sfx)) + '):')
    for b in sorted(missing_in_sfx):
        print('  ' + b)
else:
    print('All GUI buildings have scripted GUI entries')

print()
if missing_in_gui:
    print('Buildings in scripted GUIs but NOT in GUI (' + str(len(missing_in_gui)) + '):')
    for b in sorted(missing_in_gui):
        print('  ' + b)
else:
    print('All scripted GUI buildings are in GUI')

# Check feedback GUI
fb_path = os.path.join(base, 'common', 'scripted_guis', 'cmpu_feedback_guis.txt')
with open(fb_path, 'r', errors='replace') as f:
    fb_content = f.read()

fb_buildings = set()
for match in re.finditer(r'cmpu_fb_sel_(\w+)_check', fb_content):
    fb_buildings.add(match.group(1))

print()
print('Buildings in feedback GUI: ' + str(len(fb_buildings)))

# Check if all buildings in scripted GUIs are in feedback GUI
missing_in_fb = sfx_buildings - fb_buildings
if missing_in_fb:
    print('Buildings in scripted GUIs but NOT in feedback GUI (' + str(len(missing_in_fb)) + '):')
    for b in sorted(missing_in_fb):
        print('  ' + b)
else:
    print('All scripted GUI buildings are in feedback GUI')