#!/usr/bin/env python3
"""
测试博主名字处理功能
"""
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.folder_manager import FolderManager

def test_blogger_name_processing():
    """测试博主名字处理"""
    print("=== 测试博主名字处理 ===")
    
    # aigf8728 配置
    config_aigf = {
        'download_dir': 'data/downloads/aigf8728',
        'merged_dir': 'data/merged/aigf8728',
        'folder_strategy': 'blogger_daily', 
        'folder_pattern': '{blogger}_{date}'
    }
    
    fm_aigf = FolderManager('aigf8728', config_aigf)
    
    # 测试用例
    test_cases = [
        'lalalala-kakakak',           # 你的例子
        'user-name_123',              # 连字符和下划线
        'blogger@instagram',          # @ 符号
        'name with spaces',           # 空格
        'user.name.test',             # 点号
        'user/with/slashes',          # 斜杠
        'very_long_blogger_name_that_exceeds_normal_length_limits_test',  # 超长名字
        'chinese_博主名_test',        # 中文字符
        'special!@#$%chars',          # 特殊字符
    ]
    
    print(f"当前日期: 2025-08-25")
    print()
    
    for original_name in test_cases:
        # 获取处理后的文件夹
        download_folder = fm_aigf.get_download_folder(original_name)
        merged_folder = fm_aigf.get_merged_folder(original_name)
        
        # 提取文件夹名
        download_folder_name = os.path.basename(download_folder)
        merged_folder_name = os.path.basename(merged_folder)
        
        print(f"原始博主名: '{original_name}'")
        print(f"下载文件夹: {download_folder_name}")
        print(f"合并文件夹: {merged_folder_name}")
        print("-" * 50)

def check_extract_blogger_name():
    """检查博主名提取函数的具体逻辑"""
    print("\n=== 检查博主名提取逻辑 ===")
    
    config_aigf = {
        'download_dir': 'data/downloads/aigf8728',
        'merged_dir': 'data/merged/aigf8728',
        'folder_strategy': 'blogger_daily', 
        'folder_pattern': '{blogger}_{date}'
    }
    
    fm_aigf = FolderManager('aigf8728', config_aigf)
    
    test_names = [
        'lalalala-kakakak',
        'very_long_blogger_name_that_exceeds_normal_length_limits_test'
    ]
    
    for name in test_names:
        clean_name = fm_aigf.extract_blogger_name(name)
        print(f"'{name}' -> '{clean_name}'")

if __name__ == "__main__":
    test_blogger_name_processing()
    check_extract_blogger_name()
