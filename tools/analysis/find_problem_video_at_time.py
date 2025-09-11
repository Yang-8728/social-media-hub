#!/usr/bin/env python3
"""
分析合并视频中1:39位置对应的原始视频
"""
import os
import subprocess
import glob

def get_video_duration(video_path):
    """获取视频时长（秒）"""
    try:
        ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
        cmd = [
            ffprobe_exe,
            "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"❌ 无法获取时长 {video_path}: {e}")
        return 0

def find_video_at_time(target_seconds):
    """找到指定时间点对应的视频"""
    VIDEO_DIR = "videos/downloads/ai_vanvan/2025-09-01"
    
    # 获取所有视频文件（按文件名排序，这是合并时的顺序）
    video_pattern = os.path.join(VIDEO_DIR, "*.mp4")
    all_videos = sorted(glob.glob(video_pattern))
    
    print(f"🎯 查找 {target_seconds}秒（{target_seconds//60}:{target_seconds%60:02.0f}）位置的视频")
    print("=" * 60)
    
    current_time = 0
    
    for i, video in enumerate(all_videos):
        duration = get_video_duration(video)
        video_start = current_time
        video_end = current_time + duration
        
        filename = os.path.basename(video)
        
        # 检查目标时间是否在这个视频范围内
        if video_start <= target_seconds <= video_end:
            relative_time = target_seconds - video_start
            print(f"🎬 找到了！")
            print(f"📁 文件: {filename}")
            print(f"⏱️ 视频时长: {duration:.1f}秒")
            print(f"📍 在合并视频中的位置: {video_start:.1f}s - {video_end:.1f}s")
            print(f"🎯 卡顿时间在该视频的: {relative_time:.1f}秒处")
            print(f"📊 这是第 {i+1} 个视频")
            
            # 检查这个视频的音频比特率
            print(f"\n🔍 检查该视频的音频质量...")
            check_audio_bitrate(video)
            return video, relative_time
        
        print(f"{i+1:2d}. {filename:<35} {duration:6.1f}s  [{video_start:6.1f}s - {video_end:6.1f}s]")
        current_time += duration
    
    print(f"❌ 在总时长 {current_time:.1f}秒中未找到 {target_seconds}秒")
    return None, 0

def check_audio_bitrate(video_path):
    """检查视频的音频比特率"""
    try:
        ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
        cmd = [
            ffprobe_exe,
            "-v", "quiet",
            "-select_streams", "a:0",
            "-show_entries", "stream=bit_rate,codec_name",
            "-of", "default=noprint_wrappers=1",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        
        bitrate = None
        codec = None
        
        for line in output.split('\n'):
            if line.startswith('bit_rate='):
                bitrate = int(line.split('=')[1]) if line.split('=')[1] != 'N/A' else None
            elif line.startswith('codec_name='):
                codec = line.split('=')[1]
        
        if bitrate:
            bitrate_kbps = bitrate / 1000
            print(f"🔊 音频编码: {codec}")
            print(f"📊 音频比特率: {bitrate_kbps:.0f}kbps", end="")
            if bitrate_kbps < 50:
                print(" ❌ (低比特率，可能有问题)")
            else:
                print(" ✅")
        else:
            print(f"🔊 音频编码: {codec}")
            print(f"📊 音频比特率: 无法检测")
            
    except Exception as e:
        print(f"❌ 检查音频失败: {e}")

def main():
    # 1:39 = 99秒
    target_time = 1 * 60 + 39  # 99秒
    
    video, relative_time = find_video_at_time(target_time)
    
    if video:
        print(f"\n💡 建议:")
        print(f"1. 单独播放这个视频: {os.path.basename(video)}")
        print(f"2. 检查该视频在 {relative_time:.1f}秒 处是否有问题")
        print(f"3. 如果这个视频音频比特率很低，可能就是卡顿原因")

if __name__ == "__main__":
    main()
