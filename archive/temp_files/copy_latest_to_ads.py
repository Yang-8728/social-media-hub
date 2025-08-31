#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将最新下载的视频复制到广告文件夹
"""

import os
import shutil
import json
import lzma
from pathlib import Path
from datetime import datetime, date
import sys
sys.path.append('src')

from utils.logger import Logger

def copy_latest_videos_to_ads():
    """将最新下载的视频复制到广告文件夹"""
    print("📱 复制最新下载的视频到广告文件夹")
    print("=" * 50)
    
    # 初始化日志器
    logger = Logger("ai_vanvan")
    
    # 加载下载日志
    log_data = logger.load_download_log()
    
    # 获取最新的下载记录（最后10个成功的下载）
    recent_downloads = []
    for download in reversed(log_data["downloads"]):  # 从最新的开始
        if download["status"] == "success":
            recent_downloads.append(download)
            if len(recent_downloads) >= 10:  # 最多取10个
                break
    
    if not recent_downloads:
        print("❌ 没有找到任何下载记录")
        return
    
    print(f"🎯 找到最新下载的视频: {len(recent_downloads)} 个")
    
    # 显示最新下载的时间
    if recent_downloads:
        latest_time = recent_downloads[0].get("timestamp", "未知")
        print(f"📅 最新下载时间: {latest_time}")
    
    # 创建广告文件夹
    ads_folder = Path("data/downloads/ai_vanvan") / "2025-08-27" / "广告"
    ads_folder.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 广告文件夹: {ads_folder}")
    
    copied_count = 0
    failed_count = 0
    
    for i, download in enumerate(recent_downloads, 1):
        shortcode = download["shortcode"]
        folder_path = download.get("folder", "")
        timestamp = download.get("timestamp", "未知")
        
        print(f"\n📄 处理 {i}/{len(recent_downloads)}: {shortcode} ({timestamp})")
        
        if not folder_path or not os.path.exists(folder_path):
            print(f"   ❌ 文件夹不存在: {folder_path}")
            failed_count += 1
            continue
        
        # 查找与shortcode相关的所有文件
        related_files = []
        for file in os.listdir(folder_path):
            # 查找包含shortcode的文件，或者json.xz文件中包含该shortcode的
            if shortcode in file:
                related_files.append(file)
            elif file.endswith('.json.xz'):
                # 检查json.xz文件内容
                try:
                    json_path = os.path.join(folder_path, file)
                    with lzma.open(json_path, 'rb') as f:
                        data = json.loads(f.read().decode('utf-8'))
                        if data.get('node', {}).get('shortcode') == shortcode:
                            related_files.append(file)
                            # 还要找对应的媒体文件
                            base_name = file.replace('.json.xz', '')
                            for media_file in os.listdir(folder_path):
                                if media_file.startswith(base_name) and not media_file.endswith('.json.xz'):
                                    if media_file not in related_files:
                                        related_files.append(media_file)
                except Exception as e:
                    continue
        
        if not related_files:
            print(f"   ❌ 没找到相关文件")
            failed_count += 1
            continue
        
        # 复制文件到广告文件夹
        video_copied = False
        for file in related_files:
            src_path = os.path.join(folder_path, file)
            dst_path = ads_folder / file
            
            # 如果目标文件已存在，跳过
            if dst_path.exists():
                print(f"   ⏭️ 跳过已存在: {file}")
                continue
            
            try:
                shutil.copy2(src_path, dst_path)
                if file.endswith(('.mp4', '.jpg', '.png')):
                    video_copied = True
                    print(f"   ✅ 复制视频: {file}")
                elif file.endswith('.json.xz'):
                    print(f"   ✅ 复制元数据: {file}")
                else:
                    print(f"   ✅ 复制文件: {file}")
            except Exception as e:
                print(f"   ❌ 复制失败 {file}: {e}")
                failed_count += 1
        
        if video_copied:
            copied_count += 1
    
    print(f"\n📊 复制完成:")
    print(f"   ✅ 成功复制: {copied_count} 个视频")
    print(f"   ❌ 处理失败: {failed_count} 个")
    print(f"   📁 目标文件夹: {ads_folder}")
    
    # 显示广告文件夹内容
    if ads_folder.exists():
        ads_files = list(ads_folder.glob("*"))
        print(f"\n📁 广告文件夹内容: {len(ads_files)} 个文件")
        
        # 按类型分组显示
        videos = [f for f in ads_files if f.suffix.lower() in ['.mp4', '.mov']]
        images = [f for f in ads_files if f.suffix.lower() in ['.jpg', '.png', '.jpeg']]
        metadata = [f for f in ads_files if f.suffix == '.xz']
        
        print(f"   🎥 视频文件: {len(videos)} 个")
        print(f"   🖼️ 图片文件: {len(images)} 个") 
        print(f"   📋 元数据文件: {len(metadata)} 个")
        
        # 显示一些文件名
        for file in ads_files[:5]:
            file_size = file.stat().st_size / (1024*1024)  # MB
            print(f"   📄 {file.name} ({file_size:.1f}MB)")
        if len(ads_files) > 5:
            print(f"   ... 及其他 {len(ads_files) - 5} 个文件")

def main():
    copy_latest_videos_to_ads()

if __name__ == "__main__":
    main()
