#!/usr/bin/env python3
"""
分析合并行为：检查视频文件夹分布
"""

import json
import os
from pathlib import Path
from collections import defaultdict

def analyze_merge_behavior():
    """分析视频合并行为"""
    
    print("🔍 视频合并行为分析")
    print("=" * 50)
    
    # 加载下载记录
    log_path = Path(r"C:\Code\social-media-hub\videos\download_logs\gaoxiao_downloads.json")
    with open(log_path, 'r', encoding='utf-8') as f:
        download_data = json.load(f)
    
    downloads = download_data.get('downloads', [])
    unmerged_downloads = [d for d in downloads if d.get('status') == 'success' and not d.get('merged', False)]
    
    print(f"📊 未合并视频记录: {len(unmerged_downloads)} 个")
    
    # 检查实际文件分布
    downloads_dir = Path(r"C:\Code\social-media-hub\videos\downloads\gaoxiao")
    
    folder_files = defaultdict(list)
    
    for folder in downloads_dir.iterdir():
        if folder.is_dir():
            folder_name = folder.name
            mp4_files = list(folder.glob("*.mp4"))
            if mp4_files:
                folder_files[folder_name] = mp4_files
    
    print(f"\n📁 文件夹分布:")
    total_files = 0
    for folder_name, files in sorted(folder_files.items()):
        print(f"  📅 {folder_name}: {len(files)} 个视频")
        total_files += len(files)
        for file in files[:3]:  # 显示前3个文件名
            print(f"    - {file.name}")
        if len(files) > 3:
            print(f"    - ... 还有 {len(files) - 3} 个文件")
    
    print(f"\n📊 总计: {total_files} 个MP4文件分布在 {len(folder_files)} 个文件夹中")
    
    # 分析合并逻辑
    print(f"\n🤔 合并行为分析:")
    print(f"根据Logger的get_unmerged_downloads()方法：")
    print(f"  📋 合并器会获取所有未合并的记录")
    print(f"  🔍 不区分文件夹，只看merged字段")
    print(f"  📅 按下载时间排序（最新的在前）")
    
    # 模拟合并器行为
    from src.utils.logger import Logger
    logger = Logger("gaoxiao")
    unmerged_shortcodes = logger.get_unmerged_downloads()
    
    print(f"\n🎬 实际合并行为预测:")
    print(f"  📈 会合并 {len(unmerged_shortcodes)} 个视频")
    print(f"  📁 这些视频分布在不同的日期文件夹中")
    print(f"  🔄 合并器会:")
    print(f"     1. 获取所有未合并记录的shortcode")
    print(f"     2. 在各个文件夹中找到对应的MP4文件")
    print(f"     3. 将所有文件合并成一个视频")
    print(f"     4. 不区分来源文件夹")
    
    # 按文件夹分组显示未合并视频的时间分布
    print(f"\n📅 未合并视频的时间分布:")
    date_groups = defaultdict(int)
    for download in unmerged_downloads:
        download_time = download.get('download_time', '')
        if download_time:
            date = download_time[:10]  # YYYY-MM-DD
            date_groups[date] += 1
    
    for date, count in sorted(date_groups.items()):
        print(f"  {date}: {count} 个视频")
    
    print(f"\n💡 回答你的问题:")
    print(f"❓ 合并会合并两个文件夹内的视频到一起吗？")
    print(f"✅ 是的！合并器会合并所有未合并的视频，不区分文件夹")
    print(f"")
    print(f"❓ 今天下载了几个，明天下载了几个，会如何处理？")
    print(f"✅ 会把今天和明天的视频都合并到一个文件中")
    print(f"")
    print(f"📝 具体行为:")
    print(f"  - 扫描所有 merged=false 的记录")
    print(f"  - 在 2025-08-25 和 2025-08-26 文件夹中找对应视频")
    print(f"  - 按时间顺序合并成一个大视频")
    print(f"  - 合并后所有视频都标记为 merged=true")
    
    return {
        'total_folders': len(folder_files),
        'total_files': total_files,
        'unmerged_records': len(unmerged_downloads),
        'folder_distribution': dict(folder_files)
    }

if __name__ == "__main__":
    result = analyze_merge_behavior()
    
    print(f"\n🎯 总结:")
    print(f"合并器会把 {result['total_folders']} 个文件夹中的 {result['total_files']} 个视频合并成 1 个文件")
