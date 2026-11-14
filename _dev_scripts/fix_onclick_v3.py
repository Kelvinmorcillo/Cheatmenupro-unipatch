#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# The pattern we're looking for - the exact string that ends the Set() call
# In the original GUI, it's: '); GetScriptedGui'
# We want to replace it with: '); GetVariableSystem.Clear(...); GetScriptedGui'

# Check if the pattern exists
if '); GetScriptedGui' in content:
    print('Pattern found, proceeding with replacement')
    
    # The replacement string - add clear commands after the '); '
    clear_adding = " GetVariableSystem.Clear('sakuya_b6_build_sel_bank'); GetVariableSystem.Clear('sakuya_b6_build_sel_food_service'); GetVariableSystem.Clear('sakuya_b6_build_sel_pharmaceutical_services'); GetVariableSystem.Clear('sakuya_b6_build_sel_software_industry')"
    
    new_content = content.replace(
        '); GetScriptedGui',
        clear_adding + '; GetScriptedGui'
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print('Replacement done')
    print(f'File size: {len(new_content)} chars')
else:
    print('Pattern NOT found in file')