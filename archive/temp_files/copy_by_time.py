#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将刚刚下载的视频复制到广告文件夹（基于文件创建时间）
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta

def copy_recent_files_to_ads():
    """将最近创建的文件复制到广告文件夹"""
    print("📱 复制刚刚下载的视频到广告文件夹")
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
    
    # 找到最近30分钟内创建的文件
    now = datetime.now()
    recent_cutoff = now - timedelta(minutes=30)
    
    print(f"⏰ 筛选时间: {recent_cutoff.strftime('%H:%M:%S')} 之后的文件")
    
    # 扫描所有文件
    all_files = list(source_folder.glob("*"))
    recent_files = []
    
    for file in all_files:
        if file.is_file() and not file.name.startswith('.'):
            # 获取文件创建时间
            create_time = datetime.fromtimestamp(file.stat().st_ctime)
            modify_time = datetime.fromtimestamp(file.stat().st_mtime)
            
            # 使用更晚的时间（创建或修改）
            file_time = max(create_time, modify_time)
            
            if file_time >= recent_cutoff:
                recent_files.append({
                    'file': file,
                    'time': file_time,
                    'size': file.stat().st_size
                })
    
    # 按时间排序
    recent_files.sort(key=lambda x: x['time'], reverse=True)
    
    if not recent_files:
        print("❌ 没有找到最近30分钟内的文件")
        print("🔍 让我显示最新的10个文件:")
        
        # 显示最新的文件
        all_files_with_time = []
        for file in all_files:
            if file.is_file() and not file.name.startswith('.'):
                modify_time = datetime.fromtimestamp(file.stat().st_mtime)
                all_files_with_time.append({
                    'file': file,
                    'time': modify_time,
                    'size': file.stat().st_size
                })
        
        all_files_with_time.sort(key=lambda x: x['time'], reverse=True)
        
        print(f"📄 最新的10个文件:")
        for i, item in enumerate(all_files_with_time[:10], 1):
            file_size = item['size'] / (1024*1024)  # MB
            print(f"   {i}. {item['file'].name} ({item['time'].strftime('%H:%M:%S')}, {file_size:.1f}MB)")
        
        # 让用户选择复制最新的多少个文件
        recent_files = all_files_with_time[:30]  # 复制最新的30个文件
        print(f"\n🎯 将复制最新的 {len(recent_files)} 个文件")
    else:
        print(f"🎯 找到最近的文件: {len(recent_files)} 个")
    
    copied_count = 0
    skipped_count = 0
    failed_count = 0
    
    # 按文件类型分组
    video_files = []
    image_files = []
    metadata_files = []
    other_files = []
    
    for item in recent_files:
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
    
    # 复制文件
    print(f"\n📥 开始复制文件...")
    
    all_items = video_files + image_files + metadata_files + other_files
    
    for i, item in enumerate(all_items, 1):
        file = item['file']
        dst_path = ads_folder / file.name
        
        # 跳过已存在的文件
        if dst_path.exists():
            print(f"   ⏭️ 跳过已存在: {file.name}")
            skipped_count += 1
            continue
        
        try:
            shutil.copy2(file, dst_path)
            file_size = item['size'] / (1024*1024)  # MB
            time_str = item['time'].strftime('%H:%M:%S')
            
            if file.suffix.lower() in ['.mp4', '.mov']:
                print(f"   ✅ 复制视频: {file.name} ({time_str}, {file_size:.1f}MB)")
            elif file.suffix.lower() in ['.jpg', '.png', '.jpeg']:
                print(f"   ✅ 复制图片: {file.name} ({time_str})")
            else:
                print(f"   ✅ 复制文件: {file.name} ({time_str})")
            
            copied_count += 1
            
        except Exception as e:
            print(f"   ❌ 复制失败 {file.name}: {e}")
            failed_count += 1
        
        # 显示进度
        if i % 10 == 0:
            print(f"   📊 进度: {i}/{len(all_items)}")
    
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

def main():
    copy_recent_files_to_ads()

if __name__ == "__main__":
    main()
