#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决音频重叠问题的方案
强制音视频严格对齐，避免音频延续到下一个视频
"""

import os
from pathlib import Path
import subprocess

def fix_audio_overlap():
    """解决音频重叠问题"""
    print("🎥 解决音频重叠问题")
    print("=" * 30)
    
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
    list_file = temp_dir / "overlap_fix_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace("\\", "\\\\")
            f.write(f"file '{abs_path}'\n")
    
    # FFmpeg路径
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    output_file = "audio_overlap_fixed.mp4"
    
    # 删除已存在的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"🗑️ 删除旧文件: {output_file}")
    
    # 关键方案：使用-shortest确保音视频严格对齐
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-ar", "44100",
        "-ac", "2",
        "-b:a", "128k",
        "-shortest",                    # 关键：以最短流为准
        "-avoid_negative_ts", "make_zero",
        "-fflags", "+genpts",
        "-af", "apad",                  # 音频填充，确保每段音频长度一致
        "-video_track_timescale", "30000",  # 统一时间基准
        output_file
    ]
    
    print(f"\n🔄 使用音频重叠修复方案...")
    print(f"💡 关键: -shortest + apad 确保音视频严格对齐")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\n✅ 音频重叠修复成功!")
                print(f"📊 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
                
                print(f"\n🎯 修复方案特点:")
                print(f"   ✅ -shortest 强制音视频同长度")
                print(f"   ✅ apad 音频填充避免断断续续")
                print(f"   ✅ 统一时间基准")
                print(f"   ✅ 避免音频延续到下个视频")
                
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

def fix_with_individual_processing():
    """另一种方案：单独处理每个视频后再合并"""
    print("🎥 方案2: 单独处理每个视频后合并")
    print("=" * 40)
    
    # 获取前3个视频文件测试
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))[:3]
    
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    processed_files = []
    
    # 第一步：单独处理每个视频，确保音视频严格对齐
    for i, video in enumerate(video_files, 1):
        print(f"\n📹 处理视频 {i}: {video.name}")
        
        processed_file = temp_dir / f"processed_{i}.mp4"
        
        # 单独处理每个视频，强制音视频长度一致
        cmd = [
            ffmpeg_exe, "-y",
            "-i", str(video),
            "-c:v", "libx264",
            "-preset", "fast", 
            "-crf", "23",
            "-c:a", "aac",
            "-ar", "44100",
            "-ac", "2",
            "-b:a", "128k",
            "-shortest",                # 关键：音视频以短的为准
            "-avoid_negative_ts", "make_zero",
            "-fflags", "+genpts",
            str(processed_file)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0 and processed_file.exists():
                size_mb = processed_file.stat().st_size / (1024*1024)
                print(f"   ✅ 处理成功 ({size_mb:.1f}MB)")
                processed_files.append(processed_file)
            else:
                print(f"   ❌ 处理失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"   ❌ 处理出错: {e}")
            return False
    
    # 第二步：合并已处理的视频
    print(f"\n🔗 合并 {len(processed_files)} 个已处理的视频...")
    
    list_file = temp_dir / "processed_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for pf in processed_files:
            abs_path = os.path.abspath(pf).replace("\\", "\\\\")
            f.write(f"file '{abs_path}'\n")
    
    output_file = "individual_processed.mp4"
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # 简单合并已处理的视频
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",  # 已处理过，可以直接copy
        output_file
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024*1024)
            print(f"\n✅ 个别处理方案成功!")
            print(f"📊 输出文件: {output_file}")
            print(f"📊 文件大小: {size_mb:.1f}MB")
            
            print(f"\n🎯 个别处理方案特点:")
            print(f"   ✅ 每个视频单独处理音视频对齐")
            print(f"   ✅ 消除原始视频的时间戳问题")
            print(f"   ✅ 最后简单合并不会引入新问题")
            
            return True
        else:
            print(f"\n❌ 合并失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 合并出错: {e}")
        return False
    finally:
        # 清理临时文件
        if list_file.exists():
            list_file.unlink()
        for pf in processed_files:
            if pf.exists():
                pf.unlink()

if __name__ == "__main__":
    print("选择方案:")
    print("1. 音频重叠修复方案")
    print("2. 个别处理方案")
    
    # 先试方案1
    fix_audio_overlap()
    
    print("\n" + "="*50)
    
    # 再试方案2
    fix_with_individual_processing()
