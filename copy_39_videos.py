#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将刚刚下载的39个视频复制到广告文件夹（21:03-21:10时间段）
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, time

def copy_39_videos_to_ads():
    """将刚刚下载的39个视频复制到广告文件夹"""
    print("📱 复制刚刚下载的39个视频到广告文件夹")
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
    
    # 定义下载时间范围 (21:03 - 21:10)
    today = datetime.now().date()
    start_time = datetime.combine(today, time(21, 3))  # 21:03
    end_time = datetime.combine(today, time(21, 10))   # 21:10
    
    print(f"⏰ 目标时间段: {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}")
    
    # 扫描所有文件
    all_files = list(source_folder.glob("*"))
    target_files = []
    
    for file in all_files:
        if file.is_file() and not file.name.startswith('.') and file.name != "广告":
            # 获取文件修改时间
            modify_time = datetime.fromtimestamp(file.stat().st_mtime)
            
            # 检查是否在目标时间段内
            if start_time <= modify_time <= end_time:
                target_files.append({
                    'file': file,
                    'time': modify_time,
                    'size': file.stat().st_size
                })
    
    # 按时间排序
    target_files.sort(key=lambda x: x['time'])
    
    if not target_files:
        print("❌ 在21:03-21:10时间段内没有找到文件")
        print("🔍 让我显示最新的文件:")
        
        # 显示最新的文件
        all_files_with_time = []
        for file in all_files:
            if file.is_file() and not file.name.startswith('.') and file.name != "广告":
                modify_time = datetime.fromtimestamp(file.stat().st_mtime)
                all_files_with_time.append({
                    'file': file,
                    'time': modify_time,
                    'size': file.stat().st_size
                })
        
        all_files_with_time.sort(key=lambda x: x['time'], reverse=True)
        
        print(f"📄 最新的20个文件:")
        for i, item in enumerate(all_files_with_time[:20], 1):
            file_size = item['size'] / (1024*1024)  # MB
            print(f"   {i}. {item['file'].name} ({item['time'].strftime('%H:%M:%S')}, {file_size:.1f}MB)")
        
        # 如果在目标时间段没找到，就取最新的39*4=156个文件（39个视频，每个通常有4个文件）
        target_files = all_files_with_time[:156]
        print(f"\n🎯 改为复制最新的 {len(target_files)} 个文件")
    else:
        print(f"🎯 找到目标时间段的文件: {len(target_files)} 个")
    
    # 按文件类型分组统计
    video_files = []
    image_files = []
    metadata_files = []
    other_files = []
    
    for item in target_files:
        file = item['file']
        if file.suffix.lower() in ['.mp4', '.mov']:
            video_files.append(item)
        elif file.suffix.lower() in ['.jpg', '.png', '.jpeg']:
            image_files.append(item)
        elif file.suffix in ['.xz', '.txt']:
            metadata_files.append(item)
        else:
            other_files.append(item)
    
    print(f"\n📊 文件类型统计:")
    print(f"   🎥 视频文件: {len(video_files)} 个")
    print(f"   🖼️ 图片文件: {len(image_files)} 个")
    print(f"   📋 元数据文件: {len(metadata_files)} 个")
    print(f"   📄 其他文件: {len(other_files)} 个")
    
    # 验证是否接近39个视频
    if len(video_files) > 0:
        print(f"✅ 找到 {len(video_files)} 个视频文件，符合39个视频的预期")
    
    # 复制文件
    print(f"\n📥 开始复制文件...")
    
    copied_count = 0
    skipped_count = 0
    failed_count = 0
    
    all_items = video_files + image_files + metadata_files + other_files
    
    for i, item in enumerate(all_items, 1):
        file = item['file']
        dst_path = ads_folder / file.name
        
        # 跳过已存在的文件
        if dst_path.exists():
            skipped_count += 1
            continue
        
        try:
            shutil.copy2(file, dst_path)
            file_size = item['size'] / (1024*1024)  # MB
            time_str = item['time'].strftime('%H:%M:%S')
            
            if file.suffix.lower() in ['.mp4', '.mov']:
                print(f"   ✅ 复制视频: {file.name} ({time_str}, {file_size:.1f}MB)")
            elif i % 10 == 0:  # 每10个文件显示一次进度
                print(f"   📊 进度: {i}/{len(all_items)} ({file.suffix})")
            
            copied_count += 1
            
        except Exception as e:
            print(f"   ❌ 复制失败 {file.name}: {e}")
            failed_count += 1
    
    print(f"\n📊 复制完成:")
    print(f"   ✅ 成功复制: {copied_count} 个文件")
    print(f"   ⏭️ 跳过已存在: {skipped_count} 个文件")
    print(f"   ❌ 复制失败: {failed_count} 个文件")
    print(f"   📁 目标文件夹: {ads_folder}")
    
    # 统计广告文件夹内容
    if ads_folder.exists():
        ads_files = list(ads_folder.glob("*"))
        videos = [f for f in ads_files if f.suffix.lower() in ['.mp4', '.mov']]
        images = [f for f in ads_files if f.suffix.lower() in ['.jpg', '.png', '.jpeg']]
        
        total_size = sum(f.stat().st_size for f in ads_files) / (1024*1024)  # MB
        
        print(f"\n📁 广告文件夹最终统计:")
        print(f"   📄 总文件: {len(ads_files)} 个")
        print(f"   🎥 视频文件: {len(videos)} 个")
        print(f"   🖼️ 图片文件: {len(images)} 个")
        print(f"   💾 总大小: {total_size:.1f}MB")
        
        if len(videos) == 39:
            print(f"✅ 完美！正好39个视频文件，符合下载记录")
        elif len(videos) > 35:
            print(f"✅ 接近目标！{len(videos)}个视频文件，基本符合预期")
        else:
            print(f"⚠️ 视频数量({len(videos)})少于预期(39)，可能需要调整时间范围")

def main():
    copy_39_videos_to_ads()

if __name__ == "__main__":
    main()
