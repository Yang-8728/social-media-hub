#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的视频合并质量测试工具
"""

import os
from pathlib import Path
import sys
sys.path.append('src')

from utils.video_merger import VideoMerger

def test_merge_quality():
    """测试视频合并并检查基本质量指标"""
    print("🎬 视频合并质量测试")
    print("=" * 50)
    
    # 使用广告文件夹中的视频
    ads_folder = Path("videos/downloads/ai_vanvan/2025-08-27/广告")
    
    if not ads_folder.exists():
        print(f"❌ 广告文件夹不存在: {ads_folder}")
        return
    
    # 获取前3个视频进行快速测试
    video_files = sorted(list(ads_folder.glob("*.mp4")))[:3]
    
    if len(video_files) < 2:
        print(f"❌ 视频文件不足，需要至少2个视频")
        return
    
    print(f"📁 使用视频文件: {len(video_files)} 个")
    
    total_input_size = 0
    total_input_duration = 0
    
    for i, video in enumerate(video_files, 1):
        size_mb = video.stat().st_size / (1024*1024)
        total_input_size += size_mb
        print(f"   {i}. {video.name} ({size_mb:.1f}MB)")
    
    print(f"📊 输入视频总大小: {total_input_size:.1f}MB")
    
    # 初始化合并器
    merger = VideoMerger("ai_vanvan")
    
    # 执行合并
    print(f"\n🔄 开始合并...")
    
    try:
        # 创建输出文件名
        output_name = f"quality_test_{len(video_files)}videos.mp4"
        output_path = Path("videos/merged/ai_vanvan") / output_name
        
        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 删除已存在的输出文件
        if output_path.exists():
            output_path.unlink()
            print(f"🗑️ 删除旧文件: {output_name}")
        
        # 执行合并
        success = merger.merge_videos_with_ffmpeg(video_files, str(output_path))
        
        if success:
            print(f"✅ 合并成功!")
            
            # 检查输出文件
            if output_path.exists():
                output_size = output_path.stat().st_size / (1024*1024)
                print(f"📊 输出文件: {output_name}")
                print(f"💾 输出大小: {output_size:.1f}MB")
                
                # 基本质量检查
                size_ratio = output_size / total_input_size
                print(f"📈 大小比率: {size_ratio:.2f}")
                
                if size_ratio < 0.3:
                    print(f"⚠️ 输出文件过小，可能存在质量问题")
                elif size_ratio > 1.2:
                    print(f"⚠️ 输出文件过大，可能存在重复或编码问题")
                else:
                    print(f"✅ 文件大小比率正常")
                
                # 检查文件是否可读
                try:
                    with open(output_path, 'rb') as f:
                        header = f.read(100)
                        if b'ftyp' in header or b'moov' in header:
                            print(f"✅ 视频文件格式正常")
                        else:
                            print(f"⚠️ 视频文件格式可能有问题")
                except Exception as e:
                    print(f"❌ 文件读取失败: {e}")
                
                # 显示合并后的文件位置
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

def check_recent_merged_videos():
    """检查最近合并的视频文件"""
    print(f"\n📂 检查最近的合并视频:")
    print("=" * 40)
    
    merged_folder = Path("videos/merged/ai_vanvan")
    
    if not merged_folder.exists():
        print(f"❌ 合并文件夹不存在")
        return
    
    # 获取所有mp4文件，按修改时间排序
    video_files = list(merged_folder.glob("*.mp4"))
    
    if not video_files:
        print(f"❌ 没有找到合并的视频文件")
        return
    
    # 按修改时间排序，最新的在前
    video_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    print(f"📊 找到 {len(video_files)} 个合并视频:")
    
    for i, video in enumerate(video_files[:5], 1):  # 显示最新的5个
        size_mb = video.stat().st_size / (1024*1024)
        mtime = video.stat().st_mtime
        import time
        time_str = time.strftime('%m-%d %H:%M', time.localtime(mtime))
        print(f"   {i}. {video.name}")
        print(f"      大小: {size_mb:.1f}MB, 时间: {time_str}")
    
    if len(video_files) > 5:
        print(f"   ... 及其他 {len(video_files) - 5} 个文件")

def main():
    print("🎥 视频合并质量测试工具")
    print("=" * 50)
    
    # 首先检查现有的合并视频
    check_recent_merged_videos()
    
    # 然后进行新的合并测试
    print(f"\n" + "=" * 50)
    test_result = test_merge_quality()
    
    print(f"\n📊 测试结果:")
    if test_result:
        print(f"✅ 合并测试成功完成")
        print(f"💡 建议: 可以尝试播放输出文件验证音视频同步")
    else:
        print(f"❌ 合并测试失败")
        print(f"💡 建议: 检查FFmpeg参数和输入文件")

if __name__ == "__main__":
    main()
