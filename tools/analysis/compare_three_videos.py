#!/usr/bin/env python3
"""
对比三个特定视频的差异
"""

import subprocess
import json
from pathlib import Path

def get_detailed_info(video_name):
    """获取视频详细信息"""
    video_dir = Path('videos/downloads/ai_vanvan/2025-09-01')
    video_path = video_dir / f"{video_name}.mp4"
    
    if not video_path.exists():
        return None
    
    ffprobe_path = Path('tools/ffmpeg/bin/ffprobe.exe')
    
    cmd = [
        str(ffprobe_path), '-v', 'quiet', '-print_format', 'json',
        '-show_format', '-show_streams', str(video_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            info = json.loads(result.stdout)
            
            # 提取关键信息
            format_info = info.get('format', {})
            streams = info.get('streams', [])
            
            video_stream = next((s for s in streams if s.get('codec_type') == 'video'), {})
            audio_stream = next((s for s in streams if s.get('codec_type') == 'audio'), {})
            
            # 获取音视频时长
            cmd_audio = [str(ffprobe_path), '-v', 'quiet', '-select_streams', 'a:0',
                        '-show_entries', 'stream=duration', '-of', 'csv=p=0', str(video_path)]
            cmd_video = [str(ffprobe_path), '-v', 'quiet', '-select_streams', 'v:0',
                        '-show_entries', 'stream=duration', '-of', 'csv=p=0', str(video_path)]
            
            audio_result = subprocess.run(cmd_audio, capture_output=True, text=True)
            video_result = subprocess.run(cmd_video, capture_output=True, text=True)
            
            audio_duration = float(audio_result.stdout.strip()) if audio_result.returncode == 0 else 0
            video_duration = float(video_result.stdout.strip()) if video_result.returncode == 0 else 0
            
            return {
                'file_size': video_path.stat().st_size / (1024 * 1024),
                'total_duration': float(format_info.get('duration', 0)),
                'bit_rate': int(format_info.get('bit_rate', 0)),
                'format': format_info.get('format_name', ''),
                'video_codec': video_stream.get('codec_name', ''),
                'video_resolution': f"{video_stream.get('width', 0)}x{video_stream.get('height', 0)}",
                'video_fps': video_stream.get('r_frame_rate', ''),
                'video_duration': video_duration,
                'audio_codec': audio_stream.get('codec_name', ''),
                'audio_sample_rate': audio_stream.get('sample_rate', ''),
                'audio_channels': audio_stream.get('channels', ''),
                'audio_bit_rate': int(audio_stream.get('bit_rate', 0)),
                'audio_duration': audio_duration,
                'sync_diff': abs(audio_duration - video_duration)
            }
            
    except Exception as e:
        print(f"Error analyzing {video_name}: {e}")
        return None

def compare_videos():
    """比较三个视频"""
    videos = [
        '2025-08-27_05-40-40_UTC',  # 正常
        '2025-08-25_15-44-54_UTC',  # 正常  
        '2025-08-20_15-43-46_UTC'   # 有问题
    ]
    
    print("=" * 80)
    print("三个视频详细对比")
    print("=" * 80)
    
    results = {}
    for video in videos:
        info = get_detailed_info(video)
        if info:
            results[video] = info
    
    # 打印对比表格
    print(f"{'属性':<25} {'27号视频(正常)':<20} {'25号视频(正常)':<20} {'20号视频(问题)':<20}")
    print("-" * 85)
    
    attributes = [
        ('文件大小(MB)', 'file_size', '{:.2f}'),
        ('总时长(秒)', 'total_duration', '{:.3f}'),
        ('总比特率(bps)', 'bit_rate', '{:,}'),
        ('视频编码', 'video_codec', '{}'),
        ('分辨率', 'video_resolution', '{}'),
        ('帧率', 'video_fps', '{}'),
        ('视频时长(秒)', 'video_duration', '{:.3f}'),
        ('音频编码', 'audio_codec', '{}'),
        ('音频采样率', 'audio_sample_rate', '{}'),
        ('音频声道', 'audio_channels', '{}'),
        ('音频比特率(bps)', 'audio_bit_rate', '{:,}'),
        ('音频时长(秒)', 'audio_duration', '{:.3f}'),
        ('同步差异(秒)', 'sync_diff', '{:.3f}'),
    ]
    
    for name, key, fmt in attributes:
        row = f"{name:<25}"
        for video in videos:
            if video in results:
                value = results[video].get(key, 'N/A')
                if isinstance(value, (int, float)) and value != 0:
                    formatted = fmt.format(value)
                else:
                    formatted = str(value)
                row += f" {formatted:<20}"
            else:
                row += f" {'N/A':<20}"
        print(row)
    
    print("\n" + "=" * 80)
    print("关键差异分析:")
    print("=" * 80)
    
    if len(results) >= 3:
        problem_video = results['2025-08-20_15-43-46_UTC']
        normal_video1 = results['2025-08-27_05-40-40_UTC']
        normal_video2 = results['2025-08-25_15-44-54_UTC']
        
        print(f"1. 音频比特率:")
        print(f"   - 27号正常视频: {normal_video1['audio_bit_rate']:,} bps")
        print(f"   - 25号正常视频: {normal_video2['audio_bit_rate']:,} bps") 
        print(f"   - 20号问题视频: {problem_video['audio_bit_rate']:,} bps ⚠️")
        
        print(f"\n2. 音视频同步:")
        print(f"   - 27号正常视频: {normal_video1['sync_diff']:.3f}秒")
        print(f"   - 25号正常视频: {normal_video2['sync_diff']:.3f}秒")
        print(f"   - 20号问题视频: {problem_video['sync_diff']:.3f}秒 ⚠️")
        
        print(f"\n3. 总比特率:")
        print(f"   - 27号正常视频: {normal_video1['bit_rate']:,} bps")
        print(f"   - 25号正常视频: {normal_video2['bit_rate']:,} bps")
        print(f"   - 20号问题视频: {problem_video['bit_rate']:,} bps")

if __name__ == "__main__":
    compare_videos()
