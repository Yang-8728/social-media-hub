#!/usr/bin/env python3
"""
合并除了标准化视频外的其他视频进行对比测试
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime

def merge_original_videos():
    """合并原始视频（不包括标准化版本）"""
    video_dir = Path('videos/downloads/ai_vanvan/2025-09-01')
    ffmpeg_path = Path('tools/ffmpeg/bin/ffmpeg.exe')
    
    # 获取所有mp4文件并排序
    all_videos = list(video_dir.glob('*.mp4'))
    all_videos.sort()
    
    # 排除标准化视频、修复版本和有问题的视频
    excluded_patterns = ['_std.mp4', '_fixed.mp4', '_normalized.mp4', '_aac_fixed.mp4']
    excluded_videos = ['2025-08-20_15-43-46_UTC.mp4']  # 排除有问题的视频
    original_videos = []
    
    for video in all_videos:
        # 检查是否匹配排除模式
        if any(pattern in video.name for pattern in excluded_patterns):
            continue
        # 检查是否是被排除的具体视频
        if video.name in excluded_videos:
            continue
        original_videos.append(video)
    
    print(f"找到 {len(original_videos)} 个原始视频")
    print(f"排除了标准化版本、修复版本和有问题的视频")
    
    # 显示将要合并的视频
    print("\n将要合并的视频:")
    for i, video in enumerate(original_videos, 1):
        size_mb = video.stat().st_size / (1024 * 1024)
        print(f"  {i:2d}. {video.name} ({size_mb:.2f} MB)")
    
    if len(original_videos) < 2:
        print("❌ 视频数量不足，无法合并")
        return
    
    # 创建合并输出目录
    output_dir = Path('videos/merged')
    output_dir.mkdir(exist_ok=True)
    
    # 生成输出文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f'merged_original_videos_{timestamp}.mp4'
    
    # 创建临时文件列表
    temp_list = video_dir / 'temp_merge_list.txt'
    
    try:
        # 写入文件列表
        with open(temp_list, 'w', encoding='utf-8') as f:
            for video in original_videos:
                # 使用绝对路径避免路径问题
                f.write(f"file '{video.absolute()}'\n")
        
        print(f"\n📝 创建了临时文件列表: {temp_list}")
        
        # FFmpeg合并命令
        cmd = [
            str(ffmpeg_path),
            '-f', 'concat',
            '-safe', '0',
            '-i', str(temp_list),
            '-c', 'copy',  # 直接复制流，不重新编码
            str(output_file),
            '-y'  # 覆盖输出文件
        ]
        
        print(f"\n🔧 开始合并 {len(original_videos)} 个视频...")
        print(f"输出文件: {output_file}")
        
        # 执行合并
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            if output_file.exists():
                size_mb = output_file.stat().st_size / (1024 * 1024)
                print(f"✅ 合并成功!")
                print(f"📁 输出文件: {output_file}")
                print(f"📊 文件大小: {size_mb:.2f} MB")
                
                # 获取合并视频信息
                get_merged_info(output_file)
            else:
                print("❌ 合并失败：输出文件不存在")
        else:
            print(f"❌ 合并失败:")
            print(f"错误信息: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 合并过程出错: {e}")
        
    finally:
        # 清理临时文件
        if temp_list.exists():
            temp_list.unlink()
            print(f"🗑️  清理临时文件: {temp_list}")

def get_merged_info(video_path):
    """获取合并后视频的信息"""
    ffprobe_path = Path('tools/ffmpeg/bin/ffprobe.exe')
    
    try:
        # 获取基本信息
        cmd = [
            str(ffprobe_path), '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', str(video_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            import json
            info = json.loads(result.stdout)
            
            format_info = info.get('format', {})
            streams = info.get('streams', [])
            
            video_stream = next((s for s in streams if s.get('codec_type') == 'video'), {})
            audio_stream = next((s for s in streams if s.get('codec_type') == 'audio'), {})
            
            print(f"\n📹 合并视频信息:")
            print(f"   时长: {float(format_info.get('duration', 0)):.2f} 秒")
            print(f"   总比特率: {format_info.get('bit_rate', 'N/A')} bps")
            print(f"   视频编码: {video_stream.get('codec_name', 'N/A')}")
            print(f"   分辨率: {video_stream.get('width')}x{video_stream.get('height')}")
            print(f"   音频编码: {audio_stream.get('codec_name', 'N/A')}")
            print(f"   音频比特率: {audio_stream.get('bit_rate', 'N/A')} bps")
            
    except Exception as e:
        print(f"⚠️  无法获取视频信息: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("原始视频合并测试 (排除有问题的视频)")
    print("=" * 60)
    merge_original_videos()
