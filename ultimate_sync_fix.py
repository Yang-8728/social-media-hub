#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
终极音频同步修复方案
"""

import os
from pathlib import Path
import subprocess

def ultimate_sync_fix():
    """终极音频同步修复方案"""
    print("🎥 终极音频同步修复方案")
    print("=" * 35)
    
    # 获取前5个视频文件测试
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))[:5]
    
    print(f"📹 测试5个视频文件:")
    for i, video in enumerate(video_files, 1):
        size_mb = video.stat().st_size / (1024*1024)
        print(f"   {i}. {video.name} ({size_mb:.1f}MB)")
    
    # 创建临时目录
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    # 创建文件列表
    list_file = temp_dir / "ultimate_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace("\\", "\\\\")
            f.write(f"file '{abs_path}'\n")
    
    # FFmpeg路径
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    output_file = "ultimate_sync_fixed.mp4"
    
    # 删除已存在的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"🗑️ 删除旧文件: {output_file}")
    
    # 终极修复方案：强制音视频同步
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c:v", "copy",                # 视频保持原始编码
        "-c:a", "aac",                 # 音频重新编码
        "-ar", "44100",                # 音频采样率
        "-ac", "2",                    # 双声道
        "-b:a", "128k",                # 音频码率
        "-async", "1",                 # 强制音频同步到视频
        "-vsync", "vfr",               # 可变帧率处理
        "-avoid_negative_ts", "make_zero",  # 修复负时间戳
        "-fflags", "+genpts",          # 重新生成时间戳
        "-max_muxing_queue_size", "9999",   # 增大缓冲区
        output_file
    ]
    
    print(f"\n🔄 使用终极同步修复...")
    print(f"💡 关键参数: -async 1 强制音频同步到视频")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\n✅ 终极同步修复成功!")
                print(f"📊 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
                
                # 验证修复效果
                print(f"\n🔍 验证修复效果...")
                verify_cmd = [
                    "tools/ffmpeg/bin/ffprobe.exe",
                    "-v", "quiet",
                    "-print_format", "json",
                    "-show_format",
                    "-show_streams",
                    output_file
                ]
                
                verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
                if verify_result.returncode == 0:
                    import json
                    info = json.loads(verify_result.stdout)
                    video_duration = None
                    audio_duration = None
                    
                    for stream in info.get("streams", []):
                        if stream.get("codec_type") == "video":
                            video_duration = float(stream.get("duration", 0))
                        elif stream.get("codec_type") == "audio":
                            audio_duration = float(stream.get("duration", 0))
                    
                    if video_duration and audio_duration:
                        print(f"   📊 视频时长: {video_duration:.2f}秒")
                        print(f"   📊 音频时长: {audio_duration:.2f}秒")
                        duration_diff = abs(video_duration - audio_duration)
                        if duration_diff < 0.1:
                            print(f"   ✅ 音视频完美同步! (差异: {duration_diff:.3f}秒)")
                        else:
                            print(f"   ⚠️ 仍有轻微差异 (差异: {duration_diff:.3f}秒)")
                    
                    print(f"\n🎯 终极修复方案特点:")
                    print(f"   ✅ -async 1 强制音频同步")
                    print(f"   ✅ -vsync vfr 可变帧率处理")
                    print(f"   ✅ 时间戳完全重建")
                    print(f"   ✅ 大缓冲区防止丢失")
                
                return True
            else:
                print(f"\n❌ 输出文件未创建")
                return False
        else:
            print(f"\n❌ FFmpeg执行失败，返回码: {result.returncode}")
            print(f"错误输出: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False
    finally:
        # 清理临时文件
        if list_file.exists():
            list_file.unlink()

if __name__ == "__main__":
    ultimate_sync_fix()
