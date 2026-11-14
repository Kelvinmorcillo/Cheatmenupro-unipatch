#!/usr/bin/env python
import zipfile

# Read the original from the zip
z = zipfile.ZipFile('C:\\Users\\kelvi\\OneDrive\\Documents\\Paradox Interactive\\Victoria 3\\mod\\cmp_unipolar_patch_v2\\clean_fix_final.zip', 'r')
content = z.read('gui/main/sakuya_main.gui').decode('utf-8')
z.close()

# Check the onclick format for coal_mine
idx = content.find("'building_coal_mine'")
if idx >= 0:
    # Find the line
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "'building_coal_mine'" in line:
            print(f'Line {i}:')
            print(line[:300])
            break
else:
    print("'building_coal_mine' not found - this might be the original format")
    
    # Try alternative search
    idx2 = content.find('building_coal_mine')
    if idx2 >= 0:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'building_coal_mine' in line:
                print(f'Line {i} (alt):')
                print(line[:300])
                break