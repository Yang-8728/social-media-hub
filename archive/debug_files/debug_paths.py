import os
import sys
sys.path.append('src')
from utils.path_utils import clean_unicode_path

# 检查路径情况
path = r'c:\Code\social-media-hub\videos\downloads\ai_vanvan\2025-08-27'
print('标准路径:', repr(path))
print('标准路径存在:', os.path.exists(path))

unicode_path = path.replace('\\', '﹨')
print('Unicode路径:', repr(unicode_path))
print('Unicode路径存在:', os.path.exists(unicode_path))

cleaned = clean_unicode_path(path)
print('清理后路径:', repr(cleaned))
print('清理后=标准?', cleaned == path)

# 看看文件在哪里
if os.path.exists(unicode_path):
    files = os.listdir(unicode_path)
    print(f'Unicode路径中有 {len(files)} 个文件')
    for f in files[:3]:  # 显示前3个
        print(f'  - {f}')

if os.path.exists(path):
    files = os.listdir(path)
    print(f'标准路径中有 {len(files)} 个文件')
else:
    print('标准路径目录不存在或为空')
