#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级视频合并修复工具 - 解决音频同步和播放问题
基于原项目的advanced_fix_video.py参数
"""

import os
from pathlib import Path
import subprocess
import sys
sys.path.append('src')

def advanced_merge_videos(video_files, output_path):
    """使用高级参数合并视频，彻底解决音频同步问题"""
    
    print("🔧 高级视频合并修复工具")
    print("=" * 50)
    print("💡 基于原项目的advanced_fix_video.py参数")
    print("💡 将重新编码所有视频确保兼容性")
    
    # 创建临时文件列表
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    filelist_path = temp_dir / "advanced_concat_list.txt"
    
    try:
        # 写入文件列表
        with open(filelist_path, 'w', encoding='utf-8') as f:
            for video in video_files:
                abs_path = os.path.abspath(video)
                # Windows路径需要双反斜杠或正斜杠
                abs_path = abs_path.replace('\\', '/')
                f.write(f"file '{abs_path}'\n")
        
        print(f"📝 创建文件列表: {filelist_path}")
        print(f"📹 准备合并 {len(video_files)} 个视频")
        
        # 显示前5个文件
        for i, video in enumerate(video_files[:5], 1):
            size_mb = Path(video).stat().st_size / (1024*1024)
            print(f"   {i}. {Path(video).name} ({size_mb:.1f}MB)")
        if len(video_files) > 5:
            print(f"   ... 及其他 {len(video_files) - 5} 个文件")
        
        # FFmpeg路径
        ffmpeg_paths = [
            "tools/ffmpeg/bin/ffmpeg.exe",
            "ffmpeg"
        ]
        
        ffmpeg_exe = None
        for path in ffmpeg_paths:
            if os.path.exists(path):
                ffmpeg_exe = path
                break
        
        if not ffmpeg_exe:
            ffmpeg_exe = "ffmpeg"
        
        # 使用原项目的高级修复参数进行合并
        cmd = [
            ffmpeg_exe, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(filelist_path),
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
            str(output_path)
        ]
        
        print(f"\\n🔄 开始高级合并...")
        print(f"💡 使用参数: 重新编码 + 统一分辨率 + 音频修复")
        print(f"⏳ 这会比较慢，但能彻底解决问题...")
        
        # 执行FFmpeg命令，显示进度
        print(f"\\n🎬 开始处理...")
        
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
            if "frame=" in line:
                frame_count += 1
                if frame_count % 100 == 0:  # 每100帧显示一次
                    print(f"🎞️ 处理进度: {line.strip()}")
            elif "time=" in line:
                print(f"⏱️ 时间进度: {line.strip()}")
            elif "error" in line.lower() or "warning" in line.lower():
                print(f"⚠️ {line.strip()}")
        
        process.wait()
        
        if process.returncode == 0:
            if os.path.exists(output_path):
                output_size = os.path.getsize(output_path) / (1024*1024)
                print(f"\\n✅ 高级合并成功!")
                print(f"📊 输出文件大小: {output_size:.1f}MB")
                return True
            else:
                print(f"\\n❌ 输出文件未创建")
                return False
        else:
            print(f"\\n❌ FFmpeg执行失败，返回码: {process.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ 合并过程出错: {e}")
        return False
    finally:
        # 清理临时文件
        if filelist_path.exists():
            filelist_path.unlink()

def advanced_fix_0827():
    """使用高级参数合并修复2025-08-27的视频"""
    print("🎥 高级视频合并修复工具")
    print("=" * 50)
    
    # 获取2025-08-27文件夹的所有视频
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))
    
    if not video_files:
        print("❌ 未找到视频文件")
        return
    
    print(f"📁 找到 {len(video_files)} 个视频文件")
    
    # 为了测试，先用前3个视频
    test_videos = video_files[:3]
    print(f"🧪 测试模式: 先合并前3个视频验证效果")
    
    # 创建输出文件
    output_name = "merged_0827_advanced_test.mp4"
    output_path = Path(output_name)
    #output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 删除已存在的输出文件
    if output_path.exists():
        output_path.unlink()
        print(f"🗑️ 删除旧文件: {output_name}")
    
    # 执行高级合并
    video_paths = [str(f) for f in test_videos]
    success = advanced_merge_videos(video_paths, str(output_path))
    
    if success:
        print(f"\\n🎉 高级合并测试完成!")
        print(f"📁 输出文件: {output_path}")
        print(f"💡 这个版本应该彻底解决音频同步问题")
        print(f"💡 如果测试效果好，可以处理全部48个视频")
        
        # 显示文件信息
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024*1024)
            print(f"📊 文件大小: {size_mb:.1f}MB")
            
            print(f"\\n🎯 高级修复特点:")
            print(f"   ✅ 重新编码 (不是copy模式)")
            print(f"   ✅ 统一30fps帧率")
            print(f"   ✅ 统一720x1280分辨率")
            print(f"   ✅ 重新编码音频为AAC")
            print(f"   ✅ 修复时间戳问题")
            print(f"   ✅ 统一像素格式")
        
    else:
        print(f"\\n❌ 高级合并失败")

def main():
    advanced_fix_0827()

if __name__ == "__main__":
    main()
