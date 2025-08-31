#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复音频同步问题的正确方案
结合原项目分批方法 + 音视频同步修复
"""

import os
from pathlib import Path
import subprocess

def fixed_sync_merge():
    """修复音频同步问题的合并方案"""
    print("🎥 音频同步修复合并方案")
    print("=" * 35)
    
    # 获取前5个视频文件测试
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))[:5]
    
    print(f"📹 测试5个视频文件:")
    for i, video in enumerate(video_files, 1):
        size_mb = video.stat().st_size / (1024*1024)
        print(f"   {i}. {video.name} ({size_mb:.1f}MB)")
    
    # 创建临时目录
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    # 创建文件列表
    list_file = temp_dir / "sync_fix_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace("\\", "\\\\")
            f.write(f"file '{abs_path}'\n")
    
    print(f"\n📝 创建文件列表: {list_file}")
    
    # FFmpeg路径
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    output_file = "test_sync_fixed.mp4"
    
    # 删除已存在的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"🗑️ 删除旧文件: {output_file}")
    
    # 关键修复方案：重新编码音频但保持视频copy
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c:v", "copy",          # 视频保持原始编码（快速）
        "-c:a", "aac",           # 音频重新编码为AAC
        "-ar", "44100",          # 统一音频采样率
        "-ac", "2",              # 双声道
        "-b:a", "128k",          # 音频码率
        "-avoid_negative_ts", "make_zero",  # 修复时间戳
        "-fflags", "+genpts",    # 重新生成时间戳
        "-shortest",             # 确保音视频长度一致
        output_file
    ]
    
    print(f"\n🔄 使用音频同步修复方案...")
    print(f"💡 方法: 视频copy + 音频重编码 + 时间戳修复")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\n✅ 同步修复合并成功!")
                print(f"📊 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
                
                print(f"\n🎯 同步修复方案特点:")
                print(f"   ✅ 视频流直接复制（保持质量）")
                print(f"   ✅ 音频重新编码（修复同步）")
                print(f"   ✅ 时间戳修复")
                print(f"   ✅ 确保音视频长度一致")
                
                # 验证修复效果
                print(f"\n🔍 验证修复效果...")
                verify_cmd = [
                    "tools/ffmpeg/bin/ffprobe.exe",
                    "-v", "quiet",
                    "-print_format", "json",
                    "-show_format",
                    "-show_streams",
                    output_file
                ]
                
                verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
                if verify_result.returncode == 0:
                    import json
                    info = json.loads(verify_result.stdout)
                    video_duration = None
                    audio_duration = None
                    
                    for stream in info.get("streams", []):
                        if stream.get("codec_type") == "video":
                            video_duration = float(stream.get("duration", 0))
                        elif stream.get("codec_type") == "audio":
                            audio_duration = float(stream.get("duration", 0))
                    
                    if video_duration and audio_duration:
                        print(f"   📊 视频时长: {video_duration:.2f}秒")
                        print(f"   📊 音频时长: {audio_duration:.2f}秒")
                        duration_diff = abs(video_duration - audio_duration)
                        if duration_diff < 0.1:
                            print(f"   ✅ 音视频同步良好 (差异: {duration_diff:.3f}秒)")
                        else:
                            print(f"   ⚠️ 可能仍有同步问题 (差异: {duration_diff:.3f}秒)")
                
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
    fixed_sync_merge()
