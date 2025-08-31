#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
彻底解决分辨率统一时的卡帧和音频同步问题
"""

import os
from pathlib import Path
import subprocess

def fix_frame_stutter():
    """解决分辨率统一时的卡帧问题"""
    print("🎥 解决分辨率统一时的卡帧问题")
    print("=" * 35)
    
    # 获取前3个视频文件测试
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))[:3]
    
    print(f"📹 测试3个视频文件:")
    for i, video in enumerate(video_files, 1):
        size_mb = video.stat().st_size / (1024*1024)
        print(f"   {i}. {video.name} ({size_mb:.1f}MB)")
    
    # 先检查每个视频的分辨率
    ffprobe_exe = "tools/ffmpeg/bin/ffprobe.exe"
    print(f"\n🔍 检查每个视频的分辨率:")
    
    for i, video in enumerate(video_files, 1):
        cmd = [
            ffprobe_exe,
            "-v", "quiet",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate",
            "-of", "csv=p=0",
            str(video)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                width, height, fps = result.stdout.strip().split(',')
                print(f"   {i}. {width}x{height} @ {fps} fps")
            else:
                print(f"   {i}. 获取信息失败")
        except:
            print(f"   {i}. 检查出错")
    
    # 创建临时目录
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    # 创建文件列表
    list_file = temp_dir / "frame_fix_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace("\\", "\\\\")
            f.write(f"file '{abs_path}'\n")
    
    # FFmpeg路径
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    output_file = "frame_stutter_fixed.mp4"
    
    # 删除已存在的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"\n🗑️ 删除旧文件: {output_file}")
    
    # 关键解决方案：不统一分辨率，保持原始比例
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-r", "30",                     # 统一帧率，但不改变分辨率
        "-c:a", "aac",
        "-ar", "44100",
        "-ac", "2",
        "-b:a", "128k",
        "-vsync", "cfr",                # 恒定帧率，避免卡帧
        "-async", "1",                  # 音频同步
        "-avoid_negative_ts", "make_zero",
        "-fflags", "+genpts",
        output_file
    ]
    
    print(f"\n🔄 方案1: 不统一分辨率，只统一帧率...")
    print(f"💡 避免添加黑边造成的卡帧问题")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\n✅ 方案1成功!")
                print(f"📊 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
                print(f"💡 此方案保持原始分辨率，避免黑边卡帧")
                
                return True
            else:
                print(f"\n❌ 输出文件未创建")
        else:
            print(f"\n❌ 方案1失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 方案1出错: {e}")
    finally:
        if list_file.exists():
            list_file.unlink()
    
    return False

def fix_with_smooth_scaling():
    """方案2：平滑缩放，避免突然的分辨率变化"""
    print(f"\n🎥 方案2: 平滑缩放避免卡帧")
    print("=" * 30)
    
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))[:3]
    
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    list_file = temp_dir / "smooth_scale_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace("\\", "\\\\")
            f.write(f"file '{abs_path}'\n")
    
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    output_file = "smooth_scaling_fixed.mp4"
    
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # 使用更平滑的缩放算法
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-vf", "scale=720:1280:force_original_aspect_ratio=decrease:flags=lanczos,pad=720:1280:(ow-iw)/2:(oh-ih)/2:color=black,fps=30",
        "-c:a", "aac",
        "-ar", "44100",
        "-ac", "2", 
        "-b:a", "128k",
        "-vsync", "cfr",
        "-async", "1",
        "-avoid_negative_ts", "make_zero",
        "-fflags", "+genpts",
        "-force_key_frames", "expr:gte(t,n_forced*2)",  # 强制关键帧，避免卡帧
        output_file
    ]
    
    print(f"🔄 使用平滑缩放算法...")
    print(f"💡 关键: lanczos缩放 + 强制关键帧")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\n✅ 方案2成功!")
                print(f"📊 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
                print(f"💡 此方案使用平滑缩放，减少卡帧")
                
                return True
            else:
                print(f"\n❌ 输出文件未创建")
        else:
            print(f"\n❌ 方案2失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 方案2出错: {e}")
    finally:
        if list_file.exists():
            list_file.unlink()
    
    return False

if __name__ == "__main__":
    print("🔧 解决分辨率统一时的卡帧和音频同步问题")
    print("="*50)
    
    # 先试方案1：不统一分辨率
    success1 = fix_frame_stutter()
    
    if not success1:
        # 方案1失败则试方案2：平滑缩放
        fix_with_smooth_scaling()
    
    print(f"\n💡 问题分析:")
    print(f"   问题根源: 添加黑边时的分辨率变化造成帧率不稳定")
    print(f"   解决思路: 要么不统一分辨率，要么使用更平滑的缩放")
