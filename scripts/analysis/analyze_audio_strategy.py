#!/usr/bin/env python3
"""
分析两种音频处理策略的优缺点
"""
import os
import subprocess
import glob

def analyze_audio_strategy():
    """分析音频处理策略"""
    VIDEO_DIR = "videos/downloads/ai_vanvan/2025-09-01"
    
    # 获取所有视频文件
    video_pattern = os.path.join(VIDEO_DIR, "*.mp4")
    all_videos = sorted(glob.glob(video_pattern))
    
    print("🎵 音频处理策略分析")
    print("=" * 50)
    
    # 统计当前音频状态
    total_videos = len(all_videos)
    aac_videos = 0
    problem_videos = 0
    normal_videos = 0
    total_size_mb = 0
    
    print(f"📊 分析 {total_videos} 个视频的音频状态...")
    
    for video in all_videos:
        try:
            ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
            cmd = [
                ffprobe_exe,
                "-v", "quiet",
                "-select_streams", "a:0",
                "-show_entries", "stream=bit_rate,codec_name",
                "-of", "default=noprint_wrappers=1",
                video
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = result.stdout.strip()
            
            bitrate = None
            codec = None
            
            for line in output.split('\n'):
                if line.startswith('bit_rate='):
                    bitrate = int(line.split('=')[1]) if line.split('=')[1] != 'N/A' else None
                elif line.startswith('codec_name='):
                    codec = line.split('=')[1]
            
            # 统计
            file_size_mb = os.path.getsize(video) / (1024*1024)
            total_size_mb += file_size_mb
            
            if codec == 'aac':
                aac_videos += 1
            
            if bitrate and bitrate < 50000:  # <50kbps
                problem_videos += 1
            else:
                normal_videos += 1
                
        except Exception:
            pass
    
    print(f"\n📈 当前状态统计:")
    print(f"  总视频数: {total_videos}")
    print(f"  已经是AAC编码: {aac_videos} ({aac_videos/total_videos:.1%})")
    print(f"  有问题视频: {problem_videos} (音频<50kbps)")
    print(f"  正常视频: {normal_videos}")
    print(f"  总文件大小: {total_size_mb:.1f}MB")
    
    print(f"\n🎯 两种策略对比:")
    
    # 策略1: 统一转换所有视频
    print(f"\n📋 策略1: 统一所有视频为AAC 128kbps")
    print(f"  ✅ 优点:")
    print(f"    - 保证所有视频编码参数完全一致")
    print(f"    - 消除所有潜在音频问题")
    print(f"    - 合并时绝对不会有兼容性问题")
    print(f"    - 音质统一，观看体验一致")
    print(f"  ❌ 缺点:")
    print(f"    - 需要重新编码所有{total_videos}个视频")
    print(f"    - 处理时间长(约{total_videos*30}秒-{total_videos*60}秒)")
    print(f"    - 正常视频可能略有质量损失")
    print(f"    - 占用更多处理资源")
    
    # 策略2: 只转换问题视频
    print(f"\n📋 策略2: 只转换有问题的视频")
    print(f"  ✅ 优点:")
    print(f"    - 只需处理{problem_videos}个问题视频")
    print(f"    - 处理时间短(约{problem_videos*30}秒-{problem_videos*60}秒)")
    print(f"    - 正常视频保持原始质量")
    print(f"    - 节省处理资源")
    print(f"  ❌ 缺点:")
    print(f"    - 视频间可能有轻微编码差异")
    print(f"    - 可能遗漏一些边缘问题视频")
    print(f"    - 需要更复杂的检测逻辑")
    
    print(f"\n🤖 我的建议:")
    
    if problem_videos < total_videos * 0.3:  # 如果问题视频<30%
        print(f"  推荐策略2: 只转换问题视频")
        print(f"  理由: 问题视频比例较低({problem_videos}/{total_videos} = {problem_videos/total_videos:.1%})")
        print(f"        效率更高，保持原始质量")
    else:
        print(f"  推荐策略1: 统一转换所有视频")
        print(f"  理由: 问题视频比例较高({problem_videos}/{total_videos} = {problem_videos/total_videos:.1%})")
        print(f"        统一处理更可靠")
    
    print(f"\n💡 混合策略建议:")
    print(f"  1. 先用策略2快速修复已知问题")
    print(f"  2. 如果还有问题，再用策略1统一处理")
    print(f"  3. 对重要项目用策略1，临时测试用策略2")

if __name__ == "__main__":
    analyze_audio_strategy()
