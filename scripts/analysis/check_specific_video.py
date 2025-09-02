#!/usr/bin/env python3
"""
检查特定视频的音频比特率
"""
import os
import subprocess

def check_specific_video_bitrate(filename):
    """检查特定视频的音频比特率"""
    video_path = os.path.join("videos", "downloads", "ai_vanvan", "2025-09-01", filename)
    
    if not os.path.exists(video_path):
        print(f"❌ 文件不存在: {filename}")
        return
    
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
        
        print(f"🎬 视频: {filename}")
        print(f"🔊 音频编码: {codec}")
        
        if bitrate:
            bitrate_kbps = bitrate / 1000
            print(f"📊 音频比特率: {bitrate_kbps:.0f}kbps", end="")
            if bitrate_kbps < 50:
                print(" ❌ 低比特率视频 - 这就是问题所在！")
                return True  # 是问题视频
            else:
                print(" ✅ 正常比特率")
                return False  # 不是问题视频
        else:
            print("📊 音频比特率: 无法检测")
            return False
            
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

def main():
    filename = "2025-06-11_18-34-31_UTC.mp4"
    
    print("🔍 检查指定视频是否为问题视频")
    print("=" * 40)
    
    is_problem = check_specific_video_bitrate(filename)
    
    print("\n📋 之前检测出的5个问题视频:")
    problem_videos = [
        "2025-08-19_09-56-05_UTC.mp4",
        "2025-08-19_10-05-11_UTC.mp4", 
        "2025-08-19_15-35-12_UTC.mp4",
        "2025-08-20_15-43-46_UTC.mp4",
        "2025-08-21_14-52-42_UTC.mp4"
    ]
    
    for pv in problem_videos:
        print(f"  - {pv}")
    
    if is_problem:
        if filename in problem_videos:
            print(f"\n✅ {filename} 确实在之前的问题视频列表中")
        else:
            print(f"\n⚠️ {filename} 是新发现的问题视频，之前漏检了！")
    else:
        print(f"\n❓ {filename} 音频比特率正常，卡顿可能由其他原因造成")

if __name__ == "__main__":
    main()
