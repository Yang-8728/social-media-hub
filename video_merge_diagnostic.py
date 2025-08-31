#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频合并问题诊断工具
分析合并前后的视频差异，发现"奇奇怪怪"的问题
"""

import os
from pathlib import Path
import sys
import subprocess
sys.path.append('src')

from utils.video_merger import VideoMerger

def analyze_video_issues():
    """分析视频合并问题"""
    print("🔍 视频合并问题诊断")
    print("=" * 50)
    
    # 使用2025-08-27文件夹的前3个视频进行测试
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))[:3]
    
    print(f"📁 测试视频: {len(video_files)} 个")
    for i, video in enumerate(video_files, 1):
        size_mb = video.stat().st_size / (1024*1024)
        print(f"  {i}. {video.name} ({size_mb:.1f}MB)")
    
    # 创建测试合并文件
    merger = VideoMerger("ai_vanvan")
    test_output = Path("videos/merged/ai_vanvan/test_merge_diagnostic.mp4")
    
    if test_output.exists():
        test_output.unlink()
    
    print(f"\n🔄 执行测试合并...")
    success = merger.merge_videos_with_ffmpeg([str(f) for f in video_files], str(test_output))
    
    if not success:
        print(f"❌ 合并失败，无法进行诊断")
        return
    
    print(f"✅ 测试合并完成")
    
    # 开始问题诊断
    print(f"\n🔬 开始问题诊断:")
    print("=" * 40)
    
    # 1. 分辨率一致性检查
    print(f"\n1️⃣ 分辨率一致性检查:")
    resolutions = []
    
    for i, video in enumerate(video_files, 1):
        try:
            width, height = merger.get_video_resolution(str(video))
            resolutions.append((width, height))
            ratio = width / height
            print(f"   源视频{i}: {width}x{height} (比例:{ratio:.2f})")
        except:
            print(f"   源视频{i}: ❌ 无法获取分辨率")
    
    # 检查合并后分辨率
    try:
        merged_width, merged_height = merger.get_video_resolution(str(test_output))
        merged_ratio = merged_width / merged_height
        print(f"   合并后: {merged_width}x{merged_height} (比例:{merged_ratio:.2f})")
        
        # 分析分辨率问题
        unique_resolutions = list(set(resolutions))
        if len(unique_resolutions) > 1:
            print(f"   ⚠️ 发现问题: 源视频分辨率不一致 ({len(unique_resolutions)}种)")
            print(f"   💡 这可能导致: 黑边、拉伸、画面跳跃")
        else:
            print(f"   ✅ 源视频分辨率一致")
    except:
        print(f"   ❌ 无法获取合并后分辨率")
    
    # 2. 文件大小合理性检查
    print(f"\n2️⃣ 文件大小合理性检查:")
    source_total_size = sum(f.stat().st_size for f in video_files) / (1024*1024)
    merged_size = test_output.stat().st_size / (1024*1024)
    size_ratio = merged_size / source_total_size
    
    print(f"   源文件总大小: {source_total_size:.1f}MB")
    print(f"   合并后大小: {merged_size:.1f}MB")
    print(f"   大小比率: {size_ratio:.3f}")
    
    if size_ratio < 0.5:
        print(f"   ❌ 严重问题: 文件过小，可能丢失数据")
    elif size_ratio < 0.8:
        print(f"   ⚠️ 可能问题: 文件偏小，可能质量损失")
    elif size_ratio > 1.2:
        print(f"   ⚠️ 可能问题: 文件过大，可能重复或编码问题")
    else:
        print(f"   ✅ 文件大小正常")
    
    # 3. 检查当前合并参数
    print(f"\n3️⃣ 当前合并参数检查:")
    print(f"   当前使用: FFmpeg concat + copy模式")
    print(f"   参数: -c copy -avoid_negative_ts make_zero -fflags +genpts")
    
    if len(unique_resolutions) > 1:
        print(f"   ⚠️ 建议: 分辨率不一致时应使用normalize模式")
        print(f"   📝 normalize模式会: 统一分辨率、添加黑边、保持比例")
    
    # 4. 测试normalize模式
    print(f"\n4️⃣ 测试分辨率标准化模式:")
    normalize_output = Path("videos/merged/ai_vanvan/test_normalize_diagnostic.mp4")
    
    if normalize_output.exists():
        normalize_output.unlink()
    
    print(f"   执行normalize合并...")
    
    try:
        normalize_success = merger.merge_videos_with_normalization([str(f) for f in video_files], str(normalize_output))
        
        if normalize_success:
            normalize_size = normalize_output.stat().st_size / (1024*1024)
            normalize_ratio = normalize_size / source_total_size
            
            print(f"   ✅ normalize合并成功")
            print(f"   📊 normalize后大小: {normalize_size:.1f}MB (比率:{normalize_ratio:.3f})")
            
            # 对比两种模式
            print(f"\n📊 两种模式对比:")
            print(f"   copy模式:      {merged_size:.1f}MB")
            print(f"   normalize模式: {normalize_size:.1f}MB")
            
            if abs(normalize_ratio - 1.0) < abs(size_ratio - 1.0):
                print(f"   💡 建议: normalize模式质量更好")
            else:
                print(f"   💡 建议: copy模式已经足够")
        else:
            print(f"   ❌ normalize合并失败")
            
    except Exception as e:
        print(f"   ❌ normalize模式出错: {e}")
    
    # 5. 总结和建议
    print(f"\n📋 诊断总结:")
    print("=" * 40)
    
    issues_found = []
    recommendations = []
    
    if len(unique_resolutions) > 1:
        issues_found.append("分辨率不一致")
        recommendations.append("使用normalize模式统一分辨率")
    
    if size_ratio < 0.8 or size_ratio > 1.2:
        issues_found.append("文件大小异常")
        recommendations.append("检查FFmpeg参数和编码设置")
    
    if not issues_found:
        print(f"✅ 未发现明显问题，当前合并配置良好")
    else:
        print(f"⚠️ 发现问题: {', '.join(issues_found)}")
        print(f"💡 建议解决方案:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    
    print(f"\n📁 测试文件:")
    print(f"   copy模式: {test_output}")
    if normalize_output.exists():
        print(f"   normalize模式: {normalize_output}")
    print(f"   💡 可以播放这些文件来验证视觉效果")

def main():
    print("🎥 视频合并问题诊断工具")
    print("=" * 50)
    
    analyze_video_issues()

if __name__ == "__main__":
    main()
