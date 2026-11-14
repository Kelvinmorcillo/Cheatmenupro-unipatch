#!/usr/bin/env python
import re

f = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', errors='replace')
c = f.read()
f.close()
lines = c.split('\n')

print("=== All onclick lines ===")
count = 0
for line in lines:
    stripped = line.strip()
    if 'onclick' in stripped:
        count += 1
        if count <= 5:
            print(stripped[:150])
print('Total onclick lines: ' + str(count))

print()
print("=== Onclick with cmpu_select_ ===")
count2 = 0
for line in lines:
    stripped = line.strip()
    if 'onclick' in stripped and 'cmpu_select_' in stripped:
        count2 += 1
        if count2 <= 5:
            print(stripped[:150])
print('Total onclick with cmpu_select_: ' + str(count2))

# Show coal mine specifically
print()
print("=== Coal mine onclick ===")
for line in lines:
    stripped = line.strip()
    if 'onclick' in stripped and 'cmpu_select_coal_mine' in stripped:
        print(stripped)
        break
else:
    print("Not found!")