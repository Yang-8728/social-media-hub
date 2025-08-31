#!/usr/bin/env python3
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
                abs_path = os.path.abspath(video).replace('\\', '/')
                f.write(f"file '{abs_path}'\n")
        
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
    video_dir = Path("../insDownloader/test_downloads_vanvan")
    
    if video_dir.exists():
        videos = list(video_dir.glob("*.mp4"))[:3]  # 取3个测试
        if videos:
            timestamp = datetime.now().strftime("%H-%M-%S")
            output = f"quality_test_{timestamp}.mp4"
            
            print(f"📹 测试视频: {len(videos)} 个")
            success = merge_videos_quality([str(v) for v in videos], output)
            
            if success:
                print("\n🎉 请播放测试视频检查:")
                print("   1. 是否有跳帧或卡顿")
                print("   2. 音频是否正常")
                print("   3. 画质是否清晰")
        else:
            print("❌ 未找到测试视频")
    else:
        print("❌ 未找到视频目录")

if __name__ == "__main__":
    main()
