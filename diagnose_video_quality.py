#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频质量问题诊断和解决方案
针对跳帧、无声音等问题提供解决方案
"""

import os
import subprocess
from pathlib import Path

def analyze_merge_commands():
    """分析当前合并命令可能的问题"""
    print("🔍 分析当前视频合并设置")
    print("=" * 50)
    
    print("📋 两种合并模式分析:")
    print()
    
    print("1️⃣ 快速合并模式 (merge_videos_with_ffmpeg):")
    print("   命令: ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4")
    print("   ✅ 优点: 速度快，不重新编码")
    print("   ❌ 潜在问题:")
    print("      - 如果源视频编码不一致可能导致跳帧")
    print("      - 音频流不兼容可能导致无声音")
    print("      - 时间戳不连续可能导致播放问题")
    print()
    
    print("2️⃣ 智能合并模式 (merge_videos_with_normalization):")
    print("   命令: 先统一分辨率，再合并")
    print("   统一化: ffmpeg -vf scale+pad -c:v libx264 -crf 23 -c:a aac")
    print("   合并: ffmpeg -f concat -safe 0 -i filelist.txt -c copy")
    print("   ✅ 优点: 分辨率统一，画质稳定")
    print("   ⚠️  注意: 统一后仍用-c copy可能有问题")
    print()
    
    print("🎯 问题诊断:")
    print("-" * 30)
    print("❌ 跳帧可能原因:")
    print("   1. 源视频帧率不一致(30fps vs 25fps vs 24fps)")
    print("   2. -c copy不重新编码，保留原始时间戳问题")
    print("   3. 视频编码格式不完全兼容")
    print()
    
    print("❌ 无声音可能原因:")
    print("   1. 源视频音频编码不一致(aac vs mp3)")
    print("   2. 音频采样率不同(44.1kHz vs 48kHz)")
    print("   3. -c copy时音频流映射问题")
    print()
    
    print("💡 解决方案:")
    print("-" * 30)
    print("🔧 建议改进的合并命令:")
    print("   ffmpeg -f concat -safe 0 -i filelist.txt \\")
    print("          -c:v libx264 -crf 23 -preset medium \\")
    print("          -c:a aac -b:a 128k \\")
    print("          -r 30 -async 1 \\")
    print("          output.mp4")
    print()
    print("📝 参数说明:")
    print("   -c:v libx264: 重新编码视频，确保兼容性")
    print("   -crf 23: 高质量编码")
    print("   -r 30: 强制输出30fps")
    print("   -async 1: 音频自动同步")
    print("   -c:a aac -b:a 128k: 统一音频格式和比特率")

def create_improved_merger():
    """创建改进的合并脚本"""
    print("\n🛠️ 创建改进的合并脚本")
    print("=" * 50)
    
    script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的视频合并器 - 解决跳帧和音频问题
"""

import os
import subprocess
import glob
from datetime import datetime
from pathlib import Path

def merge_videos_quality(video_files, output_path):
    """高质量合并视频，解决跳帧和音频问题"""
    if not video_files:
        print("❌ 没有视频文件可合并")
        return False
    
    print(f"🎬 开始高质量合并 {len(video_files)} 个视频")
    
    # 创建临时文件列表
    filelist_path = "temp_quality_filelist.txt"
    
    try:
        # 写入文件列表
        with open(filelist_path, 'w', encoding='utf-8') as f:
            for video in video_files:
                abs_path = os.path.abspath(video).replace('\\\\', '/')
                f.write(f"file '{abs_path}'\\n")
        
        # 改进的FFmpeg命令 - 解决质量问题
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", filelist_path,
            # 视频编码设置
            "-c:v", "libx264",
            "-crf", "23",           # 高质量
            "-preset", "medium",    # 平衡速度和质量
            "-r", "30",            # 强制30fps，解决跳帧
            # 音频编码设置  
            "-c:a", "aac",
            "-b:a", "128k",        # 音频比特率
            "-async", "1",         # 音频自动同步
            # 其他设置
            "-movflags", "+faststart",  # 优化网络播放
            "-y",                  # 覆盖输出
            output_path
        ]
        
        print("📊 使用高质量编码参数:")
        print("   🎬 视频: H.264, CRF23, 30fps")
        print("   🎵 音频: AAC, 128kbps, 自动同步")
        print("   ⚡ 网络优化: FastStart")
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            size_mb = os.path.getsize(output_path) / (1024*1024)
            print(f"✅ 高质量合并成功! 文件: {output_path} ({size_mb:.1f}MB)")
            return True
        else:
            print(f"❌ 合并失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 处理出错: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(filelist_path):
            os.remove(filelist_path)

def main():
    """主函数 - 测试高质量合并"""
    print("🎯 高质量视频合并测试")
    print("=" * 40)
    
    # 查找测试视频
    video_dir = Path("videos/downloads/ai_vanvan")
    if not video_dir.exists():
        video_dir = Path("../insDownloader/test_downloads_vanvan")
    
    if video_dir.exists():
        videos = list(video_dir.glob("*.mp4"))[:3]  # 取3个测试
        if videos:
            timestamp = datetime.now().strftime("%H-%M-%S")
            output = f"quality_test_{timestamp}.mp4"
            
            print(f"📹 测试视频: {len(videos)} 个")
            success = merge_videos_quality([str(v) for v in videos], output)
            
            if success:
                print("\\n🎉 请播放测试视频检查:")
                print("   1. 是否有跳帧或卡顿")
                print("   2. 音频是否正常")
                print("   3. 画质是否清晰")
        else:
            print("❌ 未找到测试视频")
    else:
        print("❌ 未找到视频目录")

if __name__ == "__main__":
    main()
'''
    
    with open("quality_merge_test.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ 已创建改进合并脚本: quality_merge_test.py")

def main():
    """主函数"""
    print("🎯 视频质量问题诊断")
    print("=" * 50)
    
    analyze_merge_commands()
    create_improved_merger()
    
    print("\n" + "=" * 50)
    print("📋 下一步行动:")
    print("1. 运行 quality_merge_test.py 测试新的合并方式")
    print("2. 手动播放测试视频检查质量")
    print("3. 如果效果好，更新主合并器代码")
    print("4. 重新合并有问题的视频")

if __name__ == "__main__":
    main()
