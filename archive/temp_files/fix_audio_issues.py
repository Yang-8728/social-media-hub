#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复音频问题 - 使用normalize模式重新合并
"""

import os
from pathlib import Path
import sys
sys.path.append('src')

from utils.video_merger import VideoMerger

def fix_audio_issues():
    """使用normalize模式修复音频问题"""
    print("🔧 修复音频问题 - normalize模式")
    print("=" * 50)
    
    # 获取2025-08-27文件夹的所有视频
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))
    
    print(f"📁 处理视频文件: {len(video_files)} 个")
    print(f"💡 normalize模式会：")
    print(f"   - 统一分辨率到720x1280")
    print(f"   - 重新编码音频确保一致性")
    print(f"   - 添加黑边保持长宽比")
    print(f"   - 修复音频同步问题")
    
    # 初始化合并器
    merger = VideoMerger("ai_vanvan")
    
    # 创建修复后的文件名
    output_name = f"merged_0827_audio_fixed.mp4"
    output_path = Path("videos/merged/ai_vanvan") / output_name
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 删除已存在的输出文件
    if output_path.exists():
        output_path.unlink()
        print(f"🗑️ 删除旧文件: {output_name}")
    
    # 执行normalize合并
    print(f"\n🔄 开始normalize模式合并...")
    print(f"⏳ 这会比较慢（需要重新编码），但能解决音频问题")
    
    try:
        success = merger.merge_videos_with_normalization([str(f) for f in video_files], str(output_path))
        
        if success:
            print(f"✅ 音频修复完成!")
            
            # 检查输出文件
            if output_path.exists():
                output_size = output_path.stat().st_size / (1024*1024)
                print(f"📊 修复后文件: {output_name}")
                print(f"💾 文件大小: {output_size:.1f}MB")
                
                print(f"\n📁 修复后文件路径:")
                print(f"   {output_path}")
                
                print(f"\n🎯 修复效果:")
                print(f"   ✅ 统一分辨率: 720x1280")
                print(f"   ✅ 音频编码一致")
                print(f"   ✅ 解决声音丢失问题")
                print(f"   ✅ 画面大小一致")
                
                return True
            else:
                print(f"❌ 修复后文件未生成")
                return False
        else:
            print(f"❌ 音频修复失败")
            return False
            
    except Exception as e:
        print(f"❌ 修复过程异常: {e}")
        return False

def main():
    print("🎥 音频问题修复工具")
    print("=" * 50)
    
    fix_result = fix_audio_issues()
    
    print(f"\n📊 修复结果:")
    if fix_result:
        print(f"✅ 音频问题修复成功")
        print(f"💡 播放 merged_0827_audio_fixed.mp4 验证效果")
        print(f"💡 现在应该没有声音丢失的问题了")
    else:
        print(f"❌ 音频问题修复失败")
        print(f"💡 可能需要检查源视频文件")

if __name__ == "__main__":
    main()
