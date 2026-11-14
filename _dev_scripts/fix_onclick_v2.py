#!/usr/bin/env python
"""
Fix the onclick handlers in sakuya_main.gui to properly set the selected building
and run the CMPU select script, so the feedback GUI shows the selected building
instead of always showing the same four fixed industries.

The problem: Victoria 3 only executes the last onclick on a widget. The original
onclick handlers were missing the ');' separator, so only GetScriptedGui executed,
and the sakuya_b6_selected_building variable was never set.

The fix: Combine the Set() and GetScriptedGui actions into one onclick handler,
ensuring both actions execute when clicking a building.
"""

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
fixed = 0

for line in lines:
    # Check if this line has sakuya_b6_selected_building and GetScriptedGui
    # but missing '); ' before GetScriptedGui
    if 'sakuya_b6_selected_building' in line and 'GetScriptedGui' in line:
        # Check if it already has '); GetScriptedGui'
        if '); GetScriptedGui' not in line:
            # Add '); ' before GetScriptedGui if missing
            # The pattern is: ...software_industry') GetScriptedGui -> ...software_industry'); GetScriptedGui
            new_line = line.replace(' GetScriptedGui', '); GetScriptedGui')
            new_lines.append(new_line)
            fixed += 1
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_lines))

print(f'Fixed {fixed} lines')
print(f'Total lines in file: {len(lines)}')