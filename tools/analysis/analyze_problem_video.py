#!/usr/bin/env python3
"""
详细分析第21个问题视频 2025-08-20_15-43-46_UTC.mp4
"""

import os
import json
import subprocess
from pathlib import Path

def analyze_video_details(video_path):
    """详细分析视频"""
    ffprobe_path = Path('tools/ffmpeg/bin/ffprobe.exe')
    
    print(f"=== 详细分析: {video_path.name} ===")
    
    # 基本信息
    size_mb = video_path.stat().st_size / (1024 * 1024)
    print(f"文件大小: {size_mb:.2f} MB")
    
    # 获取详细信息
    cmd = [
        str(ffprobe_path), '-v', 'quiet', '-print_format', 'json',
        '-show_format', '-show_streams', '-show_error', str(video_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            info = json.loads(result.stdout)
            
            # 格式信息
            format_info = info.get('format', {})
            print(f"时长: {float(format_info.get('duration', 0)):.2f} 秒")
            print(f"比特率: {format_info.get('bit_rate', 'N/A')} bps")
            print(f"格式: {format_info.get('format_name', 'N/A')}")
            
            # 流信息
            streams = info.get('streams', [])
            for i, stream in enumerate(streams):
                print(f"\n流 #{i}:")
                print(f"  类型: {stream.get('codec_type')}")
                print(f"  编码: {stream.get('codec_name')}")
                
                if stream.get('codec_type') == 'video':
                    print(f"  分辨率: {stream.get('width')}x{stream.get('height')}")
                    print(f"  帧率: {stream.get('r_frame_rate')}")
                    print(f"  像素格式: {stream.get('pix_fmt')}")
                    print(f"  级别: {stream.get('level')}")
                    
                elif stream.get('codec_type') == 'audio':
                    print(f"  采样率: {stream.get('sample_rate')} Hz")
                    print(f"  声道: {stream.get('channels')}")
                    print(f"  比特率: {stream.get('bit_rate')} bps")
                    print(f"  采样格式: {stream.get('sample_fmt')}")
            
            # 检查错误
            errors = info.get('error', {})
            if errors:
                print(f"\n❌ 发现错误: {errors}")
            
        else:
            print(f"❌ ffprobe失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 分析失败: {e}")

def check_audio_video_sync(video_path):
    """检查音视频同步"""
    ffprobe_path = Path('tools/ffmpeg/bin/ffprobe.exe')
    
    print(f"\n=== 音视频同步检查: {video_path.name} ===")
    
    # 检查音频流持续时间
    cmd_audio = [
        str(ffprobe_path), '-v', 'quiet', '-select_streams', 'a:0',
        '-show_entries', 'stream=duration', '-of', 'csv=p=0', str(video_path)
    ]
    
    # 检查视频流持续时间
    cmd_video = [
        str(ffprobe_path), '-v', 'quiet', '-select_streams', 'v:0',
        '-show_entries', 'stream=duration', '-of', 'csv=p=0', str(video_path)
    ]
    
    try:
        audio_result = subprocess.run(cmd_audio, capture_output=True, text=True)
        video_result = subprocess.run(cmd_video, capture_output=True, text=True)
        
        if audio_result.returncode == 0 and video_result.returncode == 0:
            audio_duration = float(audio_result.stdout.strip())
            video_duration = float(video_result.stdout.strip())
            
            print(f"音频时长: {audio_duration:.3f} 秒")
            print(f"视频时长: {video_duration:.3f} 秒")
            
            diff = abs(audio_duration - video_duration)
            print(f"时长差异: {diff:.3f} 秒")
            
            if diff > 0.1:  # 超过100ms认为有问题
                print(f"⚠️  音视频不同步! 差异: {diff:.3f} 秒")
                return False
            else:
                print("✅ 音视频同步正常")
                return True
        else:
            print("❌ 无法获取音视频时长")
            return False
            
    except Exception as e:
        print(f"❌ 同步检查失败: {e}")
        return False

def check_frame_issues(video_path):
    """检查帧问题"""
    ffmpeg_path = Path('tools/ffmpeg/bin/ffmpeg.exe')
    
    print(f"\n=== 帧完整性检查: {video_path.name} ===")
    
    # 检查是否有损坏的帧
    cmd = [
        str(ffmpeg_path), '-v', 'error', '-i', str(video_path),
        '-f', 'null', '-', '-xerror'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 所有帧完整")
            return True
        else:
            print(f"❌ 发现帧问题:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 帧检查失败: {e}")
        return False

def compare_versions():
    """比较原版和修复版本"""
    today = "2025-09-01"
    video_dir = Path(f'videos/downloads/ai_vanvan/{today}')
    
    base_name = "2025-08-20_15-43-46_UTC"
    original = video_dir / f"{base_name}.mp4"
    fixed = video_dir / f"{base_name}_fixed.mp4"
    normalized = video_dir / f"{base_name}_normalized.mp4"
    aac_fixed = video_dir / f"{base_name}_aac_fixed.mp4"
    
    print("=" * 60)
    print("详细问题分析报告")
    print("=" * 60)
    
    if original.exists():
        print("\n📹 原始视频:")
        analyze_video_details(original)
        audio_sync_ok = check_audio_video_sync(original)
        frame_ok = check_frame_issues(original)
        
        if not audio_sync_ok:
            print("\n🔍 问题诊断: 音视频不同步!")
        if not frame_ok:
            print("\n🔍 问题诊断: 帧损坏或不完整!")
    
    if fixed.exists():
        print("\n🔧 修复版本:")
        analyze_video_details(fixed)
        check_audio_video_sync(fixed)
        check_frame_issues(fixed)
    
    if normalized.exists():
        print("\n📐 标准化版本:")
        analyze_video_details(normalized)
        check_audio_video_sync(normalized)
        check_frame_issues(normalized)
    
    if aac_fixed.exists():
        print("\n🎵 AAC修复版本:")
        analyze_video_details(aac_fixed)
        check_audio_video_sync(aac_fixed)
        check_frame_issues(aac_fixed)
    
    print("\n" + "=" * 60)
    print("总结:")
    print("根据修复版本的存在，原视频可能的问题:")
    print("1. 音视频不同步 (需要 _fixed.mp4)")
    print("2. 编码格式问题 (需要 _normalized.mp4)")
    print("3. 音频编码问题 (需要 _aac_fixed.mp4)")
    print("=" * 60)

if __name__ == "__main__":
    compare_versions()
