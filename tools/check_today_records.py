#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查今天的下载记录和合并记录对比
"""

import os
import json
import glob
from datetime import datetime
from pathlib import Path

def check_today_records():
    """对比今天的下载记录和合并记录"""
    account_name = "ai_vanvan"
    today = datetime.now().strftime("%Y-%m-%d")
    
    print(f"🔍 检查今天 ({today}) 的记录对比: {account_name}")
    print("=" * 60)
    
    # 1. 检查下载记录
    download_log_path = f"logs/downloads/{account_name}_downloads.json"
    download_records = []
    
    if os.path.exists(download_log_path):
        with open(download_log_path, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
            # 过滤今天的下载记录
            for record in log_data.get("downloads", []):
                download_time = record.get("download_time", "")
                if download_time.startswith(today):
                    download_records.append(record)
    
    print(f"📥 今天的下载记录: {len(download_records)} 条")
    
    # 显示下载详情
    success_downloads = [r for r in download_records if r.get("status") == "success"]
    skipped_downloads = [r for r in download_records if r.get("status") == "skipped"]
    failed_downloads = [r for r in download_records if r.get("status") == "failed"]
    
    print(f"  ✅ 成功下载: {len(success_downloads)} 个")
    print(f"  ⚡ 跳过下载: {len(skipped_downloads)} 个")
    print(f"  ❌ 下载失败: {len(failed_downloads)} 个")
    
    # 2. 检查今天文件夹的实际视频文件
    today_folder = f"videos/downloads/{account_name}/{today}"
    actual_videos = []
    
    if os.path.exists(today_folder):
        actual_videos = glob.glob(os.path.join(today_folder, "*.mp4"))
    
    print(f"\n📂 今天文件夹实际视频: {len(actual_videos)} 个")
    if actual_videos:
        for i, video in enumerate(actual_videos, 1):
            video_name = os.path.basename(video)
            size_mb = os.path.getsize(video) / (1024 * 1024)
            print(f"   {i:2d}. {video_name} ({size_mb:.1f}MB)")
    
    # 3. 检查合并记录
    merge_record_path = f"logs/merges/{account_name}_merged_record.json"
    merged_videos = []
    
    if os.path.exists(merge_record_path):
        with open(merge_record_path, 'r', encoding='utf-8') as f:
            merge_data = json.load(f)
            for merge_info in merge_data.get("merged_videos", []):
                # 检查合并时间是否是今天
                timestamp = merge_info.get("timestamp", "")
                if timestamp.startswith(today):
                    merged_videos.append(merge_info)
    
    print(f"\n🔄 今天的合并记录: {len(merged_videos)} 次合并")
    
    # 4. 分析哪些视频已被合并
    merged_video_paths = set()
    for merge_info in merged_videos:
        for video_path in merge_info.get("input_videos", []):
            merged_video_paths.add(os.path.abspath(video_path))
    
    print(f"📊 已合并的视频文件: {len(merged_video_paths)} 个")
    
    # 5. 对比分析
    print(f"\n📋 详细对比分析:")
    print("-" * 40)
    
    unmerged_videos = []
    merged_count = 0
    
    for video in actual_videos:
        video_abs_path = os.path.abspath(video)
        is_merged = video_abs_path in merged_video_paths
        video_name = os.path.basename(video)
        
        if is_merged:
            print(f"  ✅ {video_name} - 已合并")
            merged_count += 1
        else:
            print(f"  ⏳ {video_name} - 待合并")
            unmerged_videos.append(video)
    
    # 6. 总结
    print(f"\n📈 今天状态总结:")
    print("=" * 40)
    print(f"📥 下载成功:     {len(success_downloads)} 个")
    print(f"📂 文件夹视频:   {len(actual_videos)} 个")  
    print(f"✅ 已合并:       {merged_count} 个")
    print(f"⏳ 待合并:       {len(unmerged_videos)} 个")
    
    if len(unmerged_videos) > 0:
        print(f"\n🎯 建议执行合并操作处理剩余 {len(unmerged_videos)} 个视频")
    else:
        print(f"\n🎉 所有视频都已处理完成！")
    
    # 7. 显示合并输出文件
    if merged_videos:
        print(f"\n📤 今天的合并输出文件:")
        for i, merge_info in enumerate(merged_videos, 1):
            output_file = merge_info.get("output_file", "")
            input_count = merge_info.get("input_count", 0)
            timestamp = merge_info.get("timestamp", "")
            
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                output_name = os.path.basename(output_file)
                time_str = timestamp.split("T")[1][:8] if "T" in timestamp else ""
                print(f"   {i}. {output_name} ({size_mb:.1f}MB) - {input_count}个视频 - {time_str}")
            else:
                print(f"   {i}. {os.path.basename(output_file)} - 文件不存在")

if __name__ == "__main__":
    check_today_records()
