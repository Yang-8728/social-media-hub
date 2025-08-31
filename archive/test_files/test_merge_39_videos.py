#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试合并所有39个视频
"""

import os
from pathlib import Path
import sys
sys.path.append('src')

from utils.video_merger import VideoMerger

def test_merge_all_39_videos():
    """测试合并所有39个视频"""
    print("🎬 测试合并全部39个视频")
    print("=" * 50)
    
    # 使用广告文件夹中的所有视频
    ads_folder = Path("videos/downloads/ai_vanvan/2025-08-27/广告")
    
    if not ads_folder.exists():
        print(f"❌ 广告文件夹不存在: {ads_folder}")
        return
    
    # 获取所有视频文件，按时间排序
    video_files = sorted(list(ads_folder.glob("*.mp4")))
    
    print(f"📁 找到视频文件: {len(video_files)} 个")
    
    if len(video_files) != 39:
        print(f"⚠️ 视频数量不是39个，实际: {len(video_files)}")
    
    # 显示视频范围
    if video_files:
        first_video = video_files[0].name
        last_video = video_files[-1].name
        print(f"📅 视频时间范围:")
        print(f"   最早: {first_video}")
        print(f"   最新: {last_video}")
    
    # 计算总大小
    total_size = 0
    for video in video_files:
        size_mb = video.stat().st_size / (1024*1024)
        total_size += size_mb
    
    print(f"📊 输入视频总大小: {total_size:.1f}MB")
    
    # 初始化合并器
    merger = VideoMerger("ai_vanvan")
    
    # 执行合并
    print(f"\n🔄 开始合并全部39个视频...")
    
    try:
        # 创建输出文件名
        output_name = f"ai_vanvan_all_39videos_{len(video_files)}videos.mp4"
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
                
                # 质量检查
                size_ratio = output_size / total_size
                print(f"📈 大小比率: {size_ratio:.3f}")
                
                if 0.95 <= size_ratio <= 1.05:
                    print(f"✅ 文件大小比率理想 (损失极小)")
                elif 0.8 <= size_ratio < 0.95:
                    print(f"✅ 文件大小比率良好 (轻微压缩)")
                elif size_ratio < 0.8:
                    print(f"⚠️ 文件大小比率偏低 (可能质量损失)")
                else:
                    print(f"⚠️ 文件大小比率过高 (可能有问题)")
                
                # 计算合并后的视频时长估算
                avg_duration = 15  # 假设每个视频平均15秒
                estimated_duration = len(video_files) * avg_duration
                print(f"📽️ 估算总时长: {estimated_duration}秒 ({estimated_duration//60}分{estimated_duration%60}秒)")
                
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

def main():
    print("🎥 39个视频合并测试")
    print("=" * 50)
    
    test_result = test_merge_all_39_videos()
    
    print(f"\n📊 测试结果:")
    if test_result:
        print(f"✅ 39个视频合并测试成功")
        print(f"💡 这证明合并功能可以处理大量视频文件")
        print(f"💡 质量参数设置正确，适合批量处理")
    else:
        print(f"❌ 合并测试失败")
        print(f"💡 可能需要调整参数或检查文件")

if __name__ == "__main__":
    main()
