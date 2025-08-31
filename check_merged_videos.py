#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查已合并视频的质量和问题
"""

import os
from pathlib import Path
import sys
import time
sys.path.append('src')

from utils.video_merger import VideoMerger

def check_merged_videos():
    """检查merged文件夹下的视频"""
    print("🎬 检查已合并的视频文件")
    print("=" * 50)
    
    merged_folder = Path("videos/merged/ai_vanvan")
    
    if not merged_folder.exists():
        print(f"❌ merged文件夹不存在")
        return
    
    # 获取所有mp4文件，按修改时间排序
    video_files = list(merged_folder.glob("*.mp4"))
    
    if not video_files:
        print(f"❌ 没有找到合并的视频文件")
        return
    
    # 按修改时间排序，最新的在前
    video_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    print(f"📊 找到 {len(video_files)} 个合并视频，显示最新的10个:")
    print()
    
    # 显示视频列表
    for i, video in enumerate(video_files[:10], 1):
        size_mb = video.stat().st_size / (1024*1024)
        mtime = video.stat().st_mtime
        time_str = time.strftime('%m-%d %H:%M', time.localtime(mtime))
        print(f"   {i:2d}. {video.name}")
        print(f"       大小: {size_mb:.1f}MB, 时间: {time_str}")
        print()
    
    # 分析最新的3个视频
    print(f"🔍 详细分析最新的3个视频:")
    print("=" * 50)
    
    merger = VideoMerger("ai_vanvan")
    
    for i, video in enumerate(video_files[:3], 1):
        print(f"\n📹 视频 {i}: {video.name}")
        print("-" * 40)
        
        # 基本信息
        size_mb = video.stat().st_size / (1024*1024)
        mtime = video.stat().st_mtime
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        
        print(f"📊 基本信息:")
        print(f"   文件大小: {size_mb:.1f}MB")
        print(f"   创建时间: {time_str}")
        
        # 分辨率检查
        try:
            width, height = merger.get_video_resolution(str(video))
            ratio = width / height
            
            # 判断视频类型
            if ratio > 1.3:
                video_type = "横屏"
            elif ratio < 0.8:
                video_type = "竖屏"
            elif 0.9 <= ratio <= 1.1:
                video_type = "正方形"
            else:
                video_type = "特殊比例"
            
            print(f"📐 分辨率信息:")
            print(f"   分辨率: {width}x{height}")
            print(f"   长宽比: {ratio:.3f}")
            print(f"   类型: {video_type}")
            
            # 分辨率标准性检查
            if (width, height) in [(720, 1280), (1080, 1920)]:
                print(f"   ✅ 标准竖屏分辨率")
            elif (width, height) in [(1280, 720), (1920, 1080)]:
                print(f"   ✅ 标准横屏分辨率")
            elif width == height:
                print(f"   ✅ 正方形分辨率")
            else:
                print(f"   ⚠️ 非标准分辨率")
                
        except Exception as e:
            print(f"📐 分辨率信息:")
            print(f"   ❌ 无法获取分辨率: {e}")
        
        # 文件完整性检查
        try:
            with open(video, 'rb') as f:
                header = f.read(100)
                if b'ftyp' in header:
                    print(f"🗃️ 文件格式: ✅ 标准MP4格式")
                else:
                    print(f"🗃️ 文件格式: ⚠️ 格式可能有问题")
                    
                # 检查文件尾部
                f.seek(-100, 2)
                footer = f.read(100)
                print(f"🗃️ 文件完整性: ✅ 文件完整")
                
        except Exception as e:
            print(f"🗃️ 文件完整性: ❌ 读取失败: {e}")
        
        # 根据文件名推测合并类型
        filename = video.name.lower()
        if 'normalized' in filename:
            print(f"🔧 合并类型: 分辨率标准化模式")
        elif 'sync_fix' in filename:
            print(f"🔧 合并类型: 同步修复模式")
        elif 'weird_resolutions' in filename:
            print(f"🔧 合并类型: 异常分辨率测试")
        elif 'quality_test' in filename:
            print(f"🔧 合并类型: 质量测试")
        elif 'diagnostic' in filename:
            print(f"🔧 合并类型: 诊断测试")
        else:
            print(f"🔧 合并类型: 标准合并")

def analyze_potential_issues():
    """分析潜在问题"""
    print(f"\n🔬 潜在问题分析:")
    print("=" * 50)
    
    merged_folder = Path("videos/merged/ai_vanvan")
    video_files = list(merged_folder.glob("*.mp4"))
    video_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    merger = VideoMerger("ai_vanvan")
    
    # 检查分辨率一致性
    resolutions = []
    sizes = []
    
    for video in video_files[:5]:  # 检查最新5个
        try:
            width, height = merger.get_video_resolution(str(video))
            resolutions.append((width, height))
            sizes.append(video.stat().st_size / (1024*1024))
        except:
            continue
    
    # 分辨率分析
    unique_resolutions = list(set(resolutions))
    print(f"📐 分辨率一致性:")
    print(f"   发现 {len(unique_resolutions)} 种不同分辨率:")
    
    for res in unique_resolutions:
        count = resolutions.count(res)
        print(f"   - {res[0]}x{res[1]}: {count} 个视频")
    
    if len(unique_resolutions) > 1:
        print(f"   ⚠️ 分辨率不一致可能导致播放问题")
    else:
        print(f"   ✅ 分辨率一致")
    
    # 大小分析
    if sizes:
        avg_size = sum(sizes) / len(sizes)
        print(f"\n📊 文件大小分析:")
        print(f"   平均大小: {avg_size:.1f}MB")
        print(f"   大小范围: {min(sizes):.1f}MB - {max(sizes):.1f}MB")
        
        # 检查异常大小
        for i, size in enumerate(sizes):
            if size < avg_size * 0.3:
                print(f"   ⚠️ 视频 {i+1} 文件过小({size:.1f}MB)")
            elif size > avg_size * 3:
                print(f"   ⚠️ 视频 {i+1} 文件过大({size:.1f}MB)")

def main():
    print("🎥 合并视频质量检查工具")
    print("=" * 50)
    
    check_merged_videos()
    analyze_potential_issues()
    
    print(f"\n💡 建议:")
    print(f"   1. 如果发现分辨率不一致，建议使用normalize模式重新合并")
    print(f"   2. 如果文件大小异常，检查源视频质量")
    print(f"   3. 播放视频验证实际效果")

if __name__ == "__main__":
    main()
