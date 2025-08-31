#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细检查特定视频文件：ai_vanvan_2025-08-27_17-09-18_normalized.mp4
"""

import os
from pathlib import Path

def detailed_check_specific_video():
    """详细检查指定的视频文件"""
    video_path = "videos/merged/ai_vanvan/ai_vanvan_2025-08-27_17-09-18_normalized.mp4"
    
    print("🔍 详细检查视频：ai_vanvan_2025-08-27_17-09-18_normalized.mp4")
    print("=" * 70)
    
    if not os.path.exists(video_path):
        print("❌ 视频文件不存在")
        return
    
    # 文件基本信息
    stat = os.stat(video_path)
    size_mb = stat.st_size / (1024 * 1024)
    print(f"📦 文件大小: {size_mb:.1f}MB")
    
    # 深度检查文件内容
    try:
        with open(video_path, 'rb') as f:
            # 读取更多数据进行检查
            header = f.read(1024)  # 读取前1KB
            
            print("\n🔍 文件头分析:")
            print(f"   前16字节: {header[:16].hex()}")
            
            # MP4 文件结构检查
            if b'ftyp' in header[:20]:
                ftyp_pos = header.find(b'ftyp')
                print(f"✅ MP4文件类型标识位置: {ftyp_pos}")
                
                # 查找brand信息
                brand_data = header[ftyp_pos:ftyp_pos+20]
                print(f"   Brand信息: {brand_data}")
            
            # 读取更大块来检查轨道信息
            f.seek(0)
            large_chunk = f.read(32768)  # 32KB
            
            print("\n🎵 音频轨道检查:")
            audio_patterns = [
                (b'mp4a', 'MP4 Audio'),
                (b'aac ', 'AAC 编码'),
                (b'soun', '音频轨道'),
                (b'AudioSampleEntry', '音频采样入口'),
                (b'stsd', '采样描述'),
            ]
            
            found_audio = []
            for pattern, desc in audio_patterns:
                if pattern in large_chunk:
                    pos = large_chunk.find(pattern)
                    found_audio.append(f"{desc} (位置: {pos})")
            
            if found_audio:
                print("✅ 检测到音频相关信息:")
                for info in found_audio:
                    print(f"   - {info}")
            else:
                print("⚠️  未在前32KB检测到音频模式")
            
            print("\n🎬 视频轨道检查:")
            video_patterns = [
                (b'avc1', 'H.264/AVC'),
                (b'h264', 'H.264标识'),
                (b'vide', '视频轨道'),
                (b'VideoSampleEntry', '视频采样入口'),
            ]
            
            found_video = []
            for pattern, desc in video_patterns:
                if pattern in large_chunk:
                    pos = large_chunk.find(pattern)
                    found_video.append(f"{desc} (位置: {pos})")
            
            if found_video:
                print("✅ 检测到视频相关信息:")
                for info in found_video:
                    print(f"   - {info}")
            
            # 更深入的音频检查
            print("\n🔊 深度音频检查:")
            f.seek(0)
            full_scan = f.read()  # 读取整个文件（小文件）
            
            # 统计音频相关字节模式出现次数
            audio_count = full_scan.count(b'mp4a') + full_scan.count(b'aac ')
            print(f"   音频模式总出现次数: {audio_count}")
            
            if audio_count > 0:
                print("✅ 文件中确实包含音频数据")
            else:
                print("❌ 文件中可能真的没有音频数据")
                
    except Exception as e:
        print(f"❌ 文件检查出错: {e}")
    
    print(f"\n🎯 关于这个视频文件:")
    print(f"   文件名包含 'normalized'，说明这是经过分辨率标准化处理的")
    print(f"   如果您播放时有声音，那说明我的检测方法不够准确")
    print(f"   请确认：")
    print(f"   1. 播放时是否有声音？")
    print(f"   2. 声音是否清晰正常？")
    print(f"   3. 有没有跳帧现象？")
    print(f"   4. 画质是否满意？")

def main():
    detailed_check_specific_video()

if __name__ == "__main__":
    main()
