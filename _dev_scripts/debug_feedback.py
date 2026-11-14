#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Check for sakuya_b6_selected_building usage
print('=== sakuya_b6_selected_building occurrences ===')
matches = re.findall(r'sakuya_b6_selected_building', content)
print(f'Total: {len(matches)}')

# Show context around a few
for i, m in enumerate(matches[:5]):
    # Find line number
    idx = content.find(m)
    line_start = content.rfind('\n', 0, idx) + 1
    line_end = content.find('\n', idx)
    if line_end == 0: line_end = len(content)
    line = content[line_start:line_end]
    print(f'  Match {i+1}: ...{line[:100]}...')

# Check the four industry variables
print()
print('=== Four industry variable occurrences ===')
for var in ['sakuya_b6_build_sel_bank', 'sakuya_b6_build_sel_food_service', 
            'sakuya_b6_build_sel_pharmaceutical_services', 'sakuya_b6_build_sel_software_industry']:
    count = content.count(var)
    print(f'{var}: {count}')

# Look for the feedback panel display logic
print()
print('=== Searching for feedback display patterns ===')
# Look for common Victoria 3 GUI display patterns
patterns = ['value', 'count', 'country', 'state', 'building_sel']
for p in patterns:
    count = len(re.findall(p, content, re.IGNORECASE))
    print(f'  "{p}": {count} matches')