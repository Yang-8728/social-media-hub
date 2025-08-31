#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试原项目方法 - 只合并5个视频
"""

import os
from pathlib import Path
import subprocess

def test_5_videos_merge():
    """测试合并5个视频"""
    print("🎥 测试原项目方法 - 5个视频")
    print("=" * 35)
    
    # 获取前5个视频文件
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))[:5]
    
    print(f"📹 选择前5个视频文件:")
    for i, video in enumerate(video_files, 1):
        size_mb = video.stat().st_size / (1024*1024)
        print(f"   {i}. {video.name} ({size_mb:.1f}MB)")
    
    # 创建临时目录
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    # 创建文件列表
    list_file = temp_dir / "test_5_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace("\\", "\\\\")
            f.write(f"file '{abs_path}'\n")
    
    print(f"\n📝 创建文件列表: {list_file}")
    
    # 显示文件列表内容
    print("📄 文件列表内容:")
    with open(list_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            print(f"   {i}. {line.strip()}")
    
    # FFmpeg路径
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    output_file = "test_5_videos_original.mp4"
    
    # 删除已存在的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"🗑️ 删除旧文件: {output_file}")
    
    # 使用原项目的方法：concat demuxer + copy模式
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",  # 关键：直接复制流，不重新编码
        output_file
    ]
    
    print(f"\n🔄 使用原项目方法合并...")
    print(f"💡 方法: concat demuxer + copy模式")
    print(f"📝 命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\n✅ 合并成功!")
                print(f"📊 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
                
                print(f"\n🎯 原项目方法特点:")
                print(f"   ✅ 使用 concat demuxer")
                print(f"   ✅ -c copy (不重新编码)")
                print(f"   ✅ 保持原始编码格式")
                print(f"   ✅ 快速处理")
                
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
    test_5_videos_merge()
