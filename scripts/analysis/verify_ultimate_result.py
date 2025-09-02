#!/usr/bin/env python3
"""
验证终极版合并视频的质量
"""
import os
import subprocess

def verify_ultimate_video():
    """验证终极版合并视频"""
    video_file = "ultimate_merged_23_videos.mp4"
    
    if not os.path.exists(video_file):
        print(f"❌ 文件不存在: {video_file}")
        return
    
    print("🎯 终极版合并视频质量验证")
    print("=" * 50)
    
    ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
    
    try:
        # 获取完整信息
        cmd = [
            ffprobe_exe,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        import json
        data = json.loads(result.stdout)
        
        # 文件基本信息
        format_info = data.get('format', {})
        duration = float(format_info.get('duration', 0))
        file_size_mb = os.path.getsize(video_file) / (1024*1024)
        total_bitrate = int(format_info.get('bit_rate', 0)) / 1000 if format_info.get('bit_rate') else 0
        
        print(f"📁 文件信息:")
        print(f"  文件名: {video_file}")
        print(f"  大小: {file_size_mb:.1f}MB")
        print(f"  时长: {duration:.1f}秒 ({duration/60:.1f}分钟)")
        print(f"  总比特率: {total_bitrate:.0f}kbps")
        
        # 视频流信息
        video_streams = [s for s in data.get('streams', []) if s.get('codec_type') == 'video']
        if video_streams:
            v = video_streams[0]
            print(f"\n🎥 视频流:")
            print(f"  编码: {v.get('codec_name')}")
            print(f"  分辨率: {v.get('width')}x{v.get('height')}")
            print(f"  像素格式: {v.get('pix_fmt')}")
            
            if 'avg_frame_rate' in v:
                fps_str = v['avg_frame_rate']
                if '/' in fps_str:
                    num, den = fps_str.split('/')
                    fps = float(num) / float(den) if float(den) != 0 else 0
                    print(f"  帧率: {fps:.2f}fps")
            
            if v.get('bit_rate'):
                v_bitrate = int(v['bit_rate']) / 1000
                print(f"  视频比特率: {v_bitrate:.0f}kbps")
        
        # 音频流信息
        audio_streams = [s for s in data.get('streams', []) if s.get('codec_type') == 'audio']
        if audio_streams:
            a = audio_streams[0]
            print(f"\n🔊 音频流:")
            print(f"  编码: {a.get('codec_name')}")
            print(f"  采样率: {a.get('sample_rate')}Hz")
            print(f"  声道: {a.get('channels')}")
            print(f"  音频格式: {a.get('sample_fmt')}")
            
            if a.get('bit_rate'):
                a_bitrate = int(a['bit_rate']) / 1000
                print(f"  音频比特率: {a_bitrate:.0f}kbps")
        
        print(f"\n🔍 时间戳检查:")
        # 检查前几个包的时间戳
        cmd_ts = [
            ffprobe_exe,
            "-v", "quiet",
            "-select_streams", "v:0",
            "-show_entries", "packet=pts_time,dts_time",
            "-of", "csv=p=0",
            video_file
        ]
        
        result_ts = subprocess.run(cmd_ts, capture_output=True, text=True, timeout=5)
        lines = result_ts.stdout.strip().split('\n')[:5]
        
        has_negative = False
        for i, line in enumerate(lines):
            if line.strip():
                parts = line.split(',')
                if len(parts) >= 2:
                    pts = parts[0] if parts[0] != 'N/A' else '无'
                    dts = parts[1] if parts[1] != 'N/A' else '无'
                    
                    if dts != '无' and float(dts) < 0:
                        has_negative = True
                    
                    print(f"  包{i+1}: PTS={pts}, DTS={dts}")
        
        if has_negative:
            print("  ❌ 仍有负数时间戳")
        else:
            print("  ✅ 时间戳正常，无负数")
        
        # 错误检查
        print(f"\n⚠️ 完整性检查:")
        cmd_error = [
            ffprobe_exe,
            "-v", "error",
            "-show_entries", "packet=pts_time",
            "-select_streams", "v:0",
            "-of", "csv=p=0",
            video_file
        ]
        
        result_error = subprocess.run(cmd_error, capture_output=True, text=True, timeout=10)
        if result_error.stderr:
            print("  ⚠️ 发现问题:")
            print("  " + result_error.stderr[:200] + "..." if len(result_error.stderr) > 200 else "  " + result_error.stderr)
        else:
            print("  ✅ 完整性检查通过")
        
        print(f"\n📊 与之前版本对比:")
        
        # 对比之前的版本
        previous_files = [
            ("merged_videos_fixed_29_videos.mp4", "第一次--merge版本"),
            ("merged_strategy2_23_videos.mp4", "方案2简单版本")
        ]
        
        for prev_file, desc in previous_files:
            if os.path.exists(prev_file):
                prev_size = os.path.getsize(prev_file) / (1024*1024)
                print(f"  {desc}: {prev_size:.1f}MB")
        
        print(f"  终极版本: {file_size_mb:.1f}MB")
        
        print(f"\n🎯 关键测试点:")
        print(f"  1. 播放检查1:39位置是否完全解决卡顿")
        print(f"  2. 验证整个{duration/60:.1f}分钟视频音频连续性")
        print(f"  3. 检查画质统一性和流畅度")
        print(f"  4. 确认所有负数时间戳问题已修复")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

if __name__ == "__main__":
    verify_ultimate_video()
