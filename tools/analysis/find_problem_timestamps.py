#!/usr/bin/env python3
"""
计算有问题视频在合并视频中的时间位置
"""

import subprocess
import json
from pathlib import Path

def get_video_duration(video_path):
    """获取视频时长"""
    ffprobe_path = Path('tools/ffmpeg/bin/ffprobe.exe')
    
    cmd = [
        str(ffprobe_path), '-v', 'quiet', '-print_format', 'json',
        '-show_format', str(video_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            info = json.loads(result.stdout)
            return float(info.get('format', {}).get('duration', 0))
        return 0
    except Exception as e:
        return 0

def calculate_problem_video_timestamps():
    """计算有问题视频的时间戳"""
    video_dir = Path('videos/downloads/ai_vanvan/2025-09-01')
    
    # 合并顺序中的视频列表（排除修复版本和指定问题视频）
    all_videos = list(video_dir.glob('*.mp4'))
    all_videos.sort()
    
    excluded_patterns = ['_std.mp4', '_fixed.mp4', '_normalized.mp4', '_aac_fixed.mp4']
    excluded_videos = ['2025-08-20_15-43-46_UTC.mp4']
    
    merged_videos = []
    for video in all_videos:
        if any(pattern in video.name for pattern in excluded_patterns):
            continue
        if video.name in excluded_videos:
            continue
        merged_videos.append(video)
    
    # 有问题的视频列表
    problem_videos = [
        '2025-04-06_20-06-00_UTC.mp4',      # 44,500 bps
        '2025-05-12_04-45-50_UTC.mp4',      # 37,674 bps
        '2025-06-11_18-34-31_UTC.mp4',      # 43,936 bps
        '2025-06-29_18-58-32_UTC.mp4',      # 37,579 bps
    ]
    
    print("=" * 60)
    print("有问题视频在合并视频中的时间位置")
    print("=" * 60)
    
    current_time = 0.0
    
    for i, video in enumerate(merged_videos, 1):
        duration = get_video_duration(video)
        start_time = current_time
        end_time = current_time + duration
        
        # 格式化时间显示
        start_min = int(start_time // 60)
        start_sec = start_time % 60
        end_min = int(end_time // 60) 
        end_sec = end_time % 60
        
        status = ""
        if video.name in problem_videos:
            status = "⚠️ 有问题 (音质差)"
        
        print(f"#{i:2d} {video.name}")
        print(f"    时间: {start_min:02d}:{start_sec:05.2f} - {end_min:02d}:{end_sec:05.2f}")
        print(f"    时长: {duration:.2f}秒 {status}")
        print()
        
        current_time = end_time
    
    print("=" * 60)
    print("有问题视频时间汇总:")
    print("=" * 60)
    
    current_time = 0.0
    problem_count = 0
    
    for i, video in enumerate(merged_videos, 1):
        duration = get_video_duration(video)
        start_time = current_time
        
        if video.name in problem_videos:
            problem_count += 1
            start_min = int(start_time // 60)
            start_sec = start_time % 60
            end_min = int((start_time + duration) // 60)
            end_sec = (start_time + duration) % 60
            
            print(f"问题视频 #{problem_count}: {video.name}")
            print(f"  位置: {start_min:02d}:{start_sec:05.2f} - {end_min:02d}:{end_sec:05.2f}")
            print(f"  在视频中的第 {i} 段")
            print()
        
        current_time += duration
    
    total_min = int(current_time // 60)
    total_sec = current_time % 60
    print(f"合并视频总时长: {total_min:02d}:{total_sec:05.2f}")

if __name__ == "__main__":
    calculate_problem_video_timestamps()
