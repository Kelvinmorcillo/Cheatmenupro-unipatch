#!/usr/bin/env python
# Verify the final fix state

# Check GUI onclick handlers
f = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui', 'r', errors='replace')
c = f.read()
f.close()
lines = c.split('\n')

correct = 0
wrong = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_' in stripped:
        # Check format: onclick = "[GetVariableSystem.Set('sakuya_b6_selected_building', 'X'); GetScriptedGui('cmpu_select_X').Execute(...)]"
        # Should end with ])" - ] then "
        if len(stripped) >= 2 and stripped[-2] == ']' and stripped[-1] == '"':
            if len(stripped) >= 3 and stripped[-3] != ']':
                correct += 1
            else:
                wrong += 1
                print('  WRONG (double ]): ' + stripped[:80])
        else:
            wrong += 1
            print('  WRONG (bad ending): ' + stripped[:80] + ' ... last chars: ' + repr(stripped[-5:]))
print('GUI onclick - Correct: ' + str(correct) + ', Wrong: ' + str(wrong))

# Check scripted GUIs
f2 = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\scripted_guis\zz_cmpu_scripted_guis.txt', 'r', errors='replace')
c2 = f2.read()
f2.close()
print('Scripted GUIs - undefined effects: ' + str(c2.count('sakuya_b6_build_select_building_effect')))
print('Scripted GUIs - set_variable entries: ' + str(c2.count('set_variable = { name = sakuya_b6_build_sel')))

# Check script values
f3 = open(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\common\script_values\cmpu_feedback_values.txt', 'r', errors='replace')
c3 = f3.read()
f3.close()
print('Script values - list init: ' + str('cmpu_fb_marked_states_list = {}' in c3))

# Show one full onclick line
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetVariableSystem.Set') and 'cmpu_select_coal_mine' in stripped:
        print()
        print('Sample onclick:')
        print(stripped)
        break