#!/usr/bin/env python3
"""检查和修复路径问题"""

import os
import shutil
from pathlib import Path

def find_unicode_folders():
    """查找包含Unicode字符的文件夹"""
    unicode_folders = []
    for root, dirs, files in os.walk('.'):
        if 'videos' in root and ('∕' in root or '﹨' in root):
            unicode_folders.append((root, files))
    return unicode_folders

def find_recent_files():
    """查找最近下载的文件"""
    recent_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.mp4', '.jpg')) and 'videos' in root:
                file_path = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(file_path)
                    recent_files.append((file_path, mtime))
                except:
                    pass
    
    # 按修改时间排序，最新的在前
    recent_files.sort(key=lambda x: x[1], reverse=True)
    return recent_files[:20]  # 返回最新的20个文件

def main():
    print("🔍 检查路径问题...")
    
    # 检查Unicode路径
    unicode_folders = find_unicode_folders()
    if unicode_folders:
        print(f"发现 {len(unicode_folders)} 个Unicode路径文件夹:")
        for folder, files in unicode_folders:
            print(f"  📁 {folder} ({len(files)} 个文件)")
    else:
        print("✅ 没有发现Unicode路径问题")
    
    # 检查最近的文件
    print("\n🕒 最近下载的文件:")
    recent_files = find_recent_files()
    if recent_files:
        for file_path, mtime in recent_files:
            import datetime
            time_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  📄 {file_path} ({time_str})")
    else:
        print("❌ 没有找到最近的视频文件")
    
    # 检查目标文件夹
    target_folder = "videos/downloads/ai_vanvan/2025-08-25"
    if os.path.exists(target_folder):
        files = os.listdir(target_folder)
        print(f"\n📂 目标文件夹 {target_folder} 包含 {len(files)} 个文件")
        for f in files[:5]:  # 只显示前5个
            print(f"  - {f}")
    else:
        print(f"\n❌ 目标文件夹 {target_folder} 不存在")

if __name__ == "__main__":
    main()
