#!/usr/bin/env python
import zipfile

z = zipfile.ZipFile(r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\clean_fix_final.zip', 'r')

print("=== FILES IN ZIP ===")
for name in z.namelist():
    print('  ' + name + ' (' + str(z.getinfo(name).file_size) + ' bytes)')

print()

# 1. Verify GUI onclick handlers
content = z.read('gui/main/sakuya_main.gui').decode('utf-8', errors='replace')
lines = content.split('\n')
correct = 0
wrong = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetScriptedGui') and 'cmpu_select_' in stripped:
        # Should end with ])" - close paren, close bracket, close quote
        if len(stripped) >= 3 and stripped[-3] == ')' and stripped[-2] == ']' and stripped[-1] == '"':
            correct += 1
        else:
            wrong += 1
            print('  WRONG: ' + stripped[:100] + ' ... last: ' + repr(stripped[-5:]))
print('GUI onclick - Correct: ' + str(correct) + ', Wrong: ' + str(wrong))

# Show sample
for line in lines:
    stripped = line.strip()
    if stripped.startswith('onclick = "[GetScriptedGui') and 'cmpu_select_coal_mine' in stripped:
        print()
        print('Sample onclick:')
        print(stripped)
        break

# 2. Verify scripted GUIs
sfx = z.read('common/scripted_guis/zz_cmpu_scripted_guis.txt').decode('utf-8', errors='replace')
print()
print('Scripted GUIs:')
print('  undefined effects: ' + str(sfx.count('sakuya_b6_build_select_building_effect')))
print('  set_variable (build_sel): ' + str(sfx.count('set_variable = { name = sakuya_b6_build_sel')))
print('  set_variable (selected_building): ' + str(sfx.count('set_variable = { name = sakuya_b6_selected_building')))

# Show coal mine select
lines2 = sfx.split('\n')
for i, line in enumerate(lines2):
    if 'cmpu_select_coal_mine' in line:
        for j in range(i, min(i+6, len(lines2))):
            print(lines2[j])
        break

# 3. Verify feedback GUI
fb = z.read('common/scripted_guis/cmpu_feedback_guis.txt').decode('utf-8', errors='replace')
print()
print('Feedback GUI:')
print('  has_variable checks remaining: ' + str(fb.count('has_variable = sakuya_b6_build_sel')))
print('  variable = sakuya_b6_selected_building checks: ' + str(fb.count('variable = sakuya_b6_selected_building value =')))

# Show one example
for line in fb.split('\n'):
    if 'variable = sakuya_b6_selected_building value = building_coal_mine' in line:
        print()
        print('Example check: ' + line)
        break

# 4. Verify script values
sv = z.read('common/script_values/cmpu_feedback_values.txt').decode('utf-8', errors='replace')
print()
print('Script values:')
print('  cmpu_fb_marked_states_list: ' + str('cmpu_fb_marked_states_list = {}' in sv))

z.close()