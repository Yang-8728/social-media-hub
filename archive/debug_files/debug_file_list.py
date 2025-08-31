#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试文件列表创建问题
"""

import os
from pathlib import Path

def debug_file_list():
    """调试文件列表创建"""
    print("🔍 调试文件列表创建")
    print("=" * 30)
    
    # 获取视频文件
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))
    
    print(f"📁 源文件夹: {source_folder}")
    print(f"📁 文件夹存在: {source_folder.exists()}")
    print(f"📹 找到视频文件: {len(video_files)}")
    
    if not video_files:
        print("❌ 没有找到视频文件")
        return
    
    # 显示前3个文件
    print("\n📄 前3个视频文件:")
    for i, video in enumerate(video_files[:3], 1):
        print(f"   {i}. {video}")
        print(f"      存在: {video.exists()}")
        print(f"      绝对路径: {video.absolute()}")
    
    # 创建文件列表
    temp_list = "debug_list.txt"
    print(f"\n📝 创建文件列表: {temp_list}")
    
    try:
        with open(temp_list, 'w', encoding='utf-8') as f:
            for video in video_files[:3]:  # 只用前3个测试
                abs_path = os.path.abspath(video).replace('\\', '/')
                line = f"file '{abs_path}'"
                f.write(line + '\n')
                print(f"   写入: {line}")
        
        print(f"✅ 文件列表创建成功")
        
        # 检查文件是否创建
        if os.path.exists(temp_list):
            print(f"✅ 文件存在: {temp_list}")
            
            # 读取并显示内容
            print("\n📄 文件内容:")
            with open(temp_list, 'r', encoding='utf-8') as f:
                content = f.read()
                print(repr(content))
                
            print("\n📄 逐行显示:")
            with open(temp_list, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    print(f"   第{i}行: {repr(line)}")
        else:
            print(f"❌ 文件未创建: {temp_list}")
            
    except Exception as e:
        print(f"❌ 创建文件时出错: {e}")
    
    # 测试简单的FFmpeg命令
    print(f"\n🔧 测试FFmpeg...")
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    
    if os.path.exists(ffmpeg_exe):
        print(f"✅ FFmpeg存在: {ffmpeg_exe}")
        
        # 测试简单命令
        cmd = f'{ffmpeg_exe} -f concat -safe 0 -i {temp_list} -c copy test_debug.mp4'
        print(f"🧪 测试命令: {cmd}")
        
    else:
        print(f"❌ FFmpeg不存在: {ffmpeg_exe}")

if __name__ == "__main__":
    debug_file_list()
