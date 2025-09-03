#!/usr/bin/env python3
import json
import os
from pathlib import Path
from datetime import datetime

def check_merge_details():
    """详细检查合并记录"""
    
    print("🔍 详细检查合并记录")
    print("="*50)
    
    # 检查合并记录文件
    merge_record_file = "logs/merges/ai_vanvan_merged_record.json"
    
    if not os.path.exists(merge_record_file):
        print("❌ 合并记录文件不存在")
        return
    
    # 读取合并记录
    with open(merge_record_file, 'r', encoding='utf-8') as f:
        merge_data = json.load(f)
    
    print(f"📁 合并记录文件: {merge_record_file}")
    print(f"📊 总合并次数: {len(merge_data['merged_videos'])}")
    print()
    
    # 检查今天的文件夹
    today = datetime.now().strftime("%Y-%m-%d")
    today_folder = f"videos/downloads/ai_vanvan/{today}"
    
    today_videos = []
    if os.path.exists(today_folder):
        today_videos = [f for f in os.listdir(today_folder) if f.endswith('.mp4')]
    
    print(f"📂 今天文件夹: {today_folder}")
    print(f"📹 今天视频数量: {len(today_videos)}")
    print()
    
    # 分析每次合并记录
    for i, merge_info in enumerate(merge_data['merged_videos'], 1):
        merge_time = merge_info.get('merge_time', merge_info.get('timestamp', 'Unknown'))
        output_file = merge_info['output_file']
        input_count = merge_info['input_count']
        input_videos = merge_info['input_videos']
        
        print(f"🔄 合并记录 {i}:")
        print(f"   时间: {merge_time}")
        print(f"   输出: {os.path.basename(output_file)}")
        print(f"   输入视频数: {input_count}")
        
        # 检查输入视频是否包含今天的文件
        today_inputs = []
        for video_path in input_videos:
            if today in video_path:
                filename = os.path.basename(video_path)
                today_inputs.append(filename)
        
        if today_inputs:
            print(f"   包含今天的视频: {len(today_inputs)} 个")
            for video in today_inputs[:3]:  # 显示前3个
                print(f"     - {video}")
            if len(today_inputs) > 3:
                print(f"     ... 及其他 {len(today_inputs) - 3} 个")
        else:
            print(f"   不包含今天的视频")
        print()
    
    # 检查哪些今天的视频被合并了
    merged_today_videos = set()
    for merge_info in merge_data['merged_videos']:
        for video_path in merge_info['input_videos']:
            if today in video_path:
                filename = os.path.basename(video_path)
                merged_today_videos.add(filename)
    
    print(f"📋 今天被合并的视频汇总:")
    print(f"   总数: {len(merged_today_videos)} 个")
    if merged_today_videos:
        for video in sorted(merged_today_videos):
            print(f"   ✅ {video}")
    
    # 检查未合并的
    unmerged_videos = set(today_videos) - merged_today_videos
    if unmerged_videos:
        print(f"\n⚠️ 未合并的视频:")
        for video in sorted(unmerged_videos):
            print(f"   ❌ {video}")
    else:
        print(f"\n✅ 今天所有视频都已合并")

if __name__ == "__main__":
    check_merge_details()
