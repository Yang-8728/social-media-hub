#!/usr/bin/env python3
"""
检查所有29个视频的音频比特率
"""

import subprocess
import json
from pathlib import Path

def get_audio_bitrate(video_path):
    """获取音频比特率"""
    ffprobe_path = Path('tools/ffmpeg/bin/ffprobe.exe')
    
    cmd = [
        str(ffprobe_path), '-v', 'quiet', '-print_format', 'json',
        '-show_streams', '-select_streams', 'a:0', str(video_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            info = json.loads(result.stdout)
            streams = info.get('streams', [])
            if streams:
                return int(streams[0].get('bit_rate', 0))
        return 0
    except Exception as e:
        return 0

def check_all_bitrates():
    """检查所有视频的音频比特率"""
    video_dir = Path('videos/downloads/ai_vanvan/2025-09-01')
    mp4_files = list(video_dir.glob('*.mp4'))
    mp4_files.sort()
    
    print("=" * 80)
    print("所有29个视频的音频比特率分析")
    print("=" * 80)
    
    bitrates = []
    
    print(f"{'序号':<4} {'视频文件名':<45} {'音频比特率':<15} {'状态'}")
    print("-" * 80)
    
    for i, video_file in enumerate(mp4_files, 1):
        bitrate = get_audio_bitrate(video_file)
        bitrates.append(bitrate)
        
        # 判断状态
        if bitrate < 50000:  # 50kbps
            status = "⚠️ 可能需要转换"
        elif bitrate < 60000:  # 60kbps
            status = "🔶 较低"
        else:
            status = "✅ 正常"
        
        print(f"{i:<4} {video_file.name:<45} {bitrate:,} bps{'':<5} {status}")
    
    # 统计分析
    print("\n" + "=" * 80)
    print("统计分析:")
    print("=" * 80)
    
    bitrates = [b for b in bitrates if b > 0]  # 排除无效值
    
    if bitrates:
        min_bitrate = min(bitrates)
        max_bitrate = max(bitrates)
        avg_bitrate = sum(bitrates) / len(bitrates)
        
        print(f"最低音频比特率: {min_bitrate:,} bps")
        print(f"最高音频比特率: {max_bitrate:,} bps")
        print(f"平均音频比特率: {avg_bitrate:,.0f} bps")
        
        # 按范围分类
        very_low = [b for b in bitrates if b < 50000]  # <50k
        low = [b for b in bitrates if 50000 <= b < 60000]  # 50k-60k
        normal = [b for b in bitrates if b >= 60000]  # >=60k
        
        print(f"\n范围分布:")
        print(f"  < 50k bps (需要转换):   {len(very_low)} 个视频")
        print(f"  50k-60k bps (较低):     {len(low)} 个视频")  
        print(f"  >= 60k bps (正常):      {len(normal)} 个视频")
        
        if very_low:
            print(f"\n⚠️ 需要转换AAC的视频 ({len(very_low)}个):")
            for i, video_file in enumerate(mp4_files, 1):
                bitrate = get_audio_bitrate(video_file)
                if bitrate < 50000:
                    print(f"  #{i}: {video_file.name} ({bitrate:,} bps)")

if __name__ == "__main__":
    check_all_bitrates()
