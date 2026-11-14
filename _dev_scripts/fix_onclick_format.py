#!/usr/bin/env python
# Fix onclick format: ensure '); ' exists after building name before GetVariableSystem.Clear
import re

with open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', encoding='utf-8') as f:
    content = f.read()

# The pattern we need to fix: 'building_X' GetVariableSystem.Clear
# Should be: 'building_X'); GetVariableSystem.Clear
# Currently it's: 'building_X' GetVariableSystem.Clear (missing '); '

# Replace the pattern: 'building_X' GetVariableSystem.Clear 
# with: 'building_X'); GetVariableSystem.Clear

# Find all occurrences and fix them
# Pattern: a single quote, building name, single quote, then immediately GetVariableSystem.Clear
# We need to insert '); ' after the closing quote of the building name

# Actually, let's use a simpler approach: just ensure every line with sakuya_b6_selected_building
# has '); ' before GetVariableSystem.Clear

lines = content.split('\n')
fixed = 0

for i, line in enumerate(lines):
    # Check if this line needs fixing
    # The broken format has the building name followed directly by GetVariableSystem.Clear
    # without '); ' in between
    if 'sakuya_b6_selected_building' in line and 'GetVariableSystem.Clear' in line:
        # Check if '); ' already exists before GetVariableSystem.Clear
        # We'll look for the pattern: '); GetVariableSystem.Clear'
        if '); GetVariableSystem.Clear' not in line:
            # Fix: insert '); ' before GetVariableSystem.Clear
            # Find position of GetVariableSystem.Clear
            clear_idx = line.find('GetVariableSystem.Clear')
            if clear_idx >= 0:
                # Insert '); ' at that position
                new_line = line[:clear_idx] + '); GetVariableSystem.Clear'
                lines[i] = new_line
                fixed += 1

with open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'Fixed {fixed} lines')
"