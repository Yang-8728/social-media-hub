#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细检查合并后视频的质量问题
包括：跳帧、音频、时长、画质等
"""

import os
import subprocess
import json
from pathlib import Path

def check_video_quality(video_path):
    """检查单个视频的详细质量信息"""
    print(f"\n🔍 检查视频: {os.path.basename(video_path)}")
    print("=" * 60)
    
    # 获取详细视频信息
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', 
        '-show_streams', '-show_frames', '-select_streams', 'v:0', 
        '-read_intervals', '%+#10', video_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ 无法分析视频: {result.stderr}")
            return
            
        data = json.loads(result.stdout)
        
        # 分析视频流
        video_stream = None
        audio_stream = None
        
        for stream in data.get('streams', []):
            if stream['codec_type'] == 'video':
                video_stream = stream
            elif stream['codec_type'] == 'audio':
                audio_stream = stream
        
        # 视频信息
        if video_stream:
            print(f"📹 视频编码: {video_stream.get('codec_name', 'Unknown')}")
            print(f"📐 分辨率: {video_stream.get('width')}x{video_stream.get('height')}")
            print(f"🎬 帧率: {video_stream.get('r_frame_rate', 'Unknown')}")
            print(f"⏱️ 时长: {float(video_stream.get('duration', 0)):.2f}秒")
            
            # 检查帧率是否稳定
            frames = data.get('frames', [])
            if frames:
                frame_times = []
                for frame in frames[:10]:  # 检查前10帧
                    if 'pkt_pts_time' in frame:
                        frame_times.append(float(frame['pkt_pts_time']))
                
                if len(frame_times) > 1:
                    intervals = []
                    for i in range(1, len(frame_times)):
                        intervals.append(frame_times[i] - frame_times[i-1])
                    
                    avg_interval = sum(intervals) / len(intervals)
                    max_diff = max(abs(interval - avg_interval) for interval in intervals)
                    
                    if max_diff > 0.01:  # 超过10ms差异
                        print(f"⚠️  可能存在跳帧 (最大时间差: {max_diff:.3f}s)")
                    else:
                        print("✅ 帧率稳定，无跳帧")
        
        # 音频信息
        if audio_stream:
            print(f"🎵 音频编码: {audio_stream.get('codec_name', 'Unknown')}")
            print(f"🔊 采样率: {audio_stream.get('sample_rate', 'Unknown')}Hz")
            print(f"🎼 声道数: {audio_stream.get('channels', 'Unknown')}")
            print(f"⏱️ 音频时长: {float(audio_stream.get('duration', 0)):.2f}秒")
            print("✅ 有音频轨道")
        else:
            print("❌ 无音频轨道!")
        
        # 检查音视频同步
        if video_stream and audio_stream:
            video_duration = float(video_stream.get('duration', 0))
            audio_duration = float(audio_stream.get('duration', 0))
            duration_diff = abs(video_duration - audio_duration)
            
            if duration_diff > 0.1:  # 超过100ms差异
                print(f"⚠️  音视频可能不同步 (差异: {duration_diff:.3f}s)")
            else:
                print("✅ 音视频同步正常")
        
        # 文件大小和比特率
        format_info = data.get('format', {})
        file_size = int(format_info.get('size', 0))
        duration = float(format_info.get('duration', 0))
        
        if file_size > 0 and duration > 0:
            bitrate = (file_size * 8) / duration / 1000  # kbps
            print(f"📦 文件大小: {file_size / 1024 / 1024:.1f}MB")
            print(f"📊 总比特率: {bitrate:.0f}kbps")
            
            # 检查比特率是否正常
            if bitrate < 500:
                print("⚠️  比特率较低，可能影响画质")
            elif bitrate > 10000:
                print("⚠️  比特率很高，文件较大")
            else:
                print("✅ 比特率正常")
    
    except json.JSONDecodeError:
        print("❌ 无法解析视频信息")
    except Exception as e:
        print(f"❌ 检查失败: {e}")

def main():
    print("🔍 详细视频质量检查")
    print("=" * 50)
    
    # 检查合并视频目录
    merged_dir = Path("videos/merged/ai_vanvan")
    
    if not merged_dir.exists():
        print("❌ 合并视频目录不存在")
        return
    
    # 查找所有视频文件
    video_files = list(merged_dir.glob("*.mp4"))
    
    if not video_files:
        print("❌ 未找到合并后的视频文件")
        return
    
    print(f"📁 找到 {len(video_files)} 个视频文件")
    
    # 逐个检查
    for video_file in video_files:
        check_video_quality(str(video_file))
    
    print("\n" + "=" * 50)
    print("🎯 质量检查完成!")
    print("\n📝 问题排查指南:")
    print("- 跳帧: 检查原始视频质量，考虑重新下载")
    print("- 无音频: 确认源视频有音频，检查合并参数")
    print("- 不同步: 使用 -async 1 参数重新合并")
    print("- 画质差: 调整编码参数或提高比特率")

if __name__ == "__main__":
    main()
