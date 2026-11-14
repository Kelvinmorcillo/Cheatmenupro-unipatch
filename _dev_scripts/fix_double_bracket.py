#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

# Fix double ]] to single ]
old = 'End)]"]'
new = 'End)]"'
count = content.count(old)
new_content = content.replace(old, new)

with open(filepath, 'w', errors='replace') as f:
    f.write(new_content)
print('Fixed double bracket in ' + str(count) + ' occurrences')

# Final verification
lines = new_content.split('\n')
count_correct = 0
count_wrong = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        if stripped.endswith(']")') and ']]' not in stripped:
            count_correct += 1
        else:
            count_wrong += 1
            print('  WRONG: ' + stripped[:120])
print('Correct format: ' + str(count_correct))
print('Wrong format: ' + str(count_wrong))
print()
print('DONE')