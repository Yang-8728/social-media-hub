#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于原项目的正确合并方法
"""

import os
from pathlib import Path
import subprocess

def merge_with_original_method():
    """使用原项目的方法合并视频"""
    print("🎥 基于原项目的视频合并方法")
    print("=" * 40)
    
    # 获取所有视频文件
    source_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    video_files = sorted(list(source_folder.glob("*.mp4")))
    
    print(f"📹 找到 {len(video_files)} 个视频文件")
    
    # 分批处理，每批8个视频（原项目推荐）
    batch_size = 8
    batch_outputs = []
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    total_batches = (len(video_files) + batch_size - 1) // batch_size
    print(f"📦 将分为 {total_batches} 批处理，每批 {batch_size} 个视频")
    
    # FFmpeg路径
    ffmpeg_exe = "tools/ffmpeg/bin/ffmpeg.exe"
    
    # 第一阶段：分批合并
    for i in range(0, len(video_files), batch_size):
        batch_num = i // batch_size + 1
        batch = video_files[i:i+batch_size]
        batch_output = temp_dir / f"batch_{batch_num}.mp4"
        
        print(f"\\n📦 处理第 {batch_num}/{total_batches} 批，包含 {len(batch)} 个视频")
        
        # 创建文件列表
        list_file = temp_dir / f"batch_{batch_num}_list.txt"
        with open(list_file, "w", encoding="utf-8") as f:
            for video in batch:
                # 原项目的路径处理方法：双反斜杠转义
                abs_path = os.path.abspath(video).replace("\\", "\\\\")
                f.write(f"file '{abs_path}'\n")
        
        # 使用原项目的concat demuxer方法
        cmd = [
            ffmpeg_exe, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(list_file),
            "-c", "copy",  # 关键：直接复制流，不重新编码
            str(batch_output)
        ]
        
        print(f"   🔄 合并批次 {batch_num}...")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and batch_output.exists():
                size_mb = batch_output.stat().st_size / (1024*1024)
                print(f"   ✅ 批次 {batch_num} 合并成功 ({size_mb:.1f}MB)")
                batch_outputs.append(batch_output)
            else:
                print(f"   ❌ 批次 {batch_num} 合并失败")
                print(f"   错误: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"   ❌ 批次 {batch_num} 处理出错: {e}")
            return False
        finally:
            # 清理临时文件列表
            if list_file.exists():
                list_file.unlink()
    
    # 第二阶段：合并所有批次
    if len(batch_outputs) == 1:
        # 只有一个批次，直接重命名
        final_output = "ai_vanvan_0827_original_method.mp4"
        batch_outputs[0].rename(final_output)
        print(f"\\n✅ 单批次处理完成!")
    else:
        print(f"\\n📦 第二阶段：合并 {len(batch_outputs)} 个批次...")
        
        # 创建最终合并的文件列表
        final_list = temp_dir / "final_list.txt"
        with open(final_list, "w", encoding="utf-8") as f:
            for batch_file in batch_outputs:
                abs_path = os.path.abspath(batch_file).replace("\\", "\\\\")
                f.write(f"file '{abs_path}'\n")
        
        final_output = "ai_vanvan_0827_original_method.mp4"
        
        cmd = [
            ffmpeg_exe, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(final_list),
            "-c", "copy",  # 继续使用copy模式
            final_output
        ]
        
        print(f"🔄 最终合并...")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(final_output):
                size_mb = os.path.getsize(final_output) / (1024*1024)
                print(f"✅ 最终合并成功!")
                print(f"📊 输出文件: {final_output}")
                print(f"📊 文件大小: {size_mb:.1f}MB")
            else:
                print(f"❌ 最终合并失败")
                print(f"错误: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 最终合并出错: {e}")
            return False
        finally:
            # 清理最终文件列表
            if final_list.exists():
                final_list.unlink()
    
    # 清理批次文件
    print(f"🧹 清理临时批次文件...")
    for batch_file in batch_outputs:
        if batch_file.exists():
            batch_file.unlink()
    
    print(f"\\n🎯 原项目方法特点:")
    print(f"   ✅ 分批处理 (每批{batch_size}个)")
    print(f"   ✅ 使用 -c copy (直接复制流)")
    print(f"   ✅ 不重新编码 (保持原始质量)")
    print(f"   ✅ 避免大批量处理的内存问题")
    
    return True

if __name__ == "__main__":
    merge_with_original_method()
