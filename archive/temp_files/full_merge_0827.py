#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的高级视频合并工具 - 合并所有48个视频
"""

import os
from pathlib import Path
import subprocess

def full_merge_0827():
    """合并2025-08-27的所有48个视频"""
    print("🎥 完整高级合并工具 - 2025-08-27全部视频")
    print("=" * 50)
    
    # 获取所有视频文件
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))
    
    if not video_files:
        print("❌ 未找到视频文件")
        return
    
    print(f"📹 准备合并 {len(video_files)} 个视频")
    
    # 计算总大小
    total_size = sum(video.stat().st_size for video in video_files) / (1024*1024)
    print(f"📊 原始总大小: {total_size:.1f}MB")
    
    # 显示前5个和后5个文件
    print("📄 视频文件列表:")
    for i, video in enumerate(video_files[:5], 1):
        size_mb = video.stat().st_size / (1024*1024)
        print(f"   {i}. {video.name} ({size_mb:.1f}MB)")
    
    if len(video_files) > 10:
        print(f"   ... 中间 {len(video_files) - 10} 个文件 ...")
        for i, video in enumerate(video_files[-5:], len(video_files) - 4):
            size_mb = video.stat().st_size / (1024*1024)
            print(f"   {i}. {video.name} ({size_mb:.1f}MB)")
    
    # 创建输出文件名
    output_file = "output.mp4"
    #os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # 删除已存在的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"🗑️ 删除旧文件: {output_file}")
    
    # 创建临时文件列表
    temp_list = "temp_full_list.txt"
    with open(temp_list, 'w', encoding='utf-8') as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace('\\', '/')
            f.write(f"file '{abs_path}'\n")
    
    print(f"📝 创建文件列表: {temp_list}")
    print(f"💾 文件列表包含 {len(video_files)} 个视频路径")
    
    # FFmpeg命令 - 使用原项目的高级参数
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0", 
        "-i", temp_list,
        # === 高级修复参数 ===
        "-c:v", "libx264",              # H.264编码
        "-preset", "slow",              # 慢速编码，质量更好
        "-crf", "20",                   # 更高质量
        "-vf", "fps=30,scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black",  # 强制30fps + 统一分辨率
        "-vsync", "vfr",                # 可变帧率处理
        "-r", "30",                     # 输出30fps
        "-pix_fmt", "yuv420p",          # 标准像素格式
        "-c:a", "aac",                  # 音频AAC编码
        "-b:a", "128k",                 # 音频码率
        "-ar", "44100",                 # 音频采样率
        "-ac", "2",                     # 双声道
        "-avoid_negative_ts", "make_zero",  # 修复时间戳
        "-fflags", "+genpts",           # 重新生成时间戳
        "-max_muxing_queue_size", "9999",   # 增大缓冲区
        "-err_detect", "ignore_err",    # 忽略错误继续处理
        output_file
    ]
    
    print(f"\\n🔄 开始高级合并...")
    print(f"💡 使用原项目的advanced_fix_video.py参数")
    print(f"💡 重新编码 + 统一分辨率 + 音频修复")
    print(f"⏳ 处理48个视频，预计需要较长时间...")
    print(f"\\n🎬 开始处理...")
    
    try:
        # 使用实时输出
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding='utf-8',
            errors='replace'
        )
        
        # 实时显示进度
        frame_count = 0
        for line in process.stdout:
            if "frame=" in line and "fps=" in line:
                frame_count += 1
                if frame_count % 50 == 0:  # 每50帧显示一次
                    print(f"🎞️ {line.strip()}")
            elif "time=" in line and "bitrate=" in line:
                print(f"⏱️ {line.strip()}")
            elif "error" in line.lower():
                print(f"⚠️ {line.strip()}")
        
        process.wait()
        
        if process.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\\n✅ 全部48个视频合并成功!")
                print(f"📊 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
                print(f"\\n🎯 高级修复特点:")
                print(f"   ✅ 重新编码 (彻底解决兼容性)")
                print(f"   ✅ 统一30fps帧率")
                print(f"   ✅ 统一720x1280分辨率")
                print(f"   ✅ AAC音频编码")
                print(f"   ✅ 修复时间戳问题")
                print(f"   ✅ 统一像素格式")
                return True
            else:
                print(f"\\n❌ 输出文件未创建")
                return False
        else:
            print(f"\\n❌ FFmpeg执行失败，返回码: {process.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(temp_list):
            os.remove(temp_list)
            print(f"🧹 清理临时文件: {temp_list}")

if __name__ == "__main__":
    full_merge_0827()
