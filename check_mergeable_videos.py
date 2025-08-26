#!/usr/bin/env python3
"""
检查可合并视频数量
"""

import json
import os
from pathlib import Path

def check_mergeable_videos():
    """检查可合并的视频数量"""
    
    print("🎬 视频合并状态检查")
    print("=" * 50)
    
    # 加载下载记录
    log_path = Path(r"C:\Code\social-media-hub\videos\download_logs\ai_vanvan_downloads.json")
    with open(log_path, 'r', encoding='utf-8') as f:
        download_data = json.load(f)
    
    downloads = download_data.get('downloads', [])
    
    # 分析下载记录
    total_downloads = len(downloads)
    successful_downloads = [d for d in downloads if d.get('status') == 'success']
    merged_downloads = [d for d in downloads if d.get('status') == 'success' and d.get('merged', False)]
    unmerged_downloads = [d for d in downloads if d.get('status') == 'success' and not d.get('merged', False)]
    
    print(f"📊 下载记录统计:")
    print(f"  📋 总记录数: {total_downloads}")
    print(f"  ✅ 成功下载: {len(successful_downloads)}")
    print(f"  🎬 已合并: {len(merged_downloads)}")
    print(f"  🆕 待合并: {len(unmerged_downloads)}")
    
    # 检查实际文件
    downloads_dir = Path(r"C:\Code\social-media-hub\videos\downloads\ai_vanvan")
    
    mp4_files = []
    for folder in downloads_dir.iterdir():
        if folder.is_dir() and folder.name.startswith('2025-08-'):
            for file in folder.iterdir():
                if file.suffix == '.mp4':
                    mp4_files.append(file)
    
    print(f"\n📁 实际文件统计:")
    print(f"  🎥 MP4文件数: {len(mp4_files)}")
    
    # 显示未合并视频的详细信息
    if unmerged_downloads:
        print(f"\n🎯 可合并的视频详情:")
        print("  时间范围:")
        
        # 按下载时间排序
        unmerged_sorted = sorted(unmerged_downloads, key=lambda x: x.get('download_time', ''))
        
        if unmerged_sorted:
            earliest = unmerged_sorted[0]['download_time'][:10]  # 取日期部分
            latest = unmerged_sorted[-1]['download_time'][:10]
            print(f"    从 {earliest} 到 {latest}")
        
        # 按日期分组统计
        date_groups = {}
        for download in unmerged_downloads:
            download_time = download.get('download_time', '')
            if download_time:
                date = download_time[:10]  # YYYY-MM-DD
                date_groups[date] = date_groups.get(date, 0) + 1
        
        print(f"  📅 按日期分布:")
        for date, count in sorted(date_groups.items()):
            print(f"    {date}: {count} 个视频")
        
        # 显示博主分布
        blogger_count = {}
        for download in unmerged_downloads:
            blogger = download.get('blogger_name', 'unknown')
            blogger_count[blogger] = blogger_count.get(blogger, 0) + 1
        
        print(f"  👤 博主分布:")
        for blogger, count in sorted(blogger_count.items(), key=lambda x: x[1], reverse=True):
            print(f"    {blogger}: {count} 个视频")
        
        print(f"\n🎬 合并建议:")
        print(f"  📈 总计可合并: {len(unmerged_downloads)} 个视频")
        
        # 估算合并后文件大小
        total_size = 0
        for file in mp4_files:
            if file.exists():
                total_size += file.stat().st_size
        
        size_mb = total_size / (1024 * 1024)
        size_gb = size_mb / 1024
        
        if size_gb >= 1:
            print(f"  📦 预估大小: {size_gb:.1f} GB")
        else:
            print(f"  📦 预估大小: {size_mb:.0f} MB")
        
        # 时长估算（按平均30秒/视频估算）
        estimated_duration_seconds = len(unmerged_downloads) * 30
        estimated_minutes = estimated_duration_seconds // 60
        estimated_seconds = estimated_duration_seconds % 60
        
        print(f"  ⏱️  预估时长: {estimated_minutes}分{estimated_seconds}秒 (按30秒/视频估算)")
        
    else:
        print(f"\n✅ 没有待合并的视频!")
    
    return {
        'total_downloads': total_downloads,
        'successful_downloads': len(successful_downloads),
        'merged_downloads': len(merged_downloads),
        'unmerged_downloads': len(unmerged_downloads),
        'mp4_files': len(mp4_files)
    }

if __name__ == "__main__":
    result = check_mergeable_videos()
    
    print(f"\n🎯 合并准备状态:")
    if result['unmerged_downloads'] > 0:
        print(f"✅ 准备就绪！可以合并 {result['unmerged_downloads']} 个视频")
        print(f"💡 建议：运行视频合并器开始合并")
    else:
        print(f"✅ 所有视频都已合并完成")
        print(f"💡 提示：可以运行下载器获取新视频")
