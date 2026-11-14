#!/usr/bin/env python
"""
Fix the separators in the onclick handlers to ensure Victoria 3 executes all actions.

The issue: The onclick handlers have the Clear() calls but missing ';' separator 
before GetScriptedGui, so Victoria 3 only executes the last statement.
"""

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
fixed = 0

for line in lines:
    # Check if this line has the pattern without proper ; before GetScriptedGui
    if 'sakuya_b6_selected_building' in line and 'GetScriptedGui' in line:
        # Check if it already has '); GetScriptedGui' (proper format)
        if '); GetScriptedGui' in line:
            new_lines.append(line)
        else:
            # Add ';' before GetScriptedGui if missing
            # The pattern should be: ...software_industry'); GetScriptedGui
            # Or if missing '); ', just add ';' before GetScriptedGui
            if ');' in line and ' GetScriptedGui' in line:
                # Has ); but missing space and GetScriptedGui
                line = line.replace(' GetScriptedGui', '; GetScriptedGui')
            elif ' GetScriptedGui' in line:
                # Missing ); and GetScriptedGui, add '; '
                line = line.replace(' GetScriptedGui', '; GetScriptedGui')
            else:
                # Add '; GetScriptedGui' at the end before the closing ]
                # Find position of ]
                bracket = line.rfind(']')
                if bracket > 0:
                    # Insert before the closing bracket
                    line = line[:bracket] + '; GetScriptedGui' + line[bracket:]
            
            fixed += 1
            print('Fixed line ' + str(fixed) + ': shortened output')
            print('  ' + line[:100] + '...')
    new_lines.append(line)

with open(filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_lines))

print('Fixed ' + str(fixed) + ' lines')