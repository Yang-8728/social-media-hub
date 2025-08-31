#!/usr/bin/env python3
"""测试路径处理和文件移动"""

import os
import shutil
from pathlib import Path

def find_unicode_folders():
    """查找包含Unicode字符的文件夹"""
    for root, dirs, files in os.walk('.'):
        if 'videos' in root:
            # 检查是否包含特殊Unicode字符
            if '∕' in root or '﹨' in root:
                print(f"Found Unicode folder: {root}")
                if files:
                    print(f"  Files: {files[:3]}...")  # 只显示前3个文件
                
                # 创建正确的目标路径
                correct_path = root.replace('∕', os.sep).replace('﹨', os.sep)
                print(f"  Correct path should be: {correct_path}")
                
                return root, correct_path
    return None, None

def move_files_to_correct_location():
    """将文件移动到正确的位置"""
    unicode_folder, correct_folder = find_unicode_folders()
    
    if unicode_folder and correct_folder:
        print(f"\n移动文件从: {unicode_folder}")
        print(f"        到: {correct_folder}")
        
        # 确保目标文件夹存在
        os.makedirs(correct_folder, exist_ok=True)
        
        # 移动所有文件
        try:
            files = os.listdir(unicode_folder)
            for file in files:
                src = os.path.join(unicode_folder, file)
                dst = os.path.join(correct_folder, file)
                
                if os.path.exists(dst):
                    print(f"  跳过已存在: {file}")
                else:
                    shutil.move(src, dst)
                    print(f"  移动: {file}")
            
            # 删除空的Unicode文件夹
            try:
                os.rmdir(unicode_folder)
                print(f"  删除空文件夹: {unicode_folder}")
            except OSError:
                print(f"  无法删除文件夹（可能不为空）: {unicode_folder}")
                
        except Exception as e:
            print(f"移动文件时出错: {e}")
    else:
        print("没有找到需要修复的文件夹")

if __name__ == "__main__":
    move_files_to_correct_location()
