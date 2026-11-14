filepath = r'C:\Users\kelvi\OneDrive\Documents\Paradox Interactive\Victoria 3\mod\cmp_unipolar_patch_v2\gui\main\sakuya_main.gui'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("cmpu_select_war_machine_industry")
if idx >= 0:
    start = max(0, idx - 50)
    end = min(len(content), idx + 200)
    print(content[start:end])
EOF