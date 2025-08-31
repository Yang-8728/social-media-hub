#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能复制最新的39个视频到广告文件夹（基于文件名时间戳）
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import re

def copy_latest_39_videos_smart():
    """智能复制最新的39个视频"""
    print("📱 智能复制最新的39个视频到广告文件夹")
    print("=" * 50)
    
    # 源文件夹
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    if not source_folder.exists():
        print(f"❌ 源文件夹不存在: {source_folder}")
        return
    
    # 目标文件夹
    ads_folder = source_folder / "广告"
    ads_folder.mkdir(exist_ok=True)
    
    print(f"📁 源文件夹: {source_folder}")
    print(f"📁 广告文件夹: {ads_folder}")
    
    # 扫描所有视频文件，按文件名中的时间戳排序
    video_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_UTC)\.mp4$')
    video_groups = {}
    
    print("🔍 扫描视频文件...")
    
    for file in source_folder.glob("*.mp4"):
        match = video_pattern.search(file.name)
        if match:
            timestamp_str = match.group(1)
            try:
                # 解析时间戳
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S_UTC")
                
                # 找到对应的所有文件（mp4, jpg, json.xz, txt）
                base_name = timestamp_str
                related_files = []
                
                for ext in ['.mp4', '.jpg', '.json.xz', '.txt']:
                    related_file = source_folder / f"{base_name}{ext}"
                    if related_file.exists():
                        related_files.append(related_file)
                
                if related_files:
                    video_groups[timestamp] = {
                        'timestamp': timestamp,
                        'base_name': base_name,
                        'files': related_files
                    }
                    
            except ValueError:
                continue
    
    # 按时间戳排序，取最新的39个
    sorted_videos = sorted(video_groups.items(), key=lambda x: x[0], reverse=True)
    latest_39_videos = sorted_videos[:39]
    
    print(f"📊 总共找到: {len(sorted_videos)} 个视频")
    print(f"🎯 选择最新的: {len(latest_39_videos)} 个视频")
    
    if latest_39_videos:
        oldest_time = latest_39_videos[-1][0]
        newest_time = latest_39_videos[0][0]
        print(f"📅 时间范围: {oldest_time.strftime('%m-%d %H:%M')} ~ {newest_time.strftime('%m-%d %H:%M')}")
    
    # 统计文件数量
    total_files = 0
    video_count = 0
    image_count = 0
    metadata_count = 0
    
    for timestamp, group in latest_39_videos:
        for file in group['files']:
            total_files += 1
            if file.suffix.lower() == '.mp4':
                video_count += 1
            elif file.suffix.lower() in ['.jpg', '.png']:
                image_count += 1
            elif file.suffix in ['.xz', '.txt']:
                metadata_count += 1
    
    print(f"\n📊 准备复制的文件:")
    print(f"   🎥 视频文件: {video_count} 个")
    print(f"   🖼️ 图片文件: {image_count} 个")
    print(f"   📋 元数据文件: {metadata_count} 个")
    print(f"   📄 总文件: {total_files} 个")
    
    # 复制文件
    print(f"\n📥 开始复制文件...")
    
    copied_count = 0
    skipped_count = 0
    failed_count = 0
    
    for i, (timestamp, group) in enumerate(latest_39_videos, 1):
        print(f"\n📄 复制视频组 {i}/39: {group['base_name']}")
        
        group_copied = 0
        for file in group['files']:
            dst_path = ads_folder / file.name
            
            # 跳过已存在的文件
            if dst_path.exists():
                skipped_count += 1
                print(f"   ⏭️ 跳过: {file.name}")
                continue
            
            try:
                shutil.copy2(file, dst_path)
                file_size = file.stat().st_size / (1024*1024)  # MB
                
                if file.suffix.lower() == '.mp4':
                    print(f"   ✅ 视频: {file.name} ({file_size:.1f}MB)")
                elif file.suffix.lower() in ['.jpg', '.png']:
                    print(f"   ✅ 图片: {file.name}")
                elif file.suffix in ['.xz', '.txt']:
                    print(f"   ✅ 元数据: {file.name}")
                
                copied_count += 1
                group_copied += 1
                
            except Exception as e:
                print(f"   ❌ 复制失败 {file.name}: {e}")
                failed_count += 1
        
        # 显示进度
        if i % 5 == 0:
            print(f"   📊 总进度: {i}/39 个视频组")
    
    print(f"\n📊 复制完成:")
    print(f"   ✅ 成功复制: {copied_count} 个文件")
    print(f"   ⏭️ 跳过已存在: {skipped_count} 个文件")
    print(f"   ❌ 复制失败: {failed_count} 个文件")
    print(f"   📁 目标文件夹: {ads_folder}")
    
    # 验证广告文件夹内容
    if ads_folder.exists():
        ads_files = list(ads_folder.glob("*"))
        videos = [f for f in ads_files if f.suffix.lower() in ['.mp4', '.mov']]
        images = [f for f in ads_files if f.suffix.lower() in ['.jpg', '.png', '.jpeg']]
        metadata = [f for f in ads_files if f.suffix in ['.xz', '.txt']]
        
        total_size = sum(f.stat().st_size for f in ads_files) / (1024*1024)  # MB
        
        print(f"\n📁 广告文件夹最终统计:")
        print(f"   📄 总文件: {len(ads_files)} 个")
        print(f"   🎥 视频文件: {len(videos)} 个")
        print(f"   🖼️ 图片文件: {len(images)} 个")
        print(f"   📋 元数据文件: {len(metadata)} 个")
        print(f"   💾 总大小: {total_size:.1f}MB")
        
        if len(videos) == 39:
            print(f"✅ 完美！正好39个视频文件")
        elif len(videos) > 35:
            print(f"✅ 很好！{len(videos)}个视频文件，接近目标")
        else:
            print(f"⚠️ 视频数量({len(videos)})可能不够")
        
        # 显示一些视频文件名作为验证
        print(f"\n📄 最新的几个视频:")
        for i, video in enumerate(sorted(videos, key=lambda x: x.name, reverse=True)[:5], 1):
            video_size = video.stat().st_size / (1024*1024)  # MB
            print(f"   {i}. {video.name} ({video_size:.1f}MB)")

def main():
    copy_latest_39_videos_smart()

if __name__ == "__main__":
    main()
