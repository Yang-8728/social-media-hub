#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
只合并2025-08-27文件夹的视频文件
"""

import os
from pathlib import Path
import sys
sys.path.append('src')

from utils.video_merger import VideoMerger

def merge_0827_videos():
    """合并2025-08-27文件夹的视频"""
    print("🎬 合并2025-08-27文件夹的视频")
    print("=" * 50)
    
    # 指定2025-08-27文件夹
    target_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    
    if not target_folder.exists():
        print(f"❌ 文件夹不存在: {target_folder}")
        return
    
    # 获取所有视频文件，按文件名排序
    video_files = sorted(list(target_folder.glob("*.mp4")))
    
    print(f"📁 找到视频文件: {len(video_files)} 个")
    
    if len(video_files) == 0:
        print("❌ 没有找到视频文件")
        return
    
    # 显示前5个和后5个文件
    print(f"\n📋 视频文件列表 (显示前5个和后5个):")
    total_size = 0
    
    for i, video_file in enumerate(video_files, 1):
        size_mb = video_file.stat().st_size / (1024*1024)
        total_size += size_mb
        
        if i <= 5 or i > len(video_files) - 5:
            print(f"  {i:2d}. {video_file.name} ({size_mb:.1f}MB)")
        elif i == 6:
            print(f"      ... (中间 {len(video_files) - 10} 个文件)")
    
    print(f"\n📊 总大小: {total_size:.1f}MB")
    
    # 初始化合并器
    merger = VideoMerger("ai_vanvan")
    
    # 创建简单的输出文件名
    output_name = f"merged_0827.mp4"
    output_path = Path("videos/merged/ai_vanvan") / output_name
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 删除已存在的输出文件
    if output_path.exists():
        output_path.unlink()
        print(f"🗑️ 删除旧文件: {output_name}")
    
    # 执行合并
    print(f"\n🔄 开始合并 {len(video_files)} 个视频...")
    
    try:
        success = merger.merge_videos_with_ffmpeg([str(f) for f in video_files], str(output_path))
        
        if success:
            print(f"✅ 合并成功!")
            
            # 检查输出文件
            if output_path.exists():
                output_size = output_path.stat().st_size / (1024*1024)
                print(f"📊 输出文件: {output_name}")
                print(f"💾 输出大小: {output_size:.1f}MB")
                
                # 质量检查
                size_ratio = output_size / total_size
                print(f"📈 大小比率: {size_ratio:.3f}")
                
                if 0.95 <= size_ratio <= 1.05:
                    print(f"✅ 文件大小比率理想")
                elif 0.8 <= size_ratio < 0.95:
                    print(f"✅ 文件大小比率良好")
                else:
                    print(f"⚠️ 文件大小比率异常")
                
                print(f"\n📁 输出文件路径:")
                print(f"   {output_path}")
                
                return True
            else:
                print(f"❌ 输出文件未生成")
                return False
        else:
            print(f"❌ 合并失败")
            return False
            
    except Exception as e:
        print(f"❌ 合并过程异常: {e}")
        return False

def main():
    print("🎥 2025-08-27视频合并")
    print("=" * 50)
    
    merge_0827_videos()

if __name__ == "__main__":
    main()
