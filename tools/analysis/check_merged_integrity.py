#!/usr/bin/env python3
"""
检查合并视频的音频完整性
"""

import subprocess
import json
from pathlib import Path

def check_merged_video_integrity():
    """检查合并视频的完整性"""
    merged_video = Path('videos/merged/merged_original_videos_20250901_232046.mp4')
    ffprobe_path = Path('tools/ffmpeg/bin/ffprobe.exe')
    ffmpeg_path = Path('tools/ffmpeg/bin/ffmpeg.exe')
    
    if not merged_video.exists():
        print("❌ 合并视频不存在")
        return
    
    print("=" * 60)
    print("检查合并视频完整性")
    print("=" * 60)
    
    # 1. 基本信息检查
    print("📹 基本信息检查:")
    cmd = [
        str(ffprobe_path), '-v', 'quiet', '-print_format', 'json',
        '-show_format', '-show_streams', str(merged_video)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            info = json.loads(result.stdout)
            format_info = info.get('format', {})
            streams = info.get('streams', [])
            
            duration = float(format_info.get('duration', 0))
            print(f"   总时长: {duration:.2f} 秒 ({duration//60:.0f}:{duration%60:04.1f})")
            
            video_stream = next((s for s in streams if s.get('codec_type') == 'video'), {})
            audio_stream = next((s for s in streams if s.get('codec_type') == 'audio'), {})
            
            if audio_stream:
                print(f"   音频编码: {audio_stream.get('codec_name')}")
                print(f"   音频比特率: {audio_stream.get('bit_rate')} bps")
                print(f"   音频采样率: {audio_stream.get('sample_rate')} Hz")
            else:
                print("   ❌ 没有找到音频流!")
                
    except Exception as e:
        print(f"   ❌ 基本信息检查失败: {e}")
    
    # 2. 音频完整性检查
    print(f"\n🎵 音频完整性检查:")
    cmd_audio = [
        str(ffmpeg_path), '-i', str(merged_video), '-af', 'volumedetect', 
        '-f', 'null', '-', '-v', 'info'
    ]
    
    try:
        result = subprocess.run(cmd_audio, capture_output=True, text=True)
        stderr = result.stderr
        
        # 查找音频分析信息
        if 'volumedetect' in stderr:
            lines = stderr.split('\n')
            for line in lines:
                if 'mean_volume' in line or 'max_volume' in line:
                    print(f"   {line.strip()}")
        
        if result.returncode == 0:
            print("   ✅ 音频流处理完成")
        else:
            print(f"   ⚠️ 音频处理有警告")
            
    except Exception as e:
        print(f"   ❌ 音频完整性检查失败: {e}")
    
    # 3. 检查43秒附近的音频
    print(f"\n🔍 检查43秒附近的音频:")
    
    # 提取43秒前后的音频信息
    cmd_segment = [
        str(ffprobe_path), '-v', 'quiet', '-print_format', 'json',
        '-show_packets', '-select_streams', 'a:0', 
        '-read_intervals', '40%+10',  # 从40秒开始读取10秒
        str(merged_video)
    ]
    
    try:
        result = subprocess.run(cmd_segment, capture_output=True, text=True)
        if result.returncode == 0:
            info = json.loads(result.stdout)
            packets = info.get('packets', [])
            
            if packets:
                first_time = float(packets[0].get('pts_time', 0))
                last_time = float(packets[-1].get('pts_time', 0))
                print(f"   40-50秒区间音频包: {len(packets)} 个")
                print(f"   时间范围: {first_time:.2f}s - {last_time:.2f}s")
                
                # 检查43秒前后是否有音频包
                packets_around_43 = [p for p in packets if 42 <= float(p.get('pts_time', 0)) <= 44]
                print(f"   43秒前后(42-44s)音频包: {len(packets_around_43)} 个")
                
                if len(packets_around_43) == 0:
                    print("   ❌ 43秒附近没有音频包!")
                else:
                    print("   ✅ 43秒附近有音频包")
            else:
                print("   ❌ 40-50秒区间没有音频包!")
                
    except Exception as e:
        print(f"   ❌ 音频包检查失败: {e}")
    
    # 4. 完整视频错误检查
    print(f"\n🔧 完整视频错误检查:")
    cmd_check = [
        str(ffmpeg_path), '-v', 'error', '-i', str(merged_video),
        '-f', 'null', '-'
    ]
    
    try:
        result = subprocess.run(cmd_check, capture_output=True, text=True)
        if result.stderr.strip():
            print(f"   ❌ 发现错误:")
            print(f"   {result.stderr}")
        else:
            print(f"   ✅ 没有发现明显错误")
            
    except Exception as e:
        print(f"   ❌ 错误检查失败: {e}")

if __name__ == "__main__":
    check_merged_video_integrity()
