#!/usr/bin/env python3
"""
检测今天下载的23个视频，特别是第三个视频的问题
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
import lzma

def get_video_info(video_path):
    """获取视频信息"""
    try:
        ffprobe_path = Path('tools/ffmpeg/bin/ffprobe.exe')
        if not ffprobe_path.exists():
            ffprobe_path = 'ffprobe'  # 尝试系统PATH
        
        cmd = [
            str(ffprobe_path), '-v', 'quiet', '-print_format', 'json', 
            '-show_format', '-show_streams', str(video_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return None
    except Exception as e:
        print(f"获取视频信息失败: {e}")
        return None

def check_video_integrity(video_path):
    """检查视频完整性"""
    try:
        ffmpeg_path = Path('tools/ffmpeg/bin/ffmpeg.exe')
        if not ffmpeg_path.exists():
            ffmpeg_path = 'ffmpeg'  # 尝试系统PATH
            
        cmd = [str(ffmpeg_path), '-v', 'error', '-i', str(video_path), '-f', 'null', '-']
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0, result.stderr
    except Exception as e:
        return False, str(e)

def analyze_today_videos():
    """分析今天下载的视频"""
    today = datetime.now().strftime('%Y-%m-%d')
    video_dir = Path(f'videos/downloads/ai_vanvan/{today}')
    
    if not video_dir.exists():
        print(f"今天的视频目录不存在: {video_dir}")
        return
    
    print(f"=== 分析今天({today})下载的视频 ===\n")
    
    # 获取所有mp4文件
    mp4_files = list(video_dir.glob('*.mp4'))
    mp4_files.sort()
    
    print(f"发现 {len(mp4_files)} 个视频文件:\n")
    
    problematic_videos = []
    
    for i, video_file in enumerate(mp4_files, 1):
        print(f"--- 视频 #{i}: {video_file.name} ---")
        
        # 检查文件大小
        size_mb = video_file.stat().st_size / (1024 * 1024)
        print(f"文件大小: {size_mb:.2f} MB")
        
        # 获取视频信息
        video_info = get_video_info(video_file)
        if video_info:
            format_info = video_info.get('format', {})
            duration = float(format_info.get('duration', 0))
            print(f"时长: {duration:.2f} 秒")
            
            # 查找视频流
            video_streams = [s for s in video_info.get('streams', []) if s.get('codec_type') == 'video']
            audio_streams = [s for s in video_info.get('streams', []) if s.get('codec_type') == 'audio']
            
            if video_streams:
                vs = video_streams[0]
                print(f"视频编码: {vs.get('codec_name')}")
                print(f"分辨率: {vs.get('width')}x{vs.get('height')}")
                print(f"帧率: {vs.get('r_frame_rate')}")
            
            if audio_streams:
                aus = audio_streams[0]
                print(f"音频编码: {aus.get('codec_name')}")
                print(f"音频采样率: {aus.get('sample_rate')}")
            else:
                print("⚠️  警告: 没有音频流!")
                problematic_videos.append((i, video_file.name, "没有音频流"))
        
        # 检查视频完整性
        is_valid, error_msg = check_video_integrity(video_file)
        if not is_valid:
            print(f"❌ 视频完整性检查失败: {error_msg}")
            problematic_videos.append((i, video_file.name, f"完整性问题: {error_msg}"))
        else:
            print("✅ 视频完整性正常")
        
        # 检查是否有相关的修复文件
        base_name = video_file.stem
        related_files = list(video_dir.glob(f"{base_name}*"))
        if len(related_files) > 4:  # 正常应该有 .mp4, .jpg, .json.xz, .txt
            print(f"⚠️  发现多个相关文件 ({len(related_files)}个):")
            for rf in related_files:
                print(f"   - {rf.name}")
            problematic_videos.append((i, video_file.name, f"有{len(related_files)}个相关文件"))
        
        print()
    
    # 特别检查第三个视频
    if len(mp4_files) >= 3:
        print("=== 特别检查第三个视频 ===")
        third_video = mp4_files[2]  # 索引从0开始
        print(f"第三个视频: {third_video.name}")
        
        # 检查是否有修复版本
        base_name = third_video.stem
        fixed_versions = list(video_dir.glob(f"{base_name}*fixed*.mp4"))
        normalized_versions = list(video_dir.glob(f"{base_name}*normalized*.mp4"))
        aac_versions = list(video_dir.glob(f"{base_name}*aac*.mp4"))
        
        if fixed_versions:
            print(f"发现修复版本: {[f.name for f in fixed_versions]}")
        if normalized_versions:
            print(f"发现标准化版本: {[f.name for f in normalized_versions]}")
        if aac_versions:
            print(f"发现AAC修复版本: {[f.name for f in aac_versions]}")
        
        if fixed_versions or normalized_versions or aac_versions:
            print("❌ 第三个视频确实有问题，已生成修复版本")
        else:
            print("✅ 第三个视频看起来正常")
    
    # 总结
    print("=== 问题总结 ===")
    if problematic_videos:
        print(f"发现 {len(problematic_videos)} 个问题视频:")
        for num, name, issue in problematic_videos:
            print(f"  #{num}: {name} - {issue}")
    else:
        print("所有视频都正常")
    
    # 检查标准化视频
    std_videos = list(video_dir.glob('video*_std.mp4'))
    if std_videos:
        print(f"\n发现 {len(std_videos)} 个标准化视频:")
        for std_video in std_videos:
            size_mb = std_video.stat().st_size / (1024 * 1024)
            print(f"  - {std_video.name} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    analyze_today_videos()
