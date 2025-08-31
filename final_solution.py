#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终解决方案：强制音视频时长匹配
"""

import os
from pathlib import Path
import subprocess

def final_solution():
    """最终解决方案：强制音视频时长匹配"""
    print("🎥 最终解决方案：强制音视频时长匹配")
    print("=" * 45)
    
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
    list_file = temp_dir / "final_solution_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace("\\", "\\\\")
            f.write(f"file '{abs_path}'\n")
    
    # FFmpeg路径
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    output_file = "final_solution.mp4"
    
    # 删除已存在的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"🗑️ 删除旧文件: {output_file}")
    
    # 最终解决方案：使用filter_complex确保音视频完全匹配
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c:v", "libx264",             # 重新编码视频确保一致性
        "-preset", "fast",             # 快速编码
        "-crf", "23",                  # 合理质量
        "-r", "30",                    # 统一帧率
        "-c:a", "aac",                 # 重新编码音频
        "-ar", "44100",                # 统一采样率
        "-ac", "2",                    # 双声道
        "-b:a", "128k",                # 音频码率
        "-af", "aresample=async=1000", # 音频重采样，强制同步
        "-vsync", "cfr",               # 恒定帧率
        "-avoid_negative_ts", "make_zero",
        "-fflags", "+genpts",
        output_file
    ]
    
    print(f"\n🔄 使用最终解决方案...")
    print(f"💡 关键: 重新编码音视频 + 强制同步 + 统一参数")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024*1024)
                print(f"\n✅ 最终解决方案成功!")
                print(f"📊 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
                
                # 验证最终效果
                print(f"\n🔍 验证最终效果...")
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
                            print(f"   🎉 完美解决音视频同步! (差异: {duration_diff:.3f}秒)")
                            print(f"\n✅ 这个方案可以应用到全部48个视频!")
                        else:
                            print(f"   📊 差异: {duration_diff:.3f}秒")
                    
                    print(f"\n🎯 最终方案特点:")
                    print(f"   ✅ 完全重新编码（解决兼容性）")
                    print(f"   ✅ 音频重采样强制同步")
                    print(f"   ✅ 统一视频参数")
                    print(f"   ✅ 恒定帧率")
                
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
    final_solution()
