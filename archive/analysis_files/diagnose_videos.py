#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诊断每个视频的音视频时长
"""

import subprocess
import json
from pathlib import Path

def diagnose_videos():
    """诊断每个视频的音视频时长"""
    print("🔍 诊断视频音视频时长")
    print("=" * 40)
    
    # 获取前5个视频文件
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))[:5]
    
    total_video_duration = 0
    total_audio_duration = 0
    
    for i, video in enumerate(video_files, 1):
        print(f"\n📹 视频 {i}: {video.name}")
        
        # 获取详细信息
        cmd = [
            "tools/ffmpeg/bin/ffprobe.exe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            "-show_format",
            str(video)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                info = json.loads(result.stdout)
                
                video_duration = None
                audio_duration = None
                has_audio = False
                
                for stream in info.get("streams", []):
                    if stream.get("codec_type") == "video":
                        video_duration = float(stream.get("duration", 0))
                    elif stream.get("codec_type") == "audio":
                        audio_duration = float(stream.get("duration", 0))
                        has_audio = True
                
                print(f"   📊 视频时长: {video_duration:.3f}秒")
                if has_audio:
                    print(f"   🔊 音频时长: {audio_duration:.3f}秒")
                    diff = abs(video_duration - audio_duration) if video_duration and audio_duration else 0
                    if diff < 0.1:
                        print(f"   ✅ 音视频同步良好 (差异: {diff:.3f}秒)")
                    else:
                        print(f"   ⚠️ 音视频不同步 (差异: {diff:.3f}秒)")
                else:
                    print(f"   ❌ 无音频流!")
                    audio_duration = 0
                
                total_video_duration += video_duration if video_duration else 0
                total_audio_duration += audio_duration if audio_duration else 0
                
            else:
                print(f"   ❌ 分析失败: {result.stderr}")
                
        except Exception as e:
            print(f"   ❌ 处理出错: {e}")
    
    print(f"\n📊 总计:")
    print(f"   📹 总视频时长: {total_video_duration:.3f}秒")
    print(f"   🔊 总音频时长: {total_audio_duration:.3f}秒")
    print(f"   📊 差异: {abs(total_video_duration - total_audio_duration):.3f}秒")
    
    if abs(total_video_duration - total_audio_duration) > 1:
        print(f"\n💡 分析结论:")
        print(f"   原始视频文件就存在音视频时长不匹配问题")
        print(f"   需要使用填充音频或截断视频的方式来修复")

if __name__ == "__main__":
    diagnose_videos()
