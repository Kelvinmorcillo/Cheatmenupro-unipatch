#!/usr/bin/env python
import re

f = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', errors='replace')
c = f.read()
f.close()
lines = c.split('\n')

# Find all feedback GUI building sections and their visibility checks
print("=== Feedback GUI - Building Section Visibility Checks ===")
print()

# Find all cmpu_fb_sel_X_check visibility references in the GUI
checks_found = {}
for i, line in enumerate(lines):
    if "GetScriptedGui('cmpu_fb_sel_" in line and "IsShown" in line:
        # Extract the check name
        m = re.search(r"GetScriptedGui\('(cmpu_fb_sel_\w+_check)'\)", line)
        if m:
            check_name = m.group(1)
            # Find the building name from the text field nearby
            # Look at surrounding lines for text field
            building_name = None
            for j in range(max(0, i-5), min(len(lines), i+5)):
                text_m = re.search(r'text = "cmpu_fb_build_sel_(\w+)"', lines[j])
                if text_m:
                    building_name = text_m.group(1)
                    break
            checks_found[check_name] = building_name

print('Total feedback GUI building sections: ' + str(len(checks_found)))
print()

# Show first 10
count = 0
for check_name, building_name in checks_found.items():
    if count < 15:
        print('  ' + check_name + ' -> building: ' + str(building_name))
        count += 1
print()

# Check: are there sections that DON'T have a building name?
no_building = [(c, b) for c, b in checks_found.items() if b is None]
print('Sections without building name: ' + str(len(no_building)))
for c, b in no_building[:5]:
    print('  ' + c)

# Now check: which sakuya_b6_build_sel_X variables are actually referenced?
print()
print("=== Variables referenced in feedback GUI checks ===")
vars_referenced = set()
for i, line in enumerate(lines):
    m = re.search(r'has_variable = (sakuya_b6_build_sel_\w+)', line)
    if m:
        vars_referenced.add(m.group(1))
print('Total unique sakuya_b6_build_sel_X variables referenced: ' + str(len(vars_referenced)))
print('First 10: ' + str(sorted(list(vars_referenced))[:10]))

# Check: are there level index checks?
level_checks = sum(1 for line in lines if 'sakuya_b6_build_level_idx' in line and 'is_shown' in line)
print('Level index checks: ' + str(level_checks))

# Check: are there any sections that show regardless of selection?
print()
print("=== Checking for sections that might always show ===")
# Look for sections without IsShown or with always=true
always_show = 0
for i, line in enumerate(lines):
    if 'text = "cmpu_fb_build_sel_' in line and 'IsShown' not in line:
        # Check surrounding lines for visible
        has_visible = False
        for j in range(max(0, i-3), min(len(lines), i+3)):
            if 'visible' in lines[j]:
                has_visible = True
                break
        if not has_visible:
            always_show += 1
print('Sections without visibility check: ' + str(always_show))