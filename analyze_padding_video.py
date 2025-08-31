#!/usr/bin/env python3
import os

def analyze_merged_video():
    """分析合并后的视频，找出加黑边视频的时间段"""
    
    output_file = "test_resolution_normalization.mp4"
    
    if not os.path.exists(output_file):
        print(f"❌ 合并视频不存在: {output_file}")
        return
    
    # 原始视频信息
    video_info = [
        {
            "file": "2025-03-05_15-32-07_UTC.mp4",
            "resolution": "576x1024",
            "size_mb": 0.7,
            "needs_padding": True,  # 这个需要加黑边
            "position": 1
        },
        {
            "file": "2025-08-08_11-23-16_UTC.mp4", 
            "resolution": "720x1280",
            "size_mb": 32.0,
            "needs_padding": False,
            "position": 2
        },
        {
            "file": "2025-08-15_17-44-44_UTC.mp4",
            "resolution": "720x1280", 
            "size_mb": 10.6,
            "needs_padding": False,
            "position": 3
        },
        {
            "file": "2025-08-26_12-57-05_UTC.mp4",
            "resolution": "720x1280",
            "size_mb": 0.4,
            "needs_padding": False,
            "position": 4
        },
        {
            "file": "2025-07-26_16-58-23_UTC.mp4",
            "resolution": "720x1280",
            "size_mb": 6.2,
            "needs_padding": False,
            "position": 5
        }
    ]
    
    output_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    
    print("📹 合并视频分析结果")
    print("=" * 50)
    print(f"输出文件: {output_file}")
    print(f"输出大小: {output_size_mb:.1f}MB")
    print()
    
    print("🎬 视频序列（按合并顺序）:")
    print()
    
    estimated_time = 0
    
    for video in video_info:
        # 根据文件大小粗略估算视频时长（假设码率相近）
        estimated_duration = video["size_mb"] * 8  # 简单估算，秒数
        
        start_time = estimated_time
        end_time = estimated_time + estimated_duration
        
        status = "⚠️  需要加黑边" if video["needs_padding"] else "✅ 标准分辨率"
        
        print(f"📍 第{video['position']}个视频: {video['file']}")
        print(f"   原始分辨率: {video['resolution']}")
        print(f"   文件大小: {video['size_mb']}MB")
        print(f"   状态: {status}")
        print(f"   预计时间段: {start_time:.0f}秒 - {end_time:.0f}秒")
        
        if video["needs_padding"]:
            print(f"   🎯 这就是加黑边的视频！在合并后的开头部分")
            print(f"   💡 观看提示: 视频开始后的前{estimated_duration:.0f}秒应该有黑边")
        
        print()
        estimated_time = end_time
    
    print("🔍 观看指南:")
    print("1. 播放 test_resolution_normalization.mp4")
    print("2. 开头的第一段视频(2025-03-05)应该有黑边填充")
    print("3. 原分辨率是576x1280，会在左右两边加黑边变成720x1280")
    print("4. 后面4个视频都是标准720x1280，不应该有黑边")
    print()
    
    padding_video = next(v for v in video_info if v["needs_padding"])
    print(f"⭐ 重点: 需要加黑边的视频是第{padding_video['position']}个")
    print(f"   文件名: {padding_video['file']}")
    print(f"   位置: 合并视频的开头部分")

if __name__ == "__main__":
    analyze_merged_video()
