#!/usr/bin/env python3
"""
修复版合并脚本 - 使用正确的两阶段合并逻辑
1. 先统一编码参数（解决DTS问题）
2. 再使用concat合并
"""
import os
import subprocess
import glob
from pathlib import Path
import tempfile
import shutil

# 视频目录
VIDEO_DIR = "videos/downloads/ai_vanvan/2025-09-01"

# 只排除重复的视频，保留所有其他视频（包括有问题的）
EXCLUDED_VIDEOS = [
    # 只排除重复文件
    "2025-08-19_09-56-05_UTC (1).mp4",  # 重复文件
    "2025-08-19_10-05-11_UTC (1).mp4"   # 重复文件
]

def get_video_resolution(video_path: str) -> tuple:
    """获取视频分辨率"""
    try:
        ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
        cmd = [
            ffprobe_exe,
            "-v", "quiet",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=p=0",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        width, height = result.stdout.strip().split(',')
        return int(width), int(height)
    except Exception as e:
        print(f"⚠️ 无法获取视频分辨率 {video_path}: {e}")
        return None, None

def find_target_resolution(video_files: list) -> tuple:
    """分析所有视频，找到最适合的目标分辨率"""
    resolutions = {}
    
    for video in video_files:
        width, height = get_video_resolution(video)
        if width and height:
            # 判断是横屏还是竖屏
            if height > width:  # 竖屏
                # 标准化竖屏分辨率
                if width >= 720:
                    target = (720, 1280)  # 720p竖屏
                else:
                    target = (540, 960)   # 较小竖屏
            else:  # 横屏
                # 标准化横屏分辨率
                if width >= 1280:
                    target = (1280, 720)  # 720p横屏
                else:
                    target = (960, 540)   # 较小横屏
                    
            resolutions[target] = resolutions.get(target, 0) + 1
    
    if not resolutions:
        # 默认竖屏分辨率(Instagram常用)
        return 720, 1280
        
    # 返回最常见的分辨率
    target = max(resolutions.items(), key=lambda x: x[1])[0]
    print(f"🎯 检测到目标分辨率: {target[0]}x{target[1]} (出现{resolutions[target]}次)")
    return target

def normalize_video_resolution(input_path: str, output_path: str, target_width: int, target_height: int) -> bool:
    """统一视频分辨率，保持长宽比，添加黑边"""
    try:
        ffmpeg_exe = os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe")
        
        # FFmpeg命令：缩放并添加黑边，重新编码统一参数
        cmd = [
            ffmpeg_exe,
            "-i", input_path,
            "-vf", f"scale={target_width}:{target_height}:force_original_aspect_ratio=decrease,pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2:black",
            "-c:v", "libx264",
            "-crf", "23",
            "-preset", "medium",
            "-c:a", "aac",
            "-b:a", "128k",
            "-y",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print(f"❌ 视频标准化失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 视频标准化出错: {e}")
        return False

def merge_videos_with_ffmpeg(video_files: list, output_path: str) -> bool:
    """使用FFmpeg合并已标准化的视频"""
    if not video_files:
        print("⚠️ 没有视频文件需要合并")
        return False
    
    print(f"🔗 准备合并 {len(video_files)} 个标准化视频:")
    for i, video in enumerate(video_files, 1):
        size_mb = os.path.getsize(video) / (1024*1024)
        print(f"  {i}. {os.path.basename(video)} ({size_mb:.1f}MB)")
    
    # 创建临时文件列表
    filelist_path = "temp_filelist_fixed.txt"
    
    try:
        # 写入文件列表
        with open(filelist_path, 'w', encoding='utf-8') as f:
            for video in video_files:
                # 使用绝对路径并转义
                abs_path = os.path.abspath(video).replace('\\', '/')
                f.write(f"file '{abs_path}'\n")
        
        # FFmpeg合并命令（现在安全使用copy因为已标准化）
        ffmpeg_exe = os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe")
        cmd = [
            ffmpeg_exe,
            "-f", "concat",
            "-safe", "0",
            "-i", filelist_path,
            "-c", "copy",  # 现在安全了！
            "-y",
            output_path
        ]
        
        print(f"🚀 开始合并视频到: {output_path}")
        
        # 执行FFmpeg命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # 计算输出文件大小
            output_size_mb = os.path.getsize(output_path) / (1024*1024)
            print(f"✅ 合并成功! 输出文件: {output_path} ({output_size_mb:.1f}MB)")
            return True
        else:
            print(f"❌ FFmpeg合并失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 合并过程出错: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(filelist_path):
            os.remove(filelist_path)

def main():
    print("🎬 修复版视频合并脚本")
    print("=" * 50)
    
    # 1. 获取所有视频文件
    video_pattern = os.path.join(VIDEO_DIR, "*.mp4")
    all_videos = sorted(glob.glob(video_pattern))
    
    if not all_videos:
        print(f"❌ 在 {VIDEO_DIR} 中没有找到视频文件")
        return
    
    print(f"📁 找到 {len(all_videos)} 个视频文件")
    
    # 2. 过滤掉问题视频和重复视频
    good_videos = []
    for video in all_videos:
        filename = os.path.basename(video)
        if filename not in EXCLUDED_VIDEOS:
            good_videos.append(video)
        else:
            print(f"⏭️ 跳过排除视频: {filename}")
    
    print(f"✅ 将合并 {len(good_videos)} 个视频（包括有问题的视频，目标：27个）")
    
    # 3. 分析目标分辨率
    target_width, target_height = find_target_resolution(good_videos)
    
    # 4. 创建临时目录
    temp_dir = "temp_normalized_fixed"
    os.makedirs(temp_dir, exist_ok=True)
    
    normalized_files = []
    
    try:
        # 5. 标准化所有视频
        print("\n🔄 第一阶段：标准化视频编码参数...")
        for i, video in enumerate(good_videos):
            temp_output = os.path.join(temp_dir, f"normalized_{i:03d}.mp4")
            
            print(f"  标准化 ({i+1}/{len(good_videos)}): {os.path.basename(video)}")
            
            if normalize_video_resolution(video, temp_output, target_width, target_height):
                normalized_files.append(temp_output)
            else:
                print(f"⚠️ 跳过标准化失败的视频: {video}")
        
        if not normalized_files:
            print("❌ 没有成功标准化的视频")
            return
            
        print(f"✅ 标准化完成，共 {len(normalized_files)} 个文件")
        
        # 6. 合并标准化后的视频
        print("\n🔗 第二阶段：合并标准化后的视频...")
        output_path = f"merged_videos_fixed_{len(normalized_files)}_videos.mp4"
        
        if merge_videos_with_ffmpeg(normalized_files, output_path):
            print(f"\n🎉 合并完成！输出文件: {output_path}")
            
            # 显示对比信息
            original_size = sum(os.path.getsize(v) for v in good_videos) / (1024*1024)
            merged_size = os.path.getsize(output_path) / (1024*1024)
            print(f"📊 大小对比:")
            print(f"  原始文件总大小: {original_size:.1f}MB")
            print(f"  合并后文件大小: {merged_size:.1f}MB")
            print(f"  压缩比: {merged_size/original_size:.1%}")
        else:
            print("❌ 合并失败")
            
    finally:
        # 7. 清理临时文件
        print("\n🧹 清理临时文件...")
        for temp_file in normalized_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)

if __name__ == "__main__":
    main()
