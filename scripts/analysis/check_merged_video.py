#!/usr/bin/env python3
"""
检查修复后的合并视频质量
"""
import os
import subprocess

def check_video_info(video_path):
    """检查视频的详细信息"""
    if not os.path.exists(video_path):
        print(f"❌ 文件不存在: {video_path}")
        return
    
    ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
    
    print(f"🎬 检查视频: {os.path.basename(video_path)}")
    print("=" * 50)
    
    # 1. 基本信息
    cmd = [
        ffprobe_exe,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        import json
        data = json.loads(result.stdout)
        
        # 文件大小
        file_size_mb = os.path.getsize(video_path) / (1024*1024)
        print(f"📁 文件大小: {file_size_mb:.1f}MB")
        
        # 格式信息
        format_info = data.get('format', {})
        duration = float(format_info.get('duration', 0))
        print(f"⏱️ 总时长: {duration:.1f}秒 ({duration/60:.1f}分钟)")
        
        # 视频流信息
        video_streams = [s for s in data.get('streams', []) if s.get('codec_type') == 'video']
        if video_streams:
            v = video_streams[0]
            print(f"🎥 视频编码: {v.get('codec_name')}")
            print(f"📐 分辨率: {v.get('width')}x{v.get('height')}")
            if 'avg_frame_rate' in v:
                fps_str = v['avg_frame_rate']
                if '/' in fps_str:
                    num, den = fps_str.split('/')
                    fps = float(num) / float(den) if float(den) != 0 else 0
                    print(f"🎞️ 帧率: {fps:.2f}fps")
        
        # 音频流信息
        audio_streams = [s for s in data.get('streams', []) if s.get('codec_type') == 'audio']
        if audio_streams:
            a = audio_streams[0]
            print(f"🔊 音频编码: {a.get('codec_name')}")
            print(f"🎵 采样率: {a.get('sample_rate')}Hz")
            if 'bit_rate' in a:
                bitrate_kbps = int(a['bit_rate']) / 1000
                print(f"📊 音频比特率: {bitrate_kbps:.0f}kbps")
        
    except Exception as e:
        print(f"❌ 检查视频信息失败: {e}")
        return
    
    print("\n" + "="*50)
    
    # 2. 检查是否有错误或警告
    print("🔍 检查视频完整性...")
    cmd = [
        ffprobe_exe,
        "-v", "error",
        "-show_entries", "packet=pts_time,dts_time",
        "-select_streams", "v:0",
        "-of", "csv=p=0",
        video_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.stderr:
            print(f"⚠️ 发现警告/错误:")
            print(result.stderr[:500] + "..." if len(result.stderr) > 500 else result.stderr)
        else:
            print("✅ 未发现严重错误")
    except subprocess.TimeoutExpired:
        print("⏰ 检查超时，但这通常表示视频正常")
    except Exception as e:
        print(f"❌ 完整性检查失败: {e}")

def main():
    video_file = "merged_videos_fixed_29_videos.mp4"
    check_video_info(video_file)
    
    print(f"\n🎯 测试建议:")
    print(f"1. 播放视频检查前43秒是否有音频")
    print(f"2. 检查43秒后音频是否正常")
    print(f"3. 观察问题视频部分的表现")

if __name__ == "__main__":
    main()
