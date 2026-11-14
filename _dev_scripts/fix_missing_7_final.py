#!/usr/bin/env python
import os, re

base = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2'

# Get all building variable names from existing entries
sfx_path = os.path.join(base, 'common', 'scripted_guis', 'zz_cmpu_scripted_guis.txt')
with open(sfx_path, 'r', errors='replace') as f:
    sfx_content = f.read()

# Get all build_sel vars from existing entries
all_build_vars = set()
for match in re.finditer(r'sakuya_b6_build_sel_\w+', sfx_content):
    all_build_vars.add(match.group(0))
all_build_vars = sorted(all_build_vars)

print('Found ' + str(len(all_build_vars)) + ' unique build_sel vars')

# Missing buildings
missing = ['kaiserforum_1', 'kaiserforum_2', 'kaiserforum_3', 'kaiserforum_4',
           'sagrada_familia_cathedral_1', 'sagrada_familia_cathedral_2', 'sagrada_familia_cathedral_3']

# Build new entries
new_entries = []
for building_short in missing:
    build_var = 'sakuya_b6_build_sel_' + building_short
    
    entry = 'cmpu_select_' + building_short + ' = {\n'
    entry += ' scope = country\n'
    entry += ' is_shown = { is_player = yes }\n'
    entry += ' is_valid = { always = yes }\n'
    entry += ' ai_is_valid = { always = no }\n'
    entry += ' effect = {\n'
    entry += ' cmpu_b6_build_clear_all_selected_effect = yes\n'
    for bv in all_build_vars:
        entry += ' set_variable = { name = ' + bv + ' value = 0 }\n'
    entry += ' set_variable = { name = ' + build_var + ' value = 1 }\n'
    entry += ' }\n'
    entry += '}\n'
    entry += '\n'
    new_entries.append(entry)

# Find insertion point (before cmpu_build_has_selected_building_check)
marker = 'cmpu_build_has_selected_building_check'
idx = sfx_content.find(marker)
if idx >= 0:
    new_content = sfx_content[:idx] + ''.join(new_entries) + sfx_content[idx:]
    with open(sfx_path, 'w', errors='replace') as f:
        f.write(new_content)
    print('Added ' + str(len(new_entries)) + ' new cmpu_select_ entries')
else:
    # Append at end
    with open(sfx_path, 'a', errors='replace') as f:
        f.write('\n' + ''.join(new_entries))
    print('Appended ' + str(len(new_entries)) + ' new cmpu_select_ entries')

# Verify
with open(sfx_path, 'r', errors='replace') as f:
    check = f.read()
sfx_buildings = set()
for match in __import__('re').finditer(r'cmpu_select_(\w+) =', check):
    sfx_buildings.add(match.group(1))
print('Total cmpu_select_ entries: ' + str(len(sfx_buildings)))
print('Missing: ' + str(len(set(['kaiserforum_1','kaiserforum_2','kaiserforum_3','kaiserforum_4','sagrada_familia_cathedral_1','sagrada_familia_cathedral_2','sagrada_familia_cathedral_3']) - sfx_buildings)))