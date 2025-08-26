#!/usr/bin/env python3
"""移动文件到正确路径"""

import os
import shutil

def move_files():
    """将Unicode路径的文件移动到正确路径"""
    unicode_folder = r'.\videos﹨downloads﹨ai_vanvan﹨2025-08-25'
    correct_folder = r'.\videos\downloads\ai_vanvan\2025-08-25'
    
    if not os.path.exists(unicode_folder):
        print("❌ Unicode文件夹不存在")
        return
    
    # 确保正确的文件夹存在
    os.makedirs(correct_folder, exist_ok=True)
    
    files = os.listdir(unicode_folder)
    print(f"准备移动 {len(files)} 个文件...")
    
    moved = 0
    skipped = 0
    
    for file in files:
        src = os.path.join(unicode_folder, file)
        dst = os.path.join(correct_folder, file)
        
        if os.path.exists(dst):
            print(f"⚠️  跳过已存在: {file}")
            skipped += 1
        else:
            try:
                shutil.move(src, dst)
                print(f"✅ 移动: {file}")
                moved += 1
            except Exception as e:
                print(f"❌ 移动失败 {file}: {e}")
    
    print(f"\n📊 移动完成: 成功 {moved}, 跳过 {skipped}")
    
    # 尝试删除空的Unicode文件夹
    try:
        remaining = os.listdir(unicode_folder)
        if not remaining:
            os.rmdir(unicode_folder)
            print("🗑️  删除空的Unicode文件夹")
        else:
            print(f"⚠️  Unicode文件夹还有 {len(remaining)} 个文件未移动")
    except Exception as e:
        print(f"⚠️  无法删除Unicode文件夹: {e}")

if __name__ == "__main__":
    move_files()
