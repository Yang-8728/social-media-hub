#!/usr/bin/env python3
"""
深度分析1:39位置的问题视频
"""
import os
import subprocess
import glob

def analyze_problem_video_deeply(video_path):
    """深度分析问题视频的所有参数"""
    if not os.path.exists(video_path):
        print(f"❌ 文件不存在: {video_path}")
        return
    
    filename = os.path.basename(video_path)
    print(f"🔍 深度分析问题视频: {filename}")
    print("=" * 60)
    
    ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
    
    # 1. 完整的流信息
    print("📊 完整流信息:")
    try:
        cmd = [
            ffprobe_exe,
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            "-show_format",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        import json
        data = json.loads(result.stdout)
        
        # 格式信息
        format_info = data.get('format', {})
        duration = float(format_info.get('duration', 0))
        print(f"  时长: {duration:.2f}秒")
        print(f"  文件大小: {os.path.getsize(video_path) / (1024*1024):.1f}MB")
        print(f"  比特率: {int(format_info.get('bit_rate', 0)) / 1000:.0f}kbps")
        
        # 视频流
        video_streams = [s for s in data.get('streams', []) if s.get('codec_type') == 'video']
        if video_streams:
            v = video_streams[0]
            print(f"\n🎥 视频流:")
            print(f"  编码: {v.get('codec_name')}")
            print(f"  分辨率: {v.get('width')}x{v.get('height')}")
            print(f"  帧率: {v.get('avg_frame_rate', 'N/A')}")
            print(f"  像素格式: {v.get('pix_fmt', 'N/A')}")
            print(f"  视频比特率: {int(v.get('bit_rate', 0)) / 1000:.0f}kbps" if v.get('bit_rate') else "  视频比特率: N/A")
        
        # 音频流
        audio_streams = [s for s in data.get('streams', []) if s.get('codec_type') == 'audio']
        if audio_streams:
            a = audio_streams[0]
            print(f"\n🔊 音频流:")
            print(f"  编码: {a.get('codec_name')}")
            print(f"  采样率: {a.get('sample_rate')}Hz")
            print(f"  声道: {a.get('channels')}")
            print(f"  音频比特率: {int(a.get('bit_rate', 0)) / 1000:.0f}kbps" if a.get('bit_rate') else "  音频比特率: N/A")
            print(f"  音频格式: {a.get('sample_fmt', 'N/A')}")
        
    except Exception as e:
        print(f"❌ 分析流信息失败: {e}")
    
    # 2. 检查错误和警告
    print(f"\n⚠️ 错误检查:")
    try:
        cmd = [
            ffprobe_exe,
            "-v", "error",
            "-f", "null",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stderr:
            print("发现错误:")
            print(result.stderr)
        else:
            print("  ✅ 未发现明显错误")
            
    except Exception as e:
        print(f"❌ 错误检查失败: {e}")
    
    # 3. 检查时间戳问题
    print(f"\n⏰ 时间戳检查:")
    try:
        cmd = [
            ffprobe_exe,
            "-v", "quiet",
            "-select_streams", "v:0",
            "-show_entries", "packet=pts_time,dts_time,size",
            "-of", "csv=p=0",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        lines = result.stdout.strip().split('\n')[:10]  # 只看前10个包
        
        print("  前10个视频包的时间戳:")
        for i, line in enumerate(lines):
            if line.strip():
                parts = line.split(',')
                if len(parts) >= 3:
                    pts = parts[0] if parts[0] != 'N/A' else '无'
                    dts = parts[1] if parts[1] != 'N/A' else '无'
                    size = parts[2]
                    print(f"    包{i+1}: PTS={pts}, DTS={dts}, 大小={size}")
        
    except subprocess.TimeoutExpired:
        print("  ⏰ 时间戳检查超时")
    except Exception as e:
        print(f"  ❌ 时间戳检查失败: {e}")
    
    # 4. 音视频同步检查
    print(f"\n🎵 音视频同步检查:")
    try:
        # 检查视频时长
        cmd_v = [
            ffprobe_exe,
            "-v", "quiet",
            "-select_streams", "v:0",
            "-show_entries", "stream=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        
        cmd_a = [
            ffprobe_exe,
            "-v", "quiet",
            "-select_streams", "a:0",
            "-show_entries", "stream=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        
        result_v = subprocess.run(cmd_v, capture_output=True, text=True)
        result_a = subprocess.run(cmd_a, capture_output=True, text=True)
        
        if result_v.stdout.strip() and result_a.stdout.strip():
            v_duration = float(result_v.stdout.strip())
            a_duration = float(result_a.stdout.strip())
            diff = abs(v_duration - a_duration)
            
            print(f"  视频流时长: {v_duration:.3f}秒")
            print(f"  音频流时长: {a_duration:.3f}秒")
            print(f"  时长差异: {diff:.3f}秒")
            
            if diff > 0.1:
                print(f"  ⚠️ 音视频时长不匹配！差异{diff:.3f}秒")
            else:
                print(f"  ✅ 音视频时长匹配")
        
    except Exception as e:
        print(f"  ❌ 同步检查失败: {e}")

def main():
    problem_video = "2025-06-11_18-34-31_UTC.mp4"  # 1:39卡顿的视频
    video_path = os.path.join("videos", "downloads", "ai_vanvan", "2025-09-01", problem_video)
    
    analyze_problem_video_deeply(video_path)
    
    print(f"\n💡 建议:")
    print(f"  1. 如果发现时间戳问题，这个视频可能本身损坏")
    print(f"  2. 如果音视频时长不匹配，可能需要特殊处理")
    print(f"  3. 考虑完全排除这个视频，或者单独修复")
    print(f"  4. 检查是否是下载时的问题")

if __name__ == "__main__":
    main()
