#!/usr/bin/env python3
"""
修复今天下载的视频记录
由于Unicode路径问题，今天下载的7个视频没有被正确记录到下载日志中
此脚本用于手动补充这些记录
"""
import os
import json
import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.logger import Logger


def scan_todays_videos():
    """扫描今天下载的视频文件"""
    today_folder = "videos/downloads/ai_vanvan/2025-08-26"
    
    if not os.path.exists(today_folder):
        print(f"❌ 文件夹不存在: {today_folder}")
        return []
    
    # 扫描所有mp4文件
    mp4_files = []
    for file in os.listdir(today_folder):
        if file.endswith('.mp4'):
            mp4_files.append(file)
    
    return sorted(mp4_files)


def extract_date_from_filename(filename):
    """从文件名提取日期时间信息"""
    # 文件名格式: 2025-04-19_19-43-12_UTC.mp4
    try:
        date_part = filename.replace('_UTC.mp4', '').replace('_', ' ')
        date_part = date_part.replace('-', '-', 2).replace('-', ':', 2)  # 前两个-保留，后面的改为:
        # 结果: 2025-04-19 19:43:12
        return datetime.strptime(date_part, "%Y-%m-%d %H:%M:%S")
    except:
        return datetime.now()


def generate_shortcode_from_filename(filename):
    """从文件名生成shortcode (临时方案)"""
    # 去掉扩展名并用日期时间生成唯一标识
    base_name = filename.replace('.mp4', '')
    # 使用日期时间的hash作为shortcode
    import hashlib
    hash_obj = hashlib.md5(base_name.encode())
    return f"FIX_{hash_obj.hexdigest()[:10]}"


def add_missing_records():
    """添加缺失的下载记录"""
    print("🔧 修复今天下载的视频记录")
    print("=" * 40)
    
    # 扫描今天的视频文件
    video_files = scan_todays_videos()
    
    if not video_files:
        print("❌ 没有找到今天下载的视频文件")
        return
    
    print(f"📁 找到 {len(video_files)} 个视频文件:")
    for i, file in enumerate(video_files, 1):
        print(f"  {i}. {file}")
    
    # 确认是否添加记录
    if input(f"\n是否为这 {len(video_files)} 个视频添加下载记录? (y/N): ").lower() != 'y':
        print("❌ 取消操作")
        return
    
    # 初始化Logger
    logger = Logger("ai_vanvan")
    log_data = logger.load_download_log()
    
    added_count = 0
    
    for video_file in video_files:
        # 生成记录信息
        shortcode = generate_shortcode_from_filename(video_file)
        file_date = extract_date_from_filename(video_file)
        download_folder = "videos/downloads/ai_vanvan/2025-08-26"
        
        # 检查是否已存在记录
        existing = any(d["shortcode"] == shortcode for d in log_data["downloads"])
        if existing:
            print(f"⚠️  跳过已存在的记录: {shortcode}")
            continue
        
        # 创建下载记录
        download_record = {
            "shortcode": shortcode,
            "download_time": "2025-08-26T10:37:00.000000",  # 使用今天的下载时间
            "status": "success",
            "file_path": download_folder,
            "error": "",
            "merged": False,
            "download_folder": download_folder,
            "blogger_name": "unknown",
            "original_filename": video_file,  # 添加原始文件名用于追踪
            "manual_fix": True  # 标记为手动修复的记录
        }
        
        log_data["downloads"].append(download_record)
        added_count += 1
        print(f"✅ 添加记录: {shortcode} -> {video_file}")
    
    # 保存更新的日志
    logger.save_download_log(log_data)
    
    print(f"\n🎉 成功添加 {added_count} 条下载记录！")
    
    # 验证结果
    total_records = len(log_data["downloads"])
    unmerged_count = len([d for d in log_data["downloads"] if not d.get("merged", False)])
    print(f"📊 当前总记录数: {total_records}")
    print(f"📊 未合并视频数: {unmerged_count}")


def main():
    """主函数"""
    print("🛠️  下载记录修复工具")
    print("用于修复Unicode路径问题导致的记录丢失")
    print("=" * 50)
    
    add_missing_records()


if __name__ == "__main__":
    main()
