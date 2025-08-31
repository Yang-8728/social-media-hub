#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的完整视频合并工具 - 使用基本参数
"""

import os
from pathlib import Path
import subprocess

def simple_full_merge():
    """简化版的完整视频合并"""
    print("🎥 简化完整合并工具 - 2025-08-27全部视频")
    print("=" * 50)
    
    # 获取所有视频文件
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))
    
    if not video_files:
        print("❌ 未找到视频文件")
        return
    
    print(f"📹 准备合并 {len(video_files)} 个视频")
    
    # 创建输出文件名
    output_file = "output.mp4"
    
    # 删除已存在的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"🗑️ 删除旧文件: {output_file}")
    
    # 创建临时文件列表
    temp_list = "temp_list.txt"
    with open(temp_list, 'w', encoding='utf-8') as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace('\\', '/')
            f.write(f"file '{abs_path}'\\n")
    
    print(f"📝 创建文件列表: {temp_list}")
    
    # 简化的FFmpeg命令
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0", 
        "-i", temp_list,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        output_file
    ]
    
    print(f"\\n🔄 开始简化合并...")
    print(f"💡 使用基本编码参数")
    
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

if __name__ == "__main__":
    simple_full_merge()
