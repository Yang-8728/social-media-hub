#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
换5个不同的视频测试合并
"""

import os
from pathlib import Path
import subprocess

def test_different_5_videos():
    """测试不同的5个视频"""
    print("🎥 测试不同的5个视频合并")
    print("=" * 35)
    
    # 获取所有视频文件
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    all_videos = sorted(list(source_folder.glob("*.mp4")))
    
    print(f"📁 总共找到 {len(all_videos)} 个视频文件")
    
    # 选择第6-10个视频（跳过前5个）
    if len(all_videos) >= 10:
        video_files = all_videos[5:10]  # 第6到第10个
        print(f"📹 选择第6-10个视频文件:")
    else:
        # 如果视频不够，选择最后5个
        video_files = all_videos[-5:]
        print(f"📹 选择最后5个视频文件:")
    
    for i, video in enumerate(video_files, 1):
        size_mb = video.stat().st_size / (1024*1024)
        print(f"   {i}. {video.name} ({size_mb:.1f}MB)")
    
    # 创建临时目录
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    # 创建文件列表
    list_file = temp_dir / "different_5_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace("\\", "\\\\")
            f.write(f"file '{abs_path}'\n")
    
    print(f"\n📝 创建文件列表: {list_file}")
    
    # FFmpeg路径
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    output_file = "test_different_5.mp4"
    
    # 删除已存在的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"🗑️ 删除旧文件: {output_file}")
    
    # 使用最简单的方法先测试
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",  # 最简单的copy模式
        output_file
    ]
    
    print(f"\n🔄 使用最简单的copy模式测试...")
    print(f"💡 如果copy模式有问题，再用重编码模式")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\n✅ Copy模式合并成功!")
                print(f"📊 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
                print(f"\n💡 请测试这个文件是否还有卡顿问题")
                print(f"   如果copy模式正常，说明重编码过程引入了问题")
                print(f"   如果copy模式也卡，说明是原始视频文件的问题")
                
                return True
            else:
                print(f"\n❌ 输出文件未创建")
        else:
            print(f"\n❌ Copy模式失败: {result.stderr}")
            print(f"\n🔄 尝试重编码模式...")
            
            # Copy模式失败，尝试重编码
            return test_with_reencoding(video_files, temp_dir)
            
    except Exception as e:
        print(f"❌ Copy模式出错: {e}")
        return test_with_reencoding(video_files, temp_dir)
    finally:
        if list_file.exists():
            list_file.unlink()

def test_with_reencoding(video_files, temp_dir):
    """重编码模式测试"""
    print(f"🔄 使用重编码模式...")
    
    # 创建文件列表
    list_file = temp_dir / "reencoding_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace("\\", "\\\\")
            f.write(f"file '{abs_path}'\n")
    
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    output_file = "test_reencoded_5.mp4"
    
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # 重编码模式，强制音视频同步
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
        output_file
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\n✅ 重编码模式成功!")
                print(f"📊 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
                
                return True
            else:
                print(f"\n❌ 重编码输出文件未创建")
        else:
            print(f"\n❌ 重编码模式失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 重编码模式出错: {e}")
    finally:
        if list_file.exists():
            list_file.unlink()
    
    return False

if __name__ == "__main__":
    test_different_5_videos()
