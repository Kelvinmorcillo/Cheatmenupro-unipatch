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
        # Check for triple ]] before closing "
        # Pattern: )]]" -> )]"
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
print('Fixed triple bracket in ' + str(fixed) + ' onclick handlers')

# Verify
lines2 = new_lines
count_correct = 0
count_wrong = 0
for line in lines2:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        # Should end with ]" (single ] then ")
        if stripped.endswith(']') or stripped.endswith(']")'):
            # Check last 2 chars are ] and "
            if len(stripped) >= 2 and stripped[-2] == ']' and stripped[-1] == '"':
                # Check 3rd to last is not ]
                if len(stripped) >= 3 and stripped[-3] != ']':
                    count_correct += 1
                else:
                    count_wrong += 1
                    print('  STILL DOUBLE ]: ' + stripped[:100])
            else:
                count_wrong += 1
                print('  BAD ENDING: ' + stripped[:100])
        else:
            count_wrong += 1
            print('  WRONG: ' + stripped[:100])
print('Correct format: ' + str(count_correct))
print('Wrong format: ' + str(count_wrong))
print()
print('DONE')