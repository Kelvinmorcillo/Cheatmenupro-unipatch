filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find all the building check scripts used in visible conditions
matches = re.findall(r'visible\s*=\s*\"\[GetScriptedGui\(([^)]+)\)\.IsShown', content)
unique = list(set(matches))
print(f'Unique building check scripts: {len(unique)}')
for u in sorted(unique)[:30]:
    print(u)