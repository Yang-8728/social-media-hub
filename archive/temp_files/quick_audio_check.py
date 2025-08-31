#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速检查原始视频和合并视频的音频对比
"""

import os
from pathlib import Path

def check_audio_in_video(video_path):
    """检查视频文件中的音频标识"""
    try:
        with open(video_path, 'rb') as f:
            # 读取前64KB数据
            data = f.read(65536)
            
            # 音频编码标识
            audio_signs = [
                b'mp4a',  # MP4 audio
                b'aac ',  # AAC codec
                b'soun',  # sound track
                b'audio', # audio字符串
                b'AudioSampleEntry',  # 音频采样
            ]
            
            found_audio = []
            for sign in audio_signs:
                if sign in data:
                    found_audio.append(sign.decode('ascii', errors='ignore'))
            
            return found_audio
    except:
        return []

def main():
    print("🔍 快速音频检查对比")
    print("=" * 40)
    
    # 检查几个原始视频
    print("📹 检查原始视频音频:")
    vanvan_dir = Path("../insDownloader/test_downloads_vanvan")
    original_videos = list(vanvan_dir.glob("*.mp4"))[:3]
    
    for video in original_videos:
        audio_signs = check_audio_in_video(str(video))
        name = video.name[:25] + "..." if len(video.name) > 25 else video.name
        if audio_signs:
            print(f"✅ {name}: {audio_signs}")
        else:
            print(f"❌ {name}: 无音频标识")
    
    print("\n📹 检查合并视频音频:")
    # 检查合并视频
    merged_dir = Path("videos/merged/ai_vanvan")
    merged_videos = list(merged_dir.glob("*.mp4"))
    
    for video in merged_videos:
        audio_signs = check_audio_in_video(str(video))
        name = video.name[:25] + "..." if len(video.name) > 25 else video.name
        if audio_signs:
            print(f"✅ {name}: {audio_signs}")
        else:
            print(f"❌ {name}: 无音频标识")
    
    print("\n🎯 结论:")
    print("如果原始视频有音频标识但合并后没有，")
    print("那就确认是FFmpeg合并时的音频处理问题！")

if __name__ == "__main__":
    main()
