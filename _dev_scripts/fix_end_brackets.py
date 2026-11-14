#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
fixed = 0

for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        # Check if line ends with extra ] before "
        # Pattern: ...Execute(...).End)]"  -> should be ...Execute(...).End)]"
        # Replace multiple ] before " with single ]
        indent = line[:len(line) - len(line.lstrip())]
        # Use regex to replace ) followed by one or more ] followed by "
        # with ) followed by single ] followed by "
        new_stripped = re.sub(r'\)\]+\"', ')\"]', stripped)
        if new_stripped != stripped:
            new_line = indent + new_stripped
            new_lines.append(new_line)
            fixed += 1
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_lines))
print('Fixed bracket count in ' + str(fixed) + ' onclick handlers')

# Verify
lines2 = new_lines
count_correct = 0
count_wrong = 0
for line in lines2:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        # Correct ending: ]" (single ] then ")
        # Wrong: ]]" (double ]) or other
        if len(stripped) >= 2 and stripped[-2] == ']' and stripped[-1] == '"':
            if len(stripped) >= 3 and stripped[-3] != ']':
                count_correct += 1
            else:
                count_wrong += 1
                print('  STILL DOUBLE ]: ' + stripped[:100])
        else:
            count_wrong += 1
            print('  BAD ENDING: ' + stripped[:100])
print('Correct format: ' + str(count_correct))
print('Wrong format: ' + str(count_wrong))
print()
print('DONE')