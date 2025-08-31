#!/usr/bin/env python3
"""
测试最后4个视频的合并，验证音视频同步修复
"""
import os
import sys
sys.path.append('src')

from utils.video_merger import VideoMerger
from utils.logger import Logger

def test_last_4_videos():
    """测试最后4个视频合并"""
    # 获取最后4个视频文件
    video_dir = "videos/downloads/ai_vanvan/2025-08-30"
    all_videos = []
    
    for file in os.listdir(video_dir):
        if file.endswith('.mp4'):
            full_path = os.path.join(video_dir, file)
            all_videos.append((full_path, os.path.getmtime(full_path)))
    
    # 按修改时间排序，取最后4个
    all_videos.sort(key=lambda x: x[1], reverse=True)
    last_4_videos = [video[0] for video in all_videos[:4]]
    
    print(f"测试最后4个视频:")
    for i, video in enumerate(last_4_videos):
        filename = os.path.basename(video)
        size_mb = os.path.getsize(video) / (1024*1024)
        print(f"  {i+1}. {filename} ({size_mb:.1f}MB)")
    
    # 创建合并器
    merger = VideoMerger("ai_vanvan")
    
    # 输出文件
    output_path = "videos/merged/ai_vanvan/test_sync_fix_last4.mp4"
    
    print(f"\n开始合并到: {output_path}")
    
    # 执行合并
    success = merger.merge_videos_with_normalization(last_4_videos, output_path)
    
    if success:
        output_size = os.path.getsize(output_path) / (1024*1024)
        print(f"✅ 合并成功! 输出文件: {output_size:.1f}MB")
        print(f"📁 文件位置: {output_path}")
        print("\n请检查视频最后一段是否还有音视频不同步问题")
    else:
        print("❌ 合并失败")

if __name__ == "__main__":
    test_last_4_videos()
