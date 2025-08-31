#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的高级视频合并测试
"""

import os
from pathlib import Path
import subprocess

def simple_merge_test():
    """简单的视频合并测试"""
    print("🎥 简单高级合并测试")
    print("=" * 30)
    
    # 获取前3个视频文件
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))[:3]
    
    if not video_files:
        print("❌ 未找到视频文件")
        return
    
    print(f"📹 测试合并 {len(video_files)} 个视频:")
    for i, video in enumerate(video_files, 1):
        size_mb = video.stat().st_size / (1024*1024)
        print(f"   {i}. {video.name} ({size_mb:.1f}MB)")
    
    # 创建输出文件名
    output_file = "test_merge.mp4"
    
    # 删除已存在的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"🗑️ 删除旧文件: {output_file}")
    
    # 创建临时文件列表
    temp_list = "temp_list.txt"
    with open(temp_list, 'w', encoding='utf-8') as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace('\\', '/')
            f.write(f"file '{abs_path}'\n")
    
    print(f"📝 创建文件列表: {temp_list}")
    
    # 显示文件列表内容
    print("📄 文件列表内容:")
    with open(temp_list, 'r', encoding='utf-8') as f:
        for line in f:
            print(f"   {line.strip()}")
    
    # FFmpeg命令
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
    
    print(f"\\n🔄 开始合并...")
    print(f"💡 使用快速编码模式")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\\n✅ 合并成功!")
                print(f"📊 输出文件: {output_file} ({size_mb:.1f}MB)")
                return True
            else:
                print(f"\\n❌ 输出文件未创建")
                return False
        else:
            print(f"\\n❌ FFmpeg执行失败，返回码: {result.returncode}")
            print(f"错误信息: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(temp_list):
            os.remove(temp_list)

if __name__ == "__main__":
    simple_merge_test()
