#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决音视频时间戳不对齐问题
第一个视频播完停顿时，第二个视频音频就开始播放
"""

import os
from pathlib import Path
import subprocess

def fix_timestamp_alignment():
    """解决音视频时间戳不对齐问题"""
    print("🎥 解决音视频时间戳不对齐问题")
    print("=" * 35)
    
    # 获取前3个视频文件测试
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))[:3]
    
    print(f"📹 测试3个视频文件:")
    for i, video in enumerate(video_files, 1):
        size_mb = video.stat().st_size / (1024*1024)
        print(f"   {i}. {video.name} ({size_mb:.1f}MB)")
    
    # 创建临时目录
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    # 创建文件列表
    list_file = temp_dir / "timestamp_fix_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace("\\", "\\\\")
            f.write(f"file '{abs_path}'\n")
    
    # FFmpeg路径
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    output_file = "timestamp_aligned.mp4"
    
    # 删除已存在的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"🗑️ 删除旧文件: {output_file}")
    
    # 关键解决方案：强制音视频时间戳对齐
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c:v", "copy",                 # 保持视频原样，避免引入新问题
        "-c:a", "aac",                  # 重新编码音频，修复时间戳
        "-ar", "44100",
        "-ac", "2",
        "-b:a", "128k",
        "-shortest",                    # 关键：以最短流为准，避免音频超出视频
        "-avoid_negative_ts", "make_zero",  # 修复负时间戳
        "-fflags", "+genpts",           # 重新生成时间戳
        "-copyts",                      # 保持时间戳连续性
        "-start_at_zero",               # 从零开始时间戳
        output_file
    ]
    
    print(f"\n🔄 方案1: 强制音视频时间戳对齐...")
    print(f"💡 关键: -shortest + 重新生成时间戳")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\n✅ 时间戳对齐成功!")
                print(f"📊 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
                
                # 验证修复效果
                print(f"\n🔍 验证时间戳对齐效果...")
                verify_cmd = [
                    "tools/ffmpeg/bin/ffprobe.exe",
                    "-v", "quiet",
                    "-select_streams", "v:0,a:0",
                    "-show_entries", "stream=duration",
                    "-of", "csv=p=0",
                    output_file
                ]
                
                try:
                    verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
                    if verify_result.returncode == 0:
                        durations = verify_result.stdout.strip().split('\n')
                        if len(durations) >= 2:
                            video_duration = float(durations[0])
                            audio_duration = float(durations[1])
                            print(f"   📊 视频时长: {video_duration:.3f}秒")
                            print(f"   📊 音频时长: {audio_duration:.3f}秒")
                            diff = abs(video_duration - audio_duration)
                            if diff < 0.1:
                                print(f"   ✅ 时间戳完美对齐! (差异: {diff:.3f}秒)")
                            else:
                                print(f"   ⚠️ 仍有差异: {diff:.3f}秒")
                except:
                    print("   ⚠️ 验证过程出错")
                
                return True
            else:
                print(f"\n❌ 输出文件未创建")
        else:
            print(f"\n❌ 时间戳对齐失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 方案1出错: {e}")
    finally:
        if list_file.exists():
            list_file.unlink()
    
    return False

def fix_with_manual_sync():
    """方案2：手动音视频同步"""
    print(f"\n🎥 方案2: 手动音视频同步")
    print("=" * 25)
    
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))[:3]
    
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    list_file = temp_dir / "manual_sync_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace("\\", "\\\\")
            f.write(f"file '{abs_path}'\n")
    
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    output_file = "manual_sync_fixed.mp4"
    
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # 手动同步方案：使用filter确保完全同步
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-filter_complex", "[0:v]fps=30[v];[0:a]aresample=44100,apad[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",                    # 确保音视频同长度
        "-avoid_negative_ts", "make_zero",
        "-fflags", "+genpts",
        output_file
    ]
    
    print(f"🔄 使用filter手动同步...")
    print(f"💡 关键: filter_complex确保帧级别同步")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\n✅ 手动同步成功!")
                print(f"📊 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
                
                return True
            else:
                print(f"\n❌ 输出文件未创建")
        else:
            print(f"\n❌ 手动同步失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 方案2出错: {e}")
    finally:
        if list_file.exists():
            list_file.unlink()
    
    return False

if __name__ == "__main__":
    print("🔧 解决视频播完停顿时下个视频音频已开始的问题")
    print("="*55)
    
    print(f"\n💡 问题分析:")
    print(f"   现象: 第一个视频播完停顿时，第二个视频音频就开始")
    print(f"   原因: 音视频流长度不一致，时间戳不对齐")
    print(f"   解决: 强制音视频同步，以最短流为准")
    
    # 先试方案1：时间戳对齐
    success1 = fix_timestamp_alignment()
    
    if not success1:
        # 方案1失败则试方案2：手动同步
        fix_with_manual_sync()
