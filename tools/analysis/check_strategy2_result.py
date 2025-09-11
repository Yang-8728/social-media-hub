#!/usr/bin/env python3
"""
检查方案2的实际执行效果
"""
import os
import subprocess

def check_actual_bitrate(video_path, label):
    """检查视频的实际音频比特率"""
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
                value = line.split('=')[1]
                if value != 'N/A':
                    bitrate = int(value) / 1000
            elif line.startswith('codec_name='):
                codec = line.split('=')[1]
        
        print(f"{label}:")
        print(f"  音频编码: {codec}")
        print(f"  音频比特率: {bitrate:.0f}kbps" if bitrate else "  音频比特率: 无法检测")
        return bitrate
        
    except Exception as e:
        print(f"{label}: 检查失败 - {e}")
        return None

def main():
    print("🔍 检查方案2的实际执行效果")
    print("=" * 50)
    
    # 检查几个关键的问题视频
    problem_videos = [
        "2025-06-11_18-34-31_UTC.mp4",  # 1:39卡顿的视频
        "2025-04-06_20-06-00_UTC.mp4",  # 44kbps问题视频
        "2025-05-12_04-45-50_UTC.mp4"   # 38kbps问题视频
    ]
    
    print("📊 对比原始视频 vs 修复后视频:")
    print("-" * 50)
    
    for video in problem_videos:
        original_path = os.path.join("videos", "downloads", "ai_vanvan", "2025-09-01", video)
        
        print(f"\n🎬 {video}")
        
        if os.path.exists(original_path):
            original_bitrate = check_actual_bitrate(original_path, "  原始版本")
        else:
            print(f"  原始版本: 文件不存在")
            original_bitrate = None
    
    print(f"\n📁 检查合并后的文件:")
    merged_file = "merged_strategy2_23_videos.mp4"
    if os.path.exists(merged_file):
        file_size_mb = os.path.getsize(merged_file) / (1024*1024)
        print(f"  文件: {merged_file}")
        print(f"  大小: {file_size_mb:.1f}MB")
        check_actual_bitrate(merged_file, "  合并文件")
    else:
        print(f"  合并文件不存在: {merged_file}")
    
    print(f"\n🤔 为什么这么快？")
    print("可能的原因:")
    print("  1. FFmpeg使用了 -c:v copy，只重新编码音频")
    print("  2. 音频重新编码确实很快（相比视频编码）")
    print("  3. 文件较小，处理速度快")
    print("  4. 或者实际上没有重新编码，只是复制了")
    
    print(f"\n💡 验证方法:")
    print("  如果合并文件中问题视频的音频比特率仍然是原来的低值，")
    print("  说明修复没有真正生效")

if __name__ == "__main__":
    main()
