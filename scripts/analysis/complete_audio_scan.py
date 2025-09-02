#!/usr/bin/env python3
"""
完整扫描所有视频的音频比特率 - 确保不漏检
"""
import os
import subprocess
import glob

def get_video_audio_info(video_path):
    """获取视频的音频信息"""
    try:
        ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
        cmd = [
            ffprobe_exe,
            "-v", "quiet",
            "-select_streams", "a:0",
            "-show_entries", "stream=bit_rate,codec_name,sample_rate",
            "-of", "default=noprint_wrappers=1",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        
        info = {"bitrate": None, "codec": None, "sample_rate": None}
        
        for line in output.split('\n'):
            if line.startswith('bit_rate='):
                value = line.split('=')[1]
                if value != 'N/A':
                    info["bitrate"] = int(value)
            elif line.startswith('codec_name='):
                info["codec"] = line.split('=')[1]
            elif line.startswith('sample_rate='):
                value = line.split('=')[1]
                if value != 'N/A':
                    info["sample_rate"] = int(value)
        
        return info
    except Exception as e:
        print(f"❌ 检查失败: {os.path.basename(video_path)} - {e}")
        return {"bitrate": None, "codec": None, "sample_rate": None}

def complete_scan():
    """完整扫描所有视频"""
    VIDEO_DIR = "videos/downloads/ai_vanvan/2025-09-01"
    
    # 获取所有视频文件
    video_pattern = os.path.join(VIDEO_DIR, "*.mp4")
    all_videos = sorted(glob.glob(video_pattern))
    
    print("🔍 完整扫描所有视频音频质量")
    print("=" * 80)
    print(f"📁 目录: {VIDEO_DIR}")
    print(f"📊 实际找到文件数: {len(all_videos)}")
    print()
    
    problem_videos = []
    normal_videos = []
    
    print("📋 详细扫描结果:")
    print("-" * 80)
    print(f"{'序号':<4} {'文件名':<35} {'编码':<8} {'比特率':<10} {'采样率':<10} {'状态'}")
    print("-" * 80)
    
    for i, video in enumerate(all_videos, 1):
        filename = os.path.basename(video)
        info = get_video_audio_info(video)
        
        # 显示信息
        codec = info["codec"] or "未知"
        sample_rate = f"{info['sample_rate']}Hz" if info["sample_rate"] else "未知"
        
        if info["bitrate"]:
            bitrate_kbps = info["bitrate"] / 1000
            bitrate_str = f"{bitrate_kbps:.0f}kbps"
            
            # 判断是否有问题（<50kbps）
            if bitrate_kbps < 50:
                status = "❌ 问题"
                problem_videos.append({
                    "filename": filename,
                    "bitrate_kbps": bitrate_kbps,
                    "codec": codec,
                    "sample_rate": info["sample_rate"]
                })
            else:
                status = "✅ 正常"
                normal_videos.append({
                    "filename": filename,
                    "bitrate_kbps": bitrate_kbps,
                    "codec": codec,
                    "sample_rate": info["sample_rate"]
                })
        else:
            bitrate_str = "无法检测"
            status = "⚠️ 未知"
            # 无法检测的归为正常类别，但需要注意
            normal_videos.append({
                "filename": filename,
                "bitrate_kbps": 0,
                "codec": codec,
                "sample_rate": info["sample_rate"]
            })
        
        print(f"{i:<4} {filename:<35} {codec:<8} {bitrate_str:<10} {sample_rate:<10} {status}")
    
    print("-" * 80)
    
    # 汇总统计
    print(f"\n📊 扫描汇总:")
    print(f"  总视频数: {len(all_videos)}")
    print(f"  正常视频: {len(normal_videos)} ({len(normal_videos)/len(all_videos):.1%})")
    print(f"  问题视频: {len(problem_videos)} ({len(problem_videos)/len(all_videos):.1%})")
    
    # 问题视频详细列表
    if problem_videos:
        print(f"\n❌ 问题视频详细列表 (音频比特率 < 50kbps):")
        print("-" * 60)
        for i, pv in enumerate(problem_videos, 1):
            print(f"  {i}. {pv['filename']}")
            print(f"     音频比特率: {pv['bitrate_kbps']:.0f}kbps")
            print(f"     音频编码: {pv['codec']}")
            print()
    
    # 比特率分布统计
    print(f"📈 音频比特率分布:")
    bitrate_ranges = {
        "< 50kbps": 0,
        "50-100kbps": 0,
        "100-200kbps": 0,
        "> 200kbps": 0
    }
    
    for video in normal_videos + problem_videos:
        br = video['bitrate_kbps']
        if br < 50:
            bitrate_ranges["< 50kbps"] += 1
        elif br < 100:
            bitrate_ranges["50-100kbps"] += 1
        elif br < 200:
            bitrate_ranges["100-200kbps"] += 1
        else:
            bitrate_ranges["> 200kbps"] += 1
    
    for range_name, count in bitrate_ranges.items():
        percentage = count / len(all_videos) * 100
        print(f"  {range_name:<12}: {count:2d} 个 ({percentage:4.1f}%)")
    
    return problem_videos, normal_videos

if __name__ == "__main__":
    problem_videos, normal_videos = complete_scan()
