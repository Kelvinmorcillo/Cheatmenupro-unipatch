#!/usr/bin/env python
import re

filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# The pattern is '); GetScriptedGui' - this includes the '); ' that closes Set() 
# We want to add clear codes AFTER the '); ' but BEFORE the ' GetScriptedGui'
# So the replacement should be: '); ' + clear_codes + ' GetScriptedGui'

# The clear codes to add
clear_codes = " GetVariableSystem.Clear('sakuya_b6_build_sel_bank'); GetVariableSystem.Clear('sakuya_b6_build_sel_food_service'); GetVariableSystem.Clear('sakuya_b6_build_sel_pharmaceutical_services'); GetVariableSystem.Clear('sakuya_b6_build_sel_software_industry')"

# Replace '); GetScriptedGui' with '); ' + clear_codes + ' GetScriptedGui'
# Note: we need to keep the '); ' that's already there, and add the clear codes after it
new_content = content.replace(
    '); GetScriptedGui',
    '); ' + clear_codes + ' GetScriptedGui'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Replacement done')