#!/usr/bin/env python
import re

fb_filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\scripted_guis\cmpu_feedback_guis.txt'
with open(fb_filepath, 'r', errors='replace') as f:
    content = f.read()

# Replace: variable = sakuya_b6_selected_building value = building_X
# With:    variable = { name = sakuya_b6_selected_building value = building_X }
pattern = r"variable = sakuya_b6_selected_building value = (\w+)"
replacement = r"variable = { name = sakuya_b6_selected_building value = \1 }"

new_content = re.sub(pattern, replacement, content)
count = len(re.findall(pattern, content))

with open(fb_filepath, 'w', errors='replace') as f:
    f.write(new_content)
print('Fixed ' + str(count) + ' feedback GUI checks to use correct syntax')

# Verify
with open(fb_filepath, 'r', errors='replace') as f:
    check = f.read()
remaining_wrong = len(re.findall(r"variable = sakuya_b6_selected_building value = \w+", check))
correct = len(re.findall(r"variable = \{ name = sakuya_b6_selected_building value = \w+ \}", check))
print('  Remaining wrong syntax: ' + str(remaining_wrong))
print('  Correct syntax: ' + str(correct))

# Show example
for line in new_content.split('\n'):
    if 'sakuya_b6_selected_building value = building_coal_mine' in line:
        print('  Example: ' + line.strip())
        break