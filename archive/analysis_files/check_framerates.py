"""
检查视频帧率情况
分析现有视频的帧率分布，查看是否需要统一
"""
import os
import sys
from pathlib import Path
from collections import Counter
import subprocess
import json

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.video_merger import VideoMerger

def get_video_framerate(video_path: str) -> float:
    """获取视频帧率"""
    try:
        ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
        cmd = [
            ffprobe_exe,
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            "-select_streams", "v:0",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        # 获取帧率信息
        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'video':
                # 尝试获取帧率
                fps_str = stream.get('r_frame_rate', '0/1')
                if '/' in fps_str:
                    num, den = fps_str.split('/')
                    if float(den) > 0:
                        return float(num) / float(den)
                
                # 备选方法
                avg_fps = stream.get('avg_frame_rate', '0/1')
                if '/' in avg_fps:
                    num, den = avg_fps.split('/')
                    if float(den) > 0:
                        return float(num) / float(den)
        
        return 0.0
        
    except Exception as e:
        print(f"⚠️  获取帧率失败 {video_path}: {e}")
        return 0.0

def check_video_framerates():
    """检查视频帧率分布"""
    account_name = "ai_vanvan"
    
    print(f"🎬 检查 {account_name} 视频的帧率分布")
    print("=" * 60)
    
    # 获取downloads目录
    downloads_base = Path(f"videos/downloads/{account_name}")
    
    if not downloads_base.exists():
        print(f"❌ 下载目录不存在: {downloads_base}")
        return
    
    # 收集所有视频文件
    all_videos = []
    for date_folder in downloads_base.iterdir():
        if date_folder.is_dir():
            for video_file in date_folder.glob("*.mp4"):
                all_videos.append(video_file)
    
    print(f"📁 总共找到 {len(all_videos)} 个视频文件")
    
    # 分析帧率
    framerate_stats = Counter()
    video_details = []
    
    print(f"\n📊 帧率分析 (检查前20个视频):")
    print("-" * 70)
    
    # 只检查前20个，避免太慢
    sample_videos = all_videos[:20]
    
    merger = VideoMerger()
    
    for i, video_file in enumerate(sample_videos, 1):
        print(f"  {i:2d}/20 检查: {video_file.name[:40]:<40}", end=" | ")
        
        # 获取分辨率
        width, height = merger.get_video_resolution(str(video_file))
        
        # 获取帧率
        fps = get_video_framerate(str(video_file))
        
        if fps > 0:
            # 四舍五入到常见帧率
            if abs(fps - 30) < 1:
                rounded_fps = 30.0
            elif abs(fps - 25) < 1:
                rounded_fps = 25.0
            elif abs(fps - 24) < 1:
                rounded_fps = 24.0
            elif abs(fps - 60) < 1:
                rounded_fps = 60.0
            elif abs(fps - 15) < 1:
                rounded_fps = 15.0
            else:
                rounded_fps = round(fps, 1)
            
            framerate_stats[rounded_fps] += 1
            
            video_details.append({
                'file': video_file.name,
                'resolution': f"{width}x{height}" if width and height else "未知",
                'fps': fps,
                'rounded_fps': rounded_fps,
                'date': video_file.parent.name
            })
            
            print(f"{width:4d}x{height:<4d} | {fps:5.1f}fps")
        else:
            print("❌ 获取失败")
    
    if not framerate_stats:
        print("❌ 没有获取到有效的帧率信息")
        return
    
    print(f"\n📈 帧率统计:")
    print("-" * 40)
    
    total_videos = sum(framerate_stats.values())
    for fps, count in framerate_stats.most_common():
        percentage = (count / total_videos) * 100
        print(f"  {fps:4.1f}fps | {count:2d} 个 ({percentage:5.1f}%)")
    
    # 分析结果
    print(f"\n💡 帧率分析结论:")
    print("-" * 40)
    
    most_common_fps = framerate_stats.most_common(1)[0] if framerate_stats else None
    
    if most_common_fps:
        fps, count = most_common_fps
        percentage = (count / total_videos) * 100
        
        print(f"📍 最常见帧率: {fps}fps ({count}个视频, {percentage:.1f}%)")
        
        # 检查是否需要统一
        unique_framerates = len(framerate_stats)
        
        if unique_framerates == 1:
            print("✅ 所有视频帧率一致，无需统一")
        elif unique_framerates <= 3 and percentage >= 70:
            print(f"🟡 主要是{fps}fps，少数其他帧率，建议统一到{fps}fps")
        else:
            print(f"⚠️  帧率差异较大({unique_framerates}种)，建议统一帧率")
    
    # 平台要求分析
    print(f"\n📱 主要平台帧率要求:")
    print("-" * 40)
    print("  B站: 支持24/25/30/50/60fps，推荐30fps")
    print("  抖音: 支持24/25/30fps，推荐30fps") 
    print("  Instagram: 支持23-60fps，推荐30fps")
    print("  YouTube: 支持24/25/30/48/50/60fps")
    
    # 检查当前FFmpeg命令是否处理帧率
    print(f"\n🔧 当前FFmpeg设置检查:")
    print("-" * 40)
    print("📋 当前normalize_video_resolution命令:")
    print('   -vf "scale=..."  # 只处理分辨率')
    print('   -c:v libx264     # 视频编码')
    print('   -crf 23          # 质量设置')
    print('   -preset medium   # 编码速度')
    print('   -c:a aac         # 音频编码')
    print('   -b:a 128k        # 音频码率')
    print()
    print("⚠️  注意: 当前命令没有指定帧率参数")
    print("💡 建议: 可能需要添加 -r 30 来统一帧率到30fps")

if __name__ == "__main__":
    check_video_framerates()
