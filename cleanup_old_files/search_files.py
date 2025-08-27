import os
import glob

# 尝试查找所有可能的路径
base_paths = [
    r'c:\Code\social-media-hub\videos',
    r'c:\Code\social-media-hub\videos﹨downloads',  # Unicode分隔符
    r'c:\Code\social-media-hub'
]

search_patterns = [
    "**/ai_vanvan/**/2025-08-23*.mp4",
    "**/ai_vanvan/**/2025-08-23*.json*",
    "**/2025-08-23*.*"
]

print("=== 搜索最近下载的文件 ===")
for base_path in base_paths:
    print(f"\n搜索基础路径: {repr(base_path)}")
    print(f"路径存在: {os.path.exists(base_path)}")
    
    if os.path.exists(base_path):
        for pattern in search_patterns:
            full_pattern = os.path.join(base_path, pattern)
            files = glob.glob(full_pattern, recursive=True)
            if files:
                print(f"  模式 {pattern} 找到 {len(files)} 个文件:")
                for f in files[:3]:
                    print(f"    {f}")

# 也尝试手动遍历查找
print(f"\n=== 手动遍历查找 ===")
for root, dirs, files in os.walk(r'c:\Code\social-media-hub'):
    if any('2025-08-23' in f for f in files):
        print(f"在 {root} 找到匹配文件:")
        matching_files = [f for f in files if '2025-08-23' in f]
        for f in matching_files:
            print(f"  {f}")
        print()
