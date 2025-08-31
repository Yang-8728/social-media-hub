#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除广告文件夹中除了视频文件之外的所有文件
"""

import os
from pathlib import Path

def clean_ads_folder():
    """删除广告文件夹中的非视频文件"""
    print("🗑️ 清理广告文件夹 - 删除除视频外的所有文件")
    print("=" * 50)
    
    # 广告文件夹路径
    ads_folder = Path("videos/downloads/ai_vanvan/2025-08-27/广告")
    
    if not ads_folder.exists():
        print(f"❌ 广告文件夹不存在: {ads_folder}")
        return
    
    print(f"📁 目标文件夹: {ads_folder}")
    
    # 统计删除前的文件
    all_files = list(ads_folder.glob("*"))
    video_files = [f for f in all_files if f.suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv']]
    non_video_files = [f for f in all_files if f not in video_files and f.is_file()]
    
    print(f"\n📊 删除前统计:")
    print(f"   📄 总文件: {len(all_files)} 个")
    print(f"   🎥 视频文件: {len(video_files)} 个")
    print(f"   🗑️ 待删除文件: {len(non_video_files)} 个")
    
    if len(non_video_files) == 0:
        print("✅ 没有需要删除的非视频文件")
        return
    
    # 按类型分组显示待删除文件
    image_files = [f for f in non_video_files if f.suffix.lower() in ['.jpg', '.png', '.jpeg', '.gif']]
    metadata_files = [f for f in non_video_files if f.suffix in ['.xz', '.txt', '.json']]
    other_files = [f for f in non_video_files if f not in image_files and f not in metadata_files]
    
    print(f"\n🗂️ 待删除文件分类:")
    print(f"   🖼️ 图片文件: {len(image_files)} 个")
    print(f"   📋 元数据文件: {len(metadata_files)} 个")
    print(f"   📄 其他文件: {len(other_files)} 个")
    
    # 开始删除
    print(f"\n🗑️ 开始删除非视频文件...")
    
    deleted_count = 0
    failed_count = 0
    
    for file in non_video_files:
        try:
            file.unlink()  # 删除文件
            
            if file.suffix.lower() in ['.jpg', '.png', '.jpeg']:
                print(f"   ✅ 删除图片: {file.name}")
            elif file.suffix in ['.xz', '.txt', '.json']:
                print(f"   ✅ 删除元数据: {file.name}")
            else:
                print(f"   ✅ 删除文件: {file.name}")
            
            deleted_count += 1
            
        except Exception as e:
            print(f"   ❌ 删除失败 {file.name}: {e}")
            failed_count += 1
    
    print(f"\n📊 删除完成:")
    print(f"   ✅ 成功删除: {deleted_count} 个文件")
    print(f"   ❌ 删除失败: {failed_count} 个文件")
    
    # 验证删除后的状态
    remaining_files = list(ads_folder.glob("*"))
    remaining_videos = [f for f in remaining_files if f.suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv']]
    remaining_others = [f for f in remaining_files if f not in remaining_videos and f.is_file()]
    
    print(f"\n📁 删除后统计:")
    print(f"   📄 剩余文件: {len(remaining_files)} 个")
    print(f"   🎥 视频文件: {len(remaining_videos)} 个")
    print(f"   📄 其他文件: {len(remaining_others)} 个")
    
    if len(remaining_others) == 0:
        print("✅ 完美！现在文件夹里只有视频文件了")
        
        # 计算视频文件总大小
        total_size = sum(f.stat().st_size for f in remaining_videos) / (1024*1024)  # MB
        print(f"💾 视频文件总大小: {total_size:.1f}MB")
        
        # 显示前5个视频文件
        print(f"\n📄 保留的视频文件:")
        for i, video in enumerate(sorted(remaining_videos, key=lambda x: x.name, reverse=True)[:5], 1):
            video_size = video.stat().st_size / (1024*1024)  # MB
            print(f"   {i}. {video.name} ({video_size:.1f}MB)")
        if len(remaining_videos) > 5:
            print(f"   ... 及其他 {len(remaining_videos) - 5} 个视频文件")
    else:
        print(f"⚠️ 还有 {len(remaining_others)} 个非视频文件残留:")
        for file in remaining_others:
            print(f"   📄 {file.name}")

def main():
    clean_ads_folder()

if __name__ == "__main__":
    main()
