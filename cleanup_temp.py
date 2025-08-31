#!/usr/bin/env python3
"""
临时文件清理脚本
删除根目录下的所有测试和临时文件
"""
import glob
import os
import sys

def cleanup_temp_files():
    """清理临时测试文件"""
    print("🧹 开始清理临时测试文件...")
    
    # 定义要删除的文件模式
    temp_patterns = [
        "test_*.py",
        "test_*.mp4", 
        "merge_*.py",
        "analyze_*.py",
        "check_*.py",
        "debug_*.py",
        "fix_*.py",
        "find_*.py",
        "copy_*.py",
        "clean_*.py",
        "diagnose_*.py",
        "quality_*.py",
        "simple_*.py",
        "smart_*.py",
        "sync_*.py",
        "ultimate_*.py",
        "working_*.py",
        "video_*.py",
        "remote_*.py",
        "remove_*.py",
        "advanced_*.py",
        "final_*.py",
        "full_*.py",
        "individual_*.mp4",
        "audio_*.mp4",
        "timestamp_*.mp4",
        "debug_list.txt",
        "ai_vanvan_*.mp4",
    ]
    
    # 要保留的重要文件
    keep_files = {
        "main.py", 
        "requirements.txt", 
        "README.md", 
        "LICENSE", 
        "CONTRIBUTING.md", 
        "CHANGELOG.md",
        "cleanup_temp.py"  # 保留自己
    }
    
    deleted_count = 0
    
    for pattern in temp_patterns:
        files = glob.glob(pattern)
        for file in files:
            # 跳过重要文件
            if file in keep_files:
                continue
            
            # 跳过目录
            if os.path.isdir(file):
                continue
                
            try:
                os.remove(file)
                print(f"   🗑️  删除: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ 删除失败: {file} - {e}")
    
    # 清理特殊文件
    special_files = [
        "自动处理分辨率和编码')",
        "自动检测问题，无需手动观看')"
    ]
    
    for file in special_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"   🗑️  删除特殊文件: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ 删除特殊文件失败: {file} - {e}")
    
    print(f"\n✅ 清理完成! 共删除 {deleted_count} 个临时文件")
    print("✨ 根目录现在更加整洁了！")
    
    # 显示剩余文件
    print(f"\n📁 根目录剩余文件:")
    remaining_files = []
    for item in os.listdir("."):
        if os.path.isfile(item):
            remaining_files.append(item)
    
    remaining_files.sort()
    for file in remaining_files:
        print(f"   📄 {file}")
    
    print(f"\n📊 统计: 剩余 {len(remaining_files)} 个文件")

if __name__ == "__main__":
    # 确保在正确的目录
    if not os.path.exists("src") or not os.path.exists("main.py"):
        print("❌ 请在 social-media-hub 根目录下运行此脚本")
        sys.exit(1)
    
    # 直接执行清理
    cleanup_temp_files()
