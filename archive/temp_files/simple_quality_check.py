#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Python简单检查视频质量问题
检查文件大小、时长估算等基本信息
"""

import os
from pathlib import Path
import time

def simple_video_check(video_path):
    """简单检查视频文件基本信息"""
    print(f"\n🔍 检查视频: {os.path.basename(video_path)}")
    print("=" * 60)
    
    try:
        # 文件信息
        stat = os.stat(video_path)
        file_size = stat.st_size
        mod_time = time.ctime(stat.st_mtime)
        
        print(f"📦 文件大小: {file_size / 1024 / 1024:.1f}MB")
        print(f"📅 修改时间: {mod_time}")
        
        # 基于文件大小估算质量
        size_mb = file_size / 1024 / 1024
        
        if size_mb < 1:
            print("⚠️  文件很小，可能质量有问题")
        elif size_mb > 100:
            print("✅ 文件大小正常，质量应该不错")
        elif size_mb > 50:
            print("✅ 文件大小适中")
        else:
            print("📊 文件大小偏小，需要进一步检查")
        
        # 尝试读取文件头部检查是否损坏
        with open(video_path, 'rb') as f:
            header = f.read(8)
            if header.startswith(b'\x00\x00\x00'):
                # MP4文件头
                f.seek(4)
                ftype = f.read(4)
                if ftype == b'ftyp':
                    print("✅ MP4文件头正常")
                else:
                    print("⚠️  文件头可能有问题")
            else:
                print("⚠️  文件格式可能有问题")
        
        # 检查文件名中的信息
        filename = os.path.basename(video_path)
        if 'merged' in filename:
            print("📹 这是合并后的视频")
            if 'videos' in filename:
                # 提取合并的视频数量
                parts = filename.split('_')
                for part in parts:
                    if 'videos' in part and part.replace('videos', '').isdigit():
                        count = part.replace('videos', '')
                        print(f"🔢 合并了 {count} 个视频")
                        
                        # 估算平均每个视频的大小
                        avg_size = size_mb / int(count)
                        print(f"📊 平均每个原视频: {avg_size:.1f}MB")
                        
                        if avg_size < 0.5:
                            print("⚠️  原视频可能很短或质量低")
                        elif avg_size > 5:
                            print("✅ 原视频质量应该不错")
        
        return True
    
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

def check_for_common_issues():
    """检查常见问题的迹象"""
    print("\n🔍 常见问题检查:")
    print("-" * 30)
    
    # 检查是否有临时文件或错误日志
    temp_files = list(Path(".").glob("*.tmp"))
    error_logs = list(Path(".").glob("*error*.log"))
    
    if temp_files:
        print(f"⚠️  发现 {len(temp_files)} 个临时文件，可能有未完成的操作")
    
    if error_logs:
        print(f"⚠️  发现错误日志文件，可能有处理问题")
    
    # 检查视频合并的设置
    print("\n📋 视频质量问题排查清单:")
    print("1. 🎬 跳帧问题:")
    print("   - 原因: 源视频帧率不一致、编码器设置问题")
    print("   - 检查: 播放时是否有卡顿、快进感")
    
    print("\n2. 🔇 音频问题:")
    print("   - 原因: 音频编码器设置、流映射问题")
    print("   - 检查: 是否完全无声音或音量很低")
    
    print("\n3. 🎭 音视频不同步:")
    print("   - 原因: 时间戳处理、编码延迟")
    print("   - 检查: 说话和嘴型是否对得上")
    
    print("\n4. 📺 画质降级:")
    print("   - 原因: 重编码、比特率过低")
    print("   - 检查: 是否比原视频模糊")

def main():
    print("🔍 简单视频质量检查")
    print("=" * 50)
    
    # 检查合并视频目录
    merged_dir = Path("videos/merged/ai_vanvan")
    
    if not merged_dir.exists():
        print("❌ 合并视频目录不存在")
        return
    
    # 查找所有视频文件
    video_files = list(merged_dir.glob("*.mp4"))
    
    if not video_files:
        print("❌ 未找到合并后的视频文件")
        return
    
    print(f"📁 找到 {len(video_files)} 个视频文件")
    
    # 逐个检查
    success_count = 0
    for video_file in video_files:
        if simple_video_check(str(video_file)):
            success_count += 1
    
    print(f"\n✅ 成功检查了 {success_count}/{len(video_files)} 个视频")
    
    # 常见问题指南
    check_for_common_issues()
    
    print("\n" + "=" * 50)
    print("💡 建议:")
    print("1. 手动播放一个视频文件检查是否有明显问题")
    print("2. 如果发现问题，检查原始视频质量")
    print("3. 考虑调整FFmpeg合并参数")
    print("4. 必要时重新下载质量有问题的原始视频")

if __name__ == "__main__":
    main()
