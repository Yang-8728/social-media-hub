#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将刚刚下载会话的视频复制到广告文件夹
"""

import os
import shutil
import json
import lzma
from pathlib import Path
from datetime import datetime, timedelta
import sys
sys.path.append('src')

from utils.logger import Logger

def copy_recent_session_videos_to_ads():
    """将最近一次下载会话的视频复制到广告文件夹"""
    print("📱 复制刚刚下载的视频到广告文件夹")
    print("=" * 50)
    
    # 初始化日志器
    logger = Logger("ai_vanvan")
    
    # 加载下载日志
    log_data = logger.load_download_log()
    
    # 找到最近的下载记录，筛选出最近30分钟内的下载
    now = datetime.now()
    recent_cutoff = now - timedelta(minutes=30)  # 30分钟内的下载
    
    recent_downloads = []
    for download in log_data["downloads"]:
        if download["status"] == "success":
            timestamp_str = download.get("timestamp", "")
            if timestamp_str:
                try:
                    # 解析时间戳
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    # 转换为本地时间（如果需要）
                    if timestamp.tzinfo:
                        timestamp = timestamp.replace(tzinfo=None)
                    
                    # 检查是否在最近30分钟内
                    if timestamp >= recent_cutoff:
                        recent_downloads.append({
                            'download': download,
                            'timestamp': timestamp
                        })
                except Exception as e:
                    # 如果时间戳解析失败，检查是否是最近的记录（通过位置判断）
                    pass
    
    # 如果基于时间筛选没找到，就取最后的30个成功下载记录
    if not recent_downloads:
        print("⏰ 基于时间筛选未找到，改为获取最新的下载记录...")
        success_downloads = [d for d in log_data["downloads"] if d["status"] == "success"]
        latest_downloads = success_downloads[-30:] if len(success_downloads) >= 30 else success_downloads
        recent_downloads = [{'download': d, 'timestamp': None} for d in latest_downloads]
    
    if not recent_downloads:
        print("❌ 没有找到任何下载记录")
        return
    
    # 按时间排序（最新的在前）
    recent_downloads.sort(key=lambda x: x['timestamp'] if x['timestamp'] else datetime.min, reverse=True)
    
    print(f"🎯 找到最近下载的视频: {len(recent_downloads)} 个")
    
    # 显示时间范围
    if recent_downloads and recent_downloads[0]['timestamp']:
        latest_time = recent_downloads[0]['timestamp']
        oldest_time = recent_downloads[-1]['timestamp']
        print(f"📅 时间范围: {oldest_time.strftime('%H:%M:%S')} - {latest_time.strftime('%H:%M:%S')}")
    
    # 创建广告文件夹
    ads_folder = Path("data/downloads/ai_vanvan") / "2025-08-27" / "广告"
    ads_folder.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 广告文件夹: {ads_folder}")
    
    copied_count = 0
    failed_count = 0
    skipped_count = 0
    
    for i, item in enumerate(recent_downloads, 1):
        download = item['download']
        shortcode = download["shortcode"]
        folder_path = download.get("folder", "")
        timestamp = item['timestamp']
        
        time_str = timestamp.strftime('%H:%M:%S') if timestamp else "未知时间"
        print(f"\n📄 处理 {i}/{len(recent_downloads)}: {shortcode} ({time_str})")
        
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
        files_copied_this_video = 0
        
        for file in related_files:
            src_path = os.path.join(folder_path, file)
            dst_path = ads_folder / file
            
            # 如果目标文件已存在，跳过
            if dst_path.exists():
                print(f"   ⏭️ 已存在: {file}")
                skipped_count += 1
                continue
            
            try:
                shutil.copy2(src_path, dst_path)
                files_copied_this_video += 1
                
                if file.endswith(('.mp4', '.mov')):
                    video_copied = True
                    file_size = os.path.getsize(src_path) / (1024*1024)  # MB
                    print(f"   ✅ 复制视频: {file} ({file_size:.1f}MB)")
                elif file.endswith(('.jpg', '.png', '.jpeg')):
                    print(f"   ✅ 复制图片: {file}")
                elif file.endswith('.json.xz'):
                    print(f"   ✅ 复制元数据: {file}")
                else:
                    print(f"   ✅ 复制文件: {file}")
            except Exception as e:
                print(f"   ❌ 复制失败 {file}: {e}")
                failed_count += 1
        
        if video_copied:
            copied_count += 1
            print(f"   📊 本视频复制了 {files_copied_this_video} 个文件")
    
    print(f"\n📊 复制完成:")
    print(f"   ✅ 成功复制: {copied_count} 个视频")
    print(f"   ⏭️ 跳过已存在: {skipped_count} 个文件") 
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
        
        # 计算总大小
        total_size = sum(f.stat().st_size for f in ads_files) / (1024*1024)  # MB
        print(f"   💾 总大小: {total_size:.1f}MB")
        
        # 显示一些文件名
        print(f"\n📄 最新文件:")
        sorted_files = sorted(ads_files, key=lambda f: f.stat().st_mtime, reverse=True)
        for file in sorted_files[:5]:
            file_size = file.stat().st_size / (1024*1024)  # MB
            print(f"   📄 {file.name} ({file_size:.1f}MB)")
        if len(sorted_files) > 5:
            print(f"   ... 及其他 {len(sorted_files) - 5} 个文件")

def main():
    copy_recent_session_videos_to_ads()

if __name__ == "__main__":
    main()
