filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find all lines with sakuya_b6_selected_building
lines = content.split('\n')
indices = []
for i, line in enumerate(lines):
    if 'sakuya_b6_selected_building' in line:
        indices.append(i)

print(f'Found {len(indices)} lines with sakuya_b6_selected_building')

# Check how many have the combined format (have ; GetScriptedGui)
combined = 0
separate = 0
for idx in indices:
    line = lines[idx]
    if '; GetScriptedGui' in line:
        combined += 1
    else:
        separate += 1

print(f'Combined format: {combined}')
print(f'Separate format: {separate}')

# Show a few examples
for idx in indices[:3]:
    print(f'\\nExample {idx}: {lines[idx][:120]}')
"