#!/usr/bin/env python
filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', errors='replace') as f:
    content = f.read()

# Replace )]]" with )]" - remove one extra ]
# Only in onclick lines with cmpu_select_
lines = content.split('\n')
new_lines = []
fixed = 0

for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        # Check for double ]] before closing "
        if ')]"]' in stripped:
            indent = line[:len(line) - len(line.lstrip())]
            new_stripped = stripped.replace(')]"]', ')]"')
            new_line = indent + new_stripped
            new_lines.append(new_line)
            fixed += 1
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w', errors='replace') as f:
    f.write('\n'.join(new_lines))
print('Fixed double bracket in ' + str(fixed) + ' onclick handlers')

# Final verification
count_correct = 0
count_wrong = 0
for line in new_lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        # Correct: onclick = "[...]" - ends with ] then "
        if stripped.endswith(']') and not stripped.endswith(']]'):
            count_correct += 1
        else:
            count_wrong += 1
            print('  WRONG: ' + stripped[:120])
print('Correct format: ' + str(count_correct))
print('Wrong format: ' + str(count_wrong))
print()
print('DONE')