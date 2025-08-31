#!/usr/bin/env python3
"""
测试文件夹管理器功能
"""
import sys
import os
sys.path.append('.')

from src.utils.folder_manager import FolderManager

def test_folder_strategies():
    print("=== 测试文件夹策略 ===")
    
    # 测试 ai_vanvan 账号 (daily 策略)
    print("\n1. 测试 ai_vanvan 账号 (daily 策略)")
    config_vanvan = {
        'download_dir': 'data/downloads/ai_vanvan',
        'merged_dir': 'data/merged/ai_vanvan', 
        'folder_strategy': 'daily',
        'folder_pattern': '{date}'
    }
    fm_vanvan = FolderManager('ai_vanvan', config_vanvan)
    download_folder_vanvan = fm_vanvan.get_download_folder()
    merged_folder_vanvan = fm_vanvan.get_merged_folder()
    print(f"   下载文件夹: {download_folder_vanvan}")
    print(f"   合并文件夹: {merged_folder_vanvan}")
    
    # 测试 aigf8728 账号 (blogger_daily 策略)
    print("\n2. 测试 aigf8728 账号 (blogger_daily 策略)")
    config_aigf = {
        'download_dir': 'data/downloads/aigf8728',
        'merged_dir': 'data/merged/aigf8728',
        'folder_strategy': 'blogger_daily', 
        'folder_pattern': '{blogger}_{date}'
    }
    fm_aigf = FolderManager('aigf8728', config_aigf)
    
    # 测试不同博主
    test_bloggers = ['test_blogger1', 'another_blogger', 'some_chinese_博主']
    for blogger in test_bloggers:
        download_folder = fm_aigf.get_download_folder(blogger)
        merged_folder = fm_aigf.get_merged_folder(blogger)
        print(f"   博主 {blogger}:")
        print(f"     下载文件夹: {download_folder}")
        print(f"     合并文件夹: {merged_folder}")

def check_created_folders():
    print("\n=== 检查创建的文件夹 ===")
    
    base_dirs = ['data/downloads', 'data/merged']
    for base_dir in base_dirs:
        if os.path.exists(base_dir):
            print(f"\n{base_dir}:")
            for account in os.listdir(base_dir):
                account_path = os.path.join(base_dir, account)
                if os.path.isdir(account_path):
                    print(f"  {account}/")
                    for folder in os.listdir(account_path):
                        folder_path = os.path.join(account_path, folder)
                        if os.path.isdir(folder_path):
                            print(f"    {folder}/")

if __name__ == "__main__":
    test_folder_strategies()
    check_created_folders()
