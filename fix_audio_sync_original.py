#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于原项目修复方案的音频同步合并工具
"""

import os
from pathlib import Path
import subprocess
import sys
sys.path.append('src')

from utils.video_merger import VideoMerger

def merge_with_audio_sync_fix(video_files, output_path):
    """使用原项目的修复方案合并视频，解决音频同步问题"""
    
    print("🔧 使用原项目修复方案")
    print("=" * 50)
    
    # 创建临时文件列表
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    filelist_path = temp_dir / "concat_list.txt"
    
    try:
        # 写入文件列表，使用绝对路径并正确转义
        with open(filelist_path, 'w', encoding='utf-8') as f:
            for video in video_files:
                # 使用绝对路径，转义为正斜杠（更安全）
                abs_path = os.path.abspath(video).replace('\\', '/')
                f.write(f"file '{abs_path}'\n")
        
        print(f"📝 创建文件列表: {filelist_path}")
        print(f"📹 准备合并 {len(video_files)} 个视频")
        
        # 显示前5个文件
        for i, video in enumerate(video_files[:5], 1):
            size_mb = Path(video).stat().st_size / (1024*1024)
            print(f"   {i}. {Path(video).name} ({size_mb:.1f}MB)")
        if len(video_files) > 5:
            print(f"   ... 及其他 {len(video_files) - 5} 个文件")
        
        # FFmpeg命令 - 使用原项目的参数组合
        ffmpeg_paths = [
            "tools/ffmpeg/bin/ffmpeg.exe",
            "ffmpeg"
        ]
        
        ffmpeg_exe = None
        for path in ffmpeg_paths:
            if os.path.exists(path):
                ffmpeg_exe = path
                break
        
        if not ffmpeg_exe:
            ffmpeg_exe = "ffmpeg"
        
        # 使用原项目验证过的命令参数
        cmd = [
            ffmpeg_exe, "-y",
            "-f", "concat",
            "-safe", "0", 
            "-i", str(filelist_path),
            "-c", "copy",  # 直接复制编解码器，不重新编码
            str(output_path)
        ]
        
        print(f"\\n🔄 开始合并...")
        print(f"💡 使用参数: -f concat -safe 0 -c copy")
        
        # 执行FFmpeg命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_path):
                output_size = os.path.getsize(output_path) / (1024*1024)
                print(f"✅ 合并成功! 输出文件大小: {output_size:.1f}MB")
                return True
            else:
                print(f"❌ 合并失败: 输出文件未创建")
                return False
        else:
            print(f"❌ FFmpeg执行失败:")
            print(f"错误输出: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 合并过程出错: {e}")
        return False
    finally:
        # 清理临时文件
        if filelist_path.exists():
            filelist_path.unlink()

def merge_in_batches(video_files, output_path, batch_size=10):
    """分批合并视频，避免大文件合并问题"""
    print(f"🔄 分批合并模式 (每批 {batch_size} 个视频)")
    print("=" * 50)
    
    if len(video_files) <= batch_size:
        # 文件数量少，直接合并
        return merge_with_audio_sync_fix(video_files, output_path)
    
    # 分批处理
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    batch_outputs = []
    total_batches = (len(video_files) + batch_size - 1) // batch_size
    
    try:
        for i in range(0, len(video_files), batch_size):
            batch = video_files[i:i+batch_size]
            batch_num = i // batch_size + 1
            batch_output = temp_dir / f"batch_{batch_num}.mp4"
            
            print(f"\\n📦 处理批次 {batch_num}/{total_batches} (包含 {len(batch)} 个视频)")
            
            if merge_with_audio_sync_fix(batch, str(batch_output)):
                batch_outputs.append(str(batch_output))
                print(f"✅ 批次 {batch_num} 完成")
            else:
                print(f"❌ 批次 {batch_num} 失败")
                return False
        
        # 合并所有批次
        if len(batch_outputs) == 1:
            # 只有一个批次，直接重命名
            import shutil
            shutil.move(batch_outputs[0], output_path)
            print(f"✅ 单批次完成，重命名为最终文件")
            return True
        else:
            print(f"\\n🔄 合并 {len(batch_outputs)} 个批次...")
            return merge_with_audio_sync_fix(batch_outputs, output_path)
            
    finally:
        # 清理批次文件
        for batch_file in batch_outputs:
            if os.path.exists(batch_file):
                os.remove(batch_file)

def fix_audio_sync_0827():
    """使用原项目修复方案合并2025-08-27的视频"""
    print("🎥 音频同步修复工具 (基于原项目方案)")
    print("=" * 50)
    
    # 获取2025-08-27文件夹的所有视频
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))
    
    if not video_files:
        print("❌ 未找到视频文件")
        return
    
    print(f"📁 找到 {len(video_files)} 个视频文件")
    
    # 创建输出文件
    output_name = "merged_0827_sync_fixed.mp4"
    output_path = Path("videos/merged/ai_vanvan") / output_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 删除已存在的输出文件
    if output_path.exists():
        output_path.unlink()
        print(f"🗑️ 删除旧文件: {output_name}")
    
    # 执行分批合并
    print(f"\\n🔄 开始修复合并...")
    
    video_paths = [str(f) for f in video_files]
    success = merge_in_batches(video_paths, str(output_path), batch_size=8)
    
    if success:
        print(f"\\n🎉 音频同步修复完成!")
        print(f"📁 输出文件: {output_path}")
        print(f"💡 这个版本应该解决了音频同步问题")
        
        # 显示文件信息
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024*1024)
            print(f"📊 文件大小: {size_mb:.1f}MB")
        
    else:
        print(f"\\n❌ 音频同步修复失败")

def main():
    fix_audio_sync_0827()

if __name__ == "__main__":
    main()
