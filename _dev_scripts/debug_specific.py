filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find all the building check scripts used in visible conditions
matches = re.findall(r'visible\s*=\s*\"\[GetScriptedGui\(([^)]+)\)\.IsShown', content)
unique = list(set(matches))

# Find the specific ones
for keyword in ['bank', 'food', 'pharmaceutical', 'software']:
    print(f'\\n=== {keyword} ===')
    for u in unique:
        if keyword in u.lower():
            print(u)