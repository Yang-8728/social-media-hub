import os

# 递归查找所有ai_vanvan相关目录
base_path = r'c:\Code\social-media-hub\videos'
print(f"搜索路径: {base_path}")

for root, dirs, files in os.walk(base_path):
    if 'ai_vanvan' in root:
        print(f"找到目录: {root}")
        print(f"  包含 {len(files)} 个文件")
        if files:
            for f in files[:5]:  # 显示前5个文件
                print(f"    - {f}")
            if len(files) > 5:
                print(f"    ... 还有 {len(files)-5} 个文件")
        print()
