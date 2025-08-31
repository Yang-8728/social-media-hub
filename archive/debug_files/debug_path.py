#!/usr/bin/env python3
"""
调试路径问题
"""
import os
from src.utils.folder_manager import FolderManager

# 测试配置
config = {
    "download_dir": "videos/downloads/ai_vanvan",
    "merged_dir": "videos/merged/ai_vanvan", 
    "folder_strategy": "daily",
    "folder_pattern": "{date}"
}

folder_manager = FolderManager("ai_vanvan", config)

# 测试路径生成
test_path = folder_manager.get_download_folder("test_blogger")
print(f"生成的路径: {test_path}")
print(f"路径字节: {test_path.encode('utf-8')}")
print(f"路径长度: {len(test_path)}")

# 检查每个字符
for i, char in enumerate(test_path):
    print(f"字符 {i}: '{char}' (U+{ord(char):04X})")
    if ord(char) > 127:
        print(f"  ⚠️  非ASCII字符!")

# 测试标准化
normalized = os.path.normpath(test_path)
print(f"\n标准化后: {normalized}")
print(f"标准化字节: {normalized.encode('utf-8')}")
