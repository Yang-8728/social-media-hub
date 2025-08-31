#!/usr/bin/env python3
"""分析预扫描结果的时间分布"""

import os
import sys
from datetime import datetime
import re

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.logger import Logger

def analyze_video_dates():
    """分析下载视频的日期分布"""
    video_folder = "videos/downloads/ai_vanvan/2025-08-25"
    
    if not os.path.exists(video_folder):
        print("❌ 视频文件夹不存在")
        return
    
    # 获取所有mp4文件
    mp4_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
    print(f"总共有 {len(mp4_files)} 个视频文件")
    
    # 按日期分组
    date_groups = {}
    for file in mp4_files:
        # 从文件名提取日期 YYYY-MM-DD
        match = re.match(r'(\d{4}-\d{2}-\d{2})', file)
        if match:
            date_str = match.group(1)
            if date_str not in date_groups:
                date_groups[date_str] = []
            date_groups[date_str].append(file)
    
    # 按日期排序并显示
    print("\n📅 视频日期分布:")
    for date_str in sorted(date_groups.keys(), reverse=True):
        count = len(date_groups[date_str])
        print(f"  {date_str}: {count} 个视频")
        
        # 显示最近几天的详细信息
        if date_str >= '2025-08-20':
            print(f"    最新几个: {date_groups[date_str][:3]}")
    
    # 分析最近的视频
    recent_videos = []
    for date_str in sorted(date_groups.keys(), reverse=True):
        if date_str >= '2025-08-20':  # 最近一周
            recent_videos.extend(date_groups[date_str])
        if len(recent_videos) >= 20:  # 只看前20个最新的
            break
    
    print(f"\n🔥 最近一周的视频: {len(recent_videos)} 个")
    
    # 检查下载记录
    logger = Logger("ai_vanvan")
    log_data = logger.load_download_log()
    
    # 统计不同时期的下载记录
    old_records = [d for d in log_data['downloads'] if d.get('imported_from_old_project')]
    today_records = [d for d in log_data['downloads'] if '2025-08-25' in d.get('download_time', '')]
    
    print(f"\n📊 下载记录统计:")
    print(f"  旧项目导入: {len(old_records)} 条")
    print(f"  昨天下载: {len(today_records)} 条")
    print(f"  总记录: {len(log_data['downloads'])} 条")

if __name__ == "__main__":
    analyze_video_dates()
