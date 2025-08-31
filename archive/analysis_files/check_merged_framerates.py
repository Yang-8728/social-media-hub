"""
检查合并后视频的帧率
验证合并视频是否保持了30fps
"""
import os
import sys
import subprocess
import json
from pathlib import Path

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
        
        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'video':
                fps_str = stream.get('r_frame_rate', '0/1')
                if '/' in fps_str:
                    num, den = fps_str.split('/')
                    if float(den) > 0:
                        return float(num) / float(den)
        return 0.0
        
    except Exception as e:
        print(f"⚠️  获取帧率失败: {e}")
        return 0.0

def check_merged_video_framerates():
    """检查合并后视频的帧率"""
    account_name = "ai_vanvan"
    
    print("🎬 检查合并后视频的帧率")
    print("=" * 50)
    
    # 查找合并视频目录
    merged_dir = Path(f"videos/merged/{account_name}")
    
    if not merged_dir.exists():
        print(f"❌ 合并目录不存在: {merged_dir}")
        return
    
    # 获取所有合并后的视频
    merged_videos = list(merged_dir.glob("*.mp4"))
    
    if not merged_videos:
        print("❌ 没有找到合并后的视频文件")
        return
    
    print(f"📁 找到 {len(merged_videos)} 个合并视频:")
    print()
    
    for i, video_file in enumerate(merged_videos, 1):
        print(f"{i}. 📹 {video_file.name}")
        
        # 获取文件大小
        size_mb = video_file.stat().st_size / (1024*1024)
        print(f"   📊 大小: {size_mb:.1f}MB")
        
        # 获取帧率
        fps = get_video_framerate(str(video_file))
        if fps > 0:
            print(f"   🎬 帧率: {fps:.1f}fps")
            
            # 判断帧率是否正确
            if abs(fps - 30.0) < 0.1:
                print(f"   ✅ 帧率正确 (30fps)")
            else:
                print(f"   ⚠️  帧率异常 (期望30fps)")
        else:
            print(f"   ❌ 无法获取帧率")
        
        print()
    
    # 总结
    print("💡 帧率检查总结:")
    print("-" * 30)
    
    if all(abs(get_video_framerate(str(v)) - 30.0) < 0.1 for v in merged_videos if get_video_framerate(str(v)) > 0):
        print("✅ 所有合并视频都是30fps，帧率统一完美!")
        print("🎯 适合上传到所有主流平台")
    else:
        print("⚠️  部分合并视频帧率可能有问题")
    
    print("\n📱 平台兼容性:")
    print("  ✅ B站: 30fps推荐帧率")
    print("  ✅ 抖音: 30fps最佳")
    print("  ✅ Instagram: 原生30fps")
    print("  ✅ YouTube: 完全支持")

if __name__ == "__main__":
    check_merged_video_framerates()
