#!/usr/bin/env python3
"""
修复合并视频的时间戳问题
"""

import subprocess
from pathlib import Path
from datetime import datetime

def fix_merged_video():
    """修复合并视频的时间戳问题"""
    input_video = Path('videos/merged/merged_original_videos_20250901_232046.mp4')
    output_dir = Path('videos/merged')
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_video = output_dir / f'merged_original_fixed_{timestamp}.mp4'
    
    ffmpeg_path = Path('tools/ffmpeg/bin/ffmpeg.exe')
    
    print("=" * 60)
    print("修复合并视频时间戳问题")
    print("=" * 60)
    
    # 重新编码音频，保持视频不变
    cmd = [
        str(ffmpeg_path),
        '-i', str(input_video),
        '-c:v', 'copy',           # 视频流直接复制
        '-c:a', 'aac',            # 音频重新编码为AAC
        '-b:a', '128k',           # 音频比特率128k
        '-avoid_negative_ts', 'make_zero',  # 避免负时间戳
        '-fflags', '+genpts',     # 重新生成时间戳
        str(output_video),
        '-y'
    ]
    
    print("🔧 重新编码音频修复时间戳...")
    print(f"输入: {input_video}")
    print(f"输出: {output_video}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if output_video.exists():
                size_mb = output_video.stat().st_size / (1024 * 1024)
                print(f"✅ 修复成功!")
                print(f"📁 修复后文件: {output_video}")
                print(f"📊 文件大小: {size_mb:.2f} MB")
                
                # 检查修复后的视频
                print(f"\n🔍 检查修复后的视频...")
                check_cmd = [
                    str(ffmpeg_path), '-v', 'error', '-i', str(output_video),
                    '-f', 'null', '-'
                ]
                
                check_result = subprocess.run(check_cmd, capture_output=True, text=True)
                if check_result.stderr.strip():
                    print(f"⚠️ 仍有一些警告:")
                    print(check_result.stderr)
                else:
                    print(f"✅ 修复后的视频没有错误!")
                    
            else:
                print("❌ 修复失败：输出文件不存在")
        else:
            print(f"❌ 修复失败:")
            print(f"错误信息: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 修复过程出错: {e}")

if __name__ == "__main__":
    fix_merged_video()
