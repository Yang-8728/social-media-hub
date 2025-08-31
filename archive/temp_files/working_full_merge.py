#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正确的全量视频合并工具
"""

import os
from pathlib import Path
import subprocess

def working_full_merge():
    """正确的全量合并工具"""
    print("🎥 全量视频合并工具 - 修复版")
    print("=" * 40)
    
    # 获取所有视频文件
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))
    
    print(f"📹 找到 {len(video_files)} 个视频文件")
    
    # 计算总大小
    total_size = sum(video.stat().st_size for video in video_files) / (1024*1024)
    print(f"📊 原始总大小: {total_size:.1f}MB")
    
    # 创建文件列表
    temp_list = "final_list.txt"
    print(f"📝 创建文件列表: {temp_list}")
    
    with open(temp_list, 'w', encoding='utf-8') as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace('\\', '/')
            f.write(f"file '{abs_path}'\n")
    
    print(f"✅ 文件列表包含 {len(video_files)} 个视频")
    
    # 输出文件
    output_file = "ai_vanvan_0827_complete.mp4"
    
    # 删除已存在的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"🗑️ 删除旧文件: {output_file}")
    
    # FFmpeg命令 - 使用高级参数
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0", 
        "-i", temp_list,
        # 高级参数 - 解决音频同步问题
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-vf", "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black,fps=30",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-ac", "2",
        "-avoid_negative_ts", "make_zero",
        "-fflags", "+genpts",
        output_file
    ]
    
    print(f"\\n🔄 开始合并所有48个视频...")
    print(f"💡 重新编码 + 统一分辨率 + 音频修复")
    print(f"⏳ 预计需要几分钟时间...")
    
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
        
        # 显示进度
        frame_count = 0
        last_time = ""
        for line in process.stdout:
            if "frame=" in line and "fps=" in line:
                frame_count += 1
                if frame_count % 100 == 0:
                    print(f"🎞️ {line.strip()}")
            elif "time=" in line and "bitrate=" in line:
                current_time = line.strip()
                if current_time != last_time:
                    print(f"⏱️ {current_time}")
                    last_time = current_time
            elif "error" in line.lower() or "warning" in line.lower():
                print(f"⚠️ {line.strip()}")
        
        process.wait()
        
        if process.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\\n✅ 全部48个视频合并成功!")
                print(f"📊 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
                print(f"📊 压缩比: {size_mb/total_size:.2f}x")
                
                print(f"\\n🎯 合并特点:")
                print(f"   ✅ 统一分辨率: 720x1280")
                print(f"   ✅ 统一帧率: 30fps") 
                print(f"   ✅ AAC音频编码")
                print(f"   ✅ 修复时间戳和音频同步")
                print(f"   ✅ 兼容性优化")
                
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
    working_full_merge()
