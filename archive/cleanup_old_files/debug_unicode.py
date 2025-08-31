import os

print("=== 调试Unicode路径查找 ===")
base_path = r'c:\Code\social-media-hub'

found_unicode = False
for root, dirs, files in os.walk(base_path):
    if '﹨' in root:
        found_unicode = True
        print(f"Unicode路径: {root}")
        print(f"  文件数: {len(files)}")
        if files:
            print(f"  前3个文件: {files[:3]}")

if not found_unicode:
    print("没有找到Unicode路径！")
    
    # 让我们直接检查已知路径
    known_unicode_path = r'c:\Code\social-media-hub\videos﹨downloads\ai_vanvan\2025-08-27'
    print(f"\n检查已知Unicode路径: {known_unicode_path}")
    print(f"路径存在: {os.path.exists(known_unicode_path)}")
    
    if os.path.exists(known_unicode_path):
        files = os.listdir(known_unicode_path)
        print(f"文件数: {len(files)}")
        for f in files[:5]:
            print(f"  {f}")
    
    # 也检查其他可能的Unicode路径
    for date_folder in ['2025-08-26', '2025-08-27']:
        unicode_path = f'c:\\Code\\social-media-hub\\videos﹨downloads﹨ai_vanvan﹨{date_folder}'
        print(f"\n检查: {unicode_path}")
        print(f"存在: {os.path.exists(unicode_path)}")
        if os.path.exists(unicode_path):
            files = os.listdir(unicode_path)
            print(f"文件数: {len(files)}")
