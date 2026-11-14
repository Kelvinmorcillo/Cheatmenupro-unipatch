#!/usr/bin/env python
import os, re

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'
sfx_filepath = os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt')

# Get all building names from GUI
gui_path = os.path.join(base, 'gui', 'main', 'sakuya_main.gui')
with open(gui_path, 'r', errors='replace') as f:
    gui_content = f.read()

pattern = re.compile(r"GetScriptedGui\('cmpu_select_(\w+)'\)")
gui_buildings = set()
for match in pattern.finditer(gui_content):
    gui_buildings.add(match.group(1))

# Get all building names from scripted GUIs
with open(sfx_filepath, 'r', errors='replace') as f:
    sfx_content = f.read()

sfx_buildings = set()
for match in re.finditer(r'cmpu_select_(\w+) =', sfx_content):
    sfx_buildings.add(match.group(1))

# Find missing buildings
missing = gui_buildings - sfx_buildings
print('Missing buildings: ' + str(sorted(missing)))

# Get all building variable names
all_build_vars = ['sakuya_b6_build_sel_' + b for b in sorted(gui_buildings)]

# Build new entries for missing buildings
new_entries = []
for building_short in sorted(missing):
    build_var = 'sakuya_b6_build_sel_' + building_short
    
    entry = 'cmpu_select_' + building_short + ' = {\n'
    entry += ' scope = country\n'
    entry += ' is_shown = { is_player = yes }\n'
    entry += ' is_valid = { always = yes }\n'
    entry += ' ai_is_valid = { always = no }\n'
    entry += ' effect = {\n'
    # Clear ALL build_sel vars to 0
    for bv in all_build_vars:
        entry += ' set_variable = { name = ' + bv + ' value = 0 }\n'
    # Set selected building var to 1
    entry += ' set_variable = { name = ' + build_var + ' value = 1 }\n'
    entry += ' }\n'
    entry += '}\n'
    entry += '\n'
    new_entries.append(entry)

# Append new entries before cmpu_build_has_selected_building_check
marker = 'cmpu_build_has_selected_building_check'
idx = sfx_content.find(marker)
if idx >= 0:
    new_content = sfx_content[:idx] + ''.join(new_entries) + sfx_content[idx:]
    with open(sfx_filepath, 'w', errors='replace') as f:
        f.write(new_content)
    print('Added ' + str(len(new_entries)) + ' new cmpu_select_ entries')
else:
    with open(sfx_filepath, 'a', errors='replace') as f:
        f.write('\n' + ''.join(new_entries))
    print('Appended ' + str(len(new_entries)) + ' new cmpu_select_ entries (no marker found)')

# Verify
with open(sfx_filepath, 'r', errors='replace') as f:
    check = f.read()
sfx_buildings2 = set()
for match in re.finditer(r'cmpu_select_(\w+) =', check):
    sfx_buildings2.add(match.group(1))
print('Total cmpu_select_ entries now: ' + str(len(sfx_buildings2)))
print('Missing buildings remaining: ' + str(len(gui_buildings - sfx_buildings2)))