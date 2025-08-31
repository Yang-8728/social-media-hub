#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试分辨率标准化功能 - 检查昨天的优化进度
"""

import os
from pathlib import Path
import sys
sys.path.append('src')

from utils.video_merger import VideoMerger

def test_resolution_analysis():
    """测试分辨率分析功能"""
    print("🔍 测试分辨率分析功能")
    print("=" * 50)
    
    # 使用广告文件夹中的视频进行分析
    ads_folder = Path("videos/downloads/ai_vanvan/2025-08-27/广告")
    
    if not ads_folder.exists():
        print(f"❌ 广告文件夹不存在: {ads_folder}")
        return
    
    # 获取前10个视频进行分析
    video_files = sorted(list(ads_folder.glob("*.mp4")))[:10]
    
    print(f"📁 分析视频文件: {len(video_files)} 个")
    
    # 初始化合并器
    merger = VideoMerger("ai_vanvan")
    
    # 分析每个视频的分辨率
    print(f"\n📊 分辨率分析:")
    resolutions = {}
    
    for i, video in enumerate(video_files, 1):
        try:
            width, height = merger.get_video_resolution(str(video))
            ratio = width / height if height > 0 else 0
            
            # 分类视频类型
            if ratio > 1.3:
                video_type = "横屏"
            elif ratio < 0.8:
                video_type = "竖屏"
            elif 0.9 <= ratio <= 1.1:
                video_type = "正方形"
            else:
                video_type = "特殊比例"
            
            resolution_key = f"{width}x{height}"
            if resolution_key not in resolutions:
                resolutions[resolution_key] = {'count': 0, 'type': video_type, 'ratio': ratio}
            resolutions[resolution_key]['count'] += 1
            
            print(f"   {i:2d}. {video.name[:30]:<30} {width:4d}x{height:<4d} ({video_type}) 比例:{ratio:.2f}")
            
        except Exception as e:
            print(f"   {i:2d}. {video.name[:30]:<30} ❌ 无法获取分辨率: {e}")
    
    # 统计分辨率分布
    print(f"\n📈 分辨率分布统计:")
    for resolution, info in sorted(resolutions.items(), key=lambda x: x[1]['count'], reverse=True):
        print(f"   {resolution:<12} {info['type']:<8} 数量:{info['count']} 比例:{info['ratio']:.2f}")
    
    # 测试目标分辨率选择
    print(f"\n🎯 目标分辨率选择:")
    try:
        target_width, target_height = merger.find_target_resolution([str(v) for v in video_files])
        print(f"   选择的目标分辨率: {target_width}x{target_height}")
        
        target_ratio = target_width / target_height
        if target_ratio > 1.3:
            target_type = "横屏"
        elif target_ratio < 0.8:
            target_type = "竖屏"
        else:
            target_type = "正方形"
        
        print(f"   目标类型: {target_type} (比例: {target_ratio:.2f})")
        
    except Exception as e:
        print(f"   ❌ 目标分辨率选择失败: {e}")

def test_normalization_function():
    """测试分辨率标准化功能"""
    print(f"\n🔧 测试分辨率标准化功能")
    print("=" * 50)
    
    # 使用广告文件夹中的前3个视频
    ads_folder = Path("videos/downloads/ai_vanvan/2025-08-27/广告")
    video_files = sorted(list(ads_folder.glob("*.mp4")))[:3]
    
    print(f"📁 测试视频文件: {len(video_files)} 个")
    
    # 初始化合并器
    merger = VideoMerger("ai_vanvan")
    
    # 创建输出文件名
    output_name = f"normalized_test_{len(video_files)}videos.mp4"
    output_path = Path("videos/merged/ai_vanvan") / output_name
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 删除已存在的输出文件
    if output_path.exists():
        output_path.unlink()
        print(f"🗑️ 删除旧文件: {output_name}")
    
    # 测试标准化合并
    print(f"\n🔄 开始标准化合并...")
    
    try:
        success = merger.merge_videos_with_normalization([str(v) for v in video_files], str(output_path))
        
        if success:
            print(f"✅ 标准化合并成功!")
            
            # 检查输出文件
            if output_path.exists():
                output_size = output_path.stat().st_size / (1024*1024)
                print(f"📊 输出文件: {output_name}")
                print(f"💾 输出大小: {output_size:.1f}MB")
                
                # 检查输出视频的分辨率
                try:
                    width, height = merger.get_video_resolution(str(output_path))
                    print(f"📐 输出分辨率: {width}x{height}")
                    
                    ratio = width / height
                    if ratio > 1.3:
                        video_type = "横屏"
                    elif ratio < 0.8:
                        video_type = "竖屏"
                    else:
                        video_type = "正方形"
                    
                    print(f"📱 视频类型: {video_type} (比例: {ratio:.2f})")
                    
                except Exception as e:
                    print(f"⚠️ 无法获取输出分辨率: {e}")
                
                print(f"\n📁 输出文件路径:")
                print(f"   {output_path}")
                
                return True
            else:
                print(f"❌ 输出文件未生成")
                return False
        else:
            print(f"❌ 标准化合并失败")
            return False
            
    except Exception as e:
        print(f"❌ 标准化过程异常: {e}")
        return False

def main():
    print("🎥 分辨率标准化功能测试")
    print("=" * 50)
    
    # 测试分辨率分析
    test_resolution_analysis()
    
    # 测试标准化功能
    test_result = test_normalization_function()
    
    print(f"\n📊 测试结果:")
    if test_result:
        print(f"✅ 分辨率标准化功能工作正常")
        print(f"💡 昨天的优化：去除黑边、统一分辨率功能已实现")
    else:
        print(f"❌ 分辨率标准化功能有问题")
        print(f"💡 可能需要进一步优化参数")

if __name__ == "__main__":
    main()
