#!/usr/bin/env python3
"""
方案2改进版：修复问题视频 + 使用--merge逻辑合并
"""
import os
import subprocess
import glob
import shutil

# 基于最新扫描的5个问题视频
PROBLEM_VIDEOS = [
    "2025-04-06_20-06-00_UTC.mp4",  # 44kbps
    "2025-05-12_04-45-50_UTC.mp4",  # 38kbps
    "2025-06-11_18-34-31_UTC.mp4",  # 44kbps (1:39卡顿)
    "2025-06-29_18-58-32_UTC.mp4",  # 38kbps
    "2025-08-20_15-43-46_UTC.mp4"   # 41kbps
]

VIDEO_DIR = "videos/downloads/ai_vanvan/2025-09-01"

def fix_problem_video(input_path, output_path):
    """修复单个问题视频的音频质量"""
    try:
        ffmpeg_exe = os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe")
        
        # 只重新编码音频，保持视频不变
        cmd = [
            ffmpeg_exe,
            "-i", input_path,
            "-c:v", "copy",      # 视频流直接复制
            "-c:a", "aac",       # 音频重新编码为AAC
            "-b:a", "128k",      # 提升音频比特率到128kbps
            "-ar", "44100",      # 保持采样率
            "-y",                # 覆盖输出文件
            output_path
        ]
        
        print(f"  🔧 修复音频: {os.path.basename(input_path)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            print(f"  ❌ 修复失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ 修复出错: {e}")
        return False

def get_video_resolution(video_path):
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

def find_target_resolution(video_files):
    """分析所有视频，找到最适合的目标分辨率"""
    resolutions = {}
    
    for video in video_files:
        width, height = get_video_resolution(video)
        if width and height:
            # 判断是横屏还是竖屏
            if height > width:  # 竖屏
                if width >= 720:
                    target = (720, 1280)  # 720p竖屏
                else:
                    target = (540, 960)   # 较小竖屏
            else:  # 横屏
                if width >= 1280:
                    target = (1280, 720)  # 720p横屏
                else:
                    target = (960, 540)   # 较小横屏
                    
            resolutions[target] = resolutions.get(target, 0) + 1
    
    if not resolutions:
        return 720, 1280
        
    target = max(resolutions.items(), key=lambda x: x[1])[0]
    print(f"🎯 检测到目标分辨率: {target[0]}x{target[1]} (出现{resolutions[target]}次)")
    return target

def normalize_video_resolution(input_path, output_path, target_width, target_height):
    """统一视频分辨率和编码参数（--merge逻辑）"""
    try:
        ffmpeg_exe = os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe")
        
        # 完整的重新编码（--merge逻辑）
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
            print(f"❌ 标准化失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 标准化出错: {e}")
        return False

def merge_videos_with_ffmpeg(video_files, output_path):
    """使用FFmpeg合并已标准化的视频（--merge逻辑第二阶段）"""
    if not video_files:
        print("⚠️ 没有视频文件需要合并")
        return False
    
    print(f"🔗 准备合并 {len(video_files)} 个标准化视频")
    
    filelist_path = "temp_filelist_strategy2_fixed.txt"
    
    try:
        with open(filelist_path, 'w', encoding='utf-8') as f:
            for video in video_files:
                abs_path = os.path.abspath(video).replace('\\', '/')
                f.write(f"file '{abs_path}'\n")
        
        ffmpeg_exe = os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe")
        cmd = [
            ffmpeg_exe,
            "-f", "concat",
            "-safe", "0",
            "-i", filelist_path,
            "-c", "copy",  # 现在安全了，因为所有视频已标准化
            "-y",
            output_path
        ]
        
        print(f"🚀 开始合并视频到: {output_path}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
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
        if os.path.exists(filelist_path):
            os.remove(filelist_path)

def create_mixed_video_list():
    """创建混合视频列表（修复后的问题视频 + 原始正常视频）"""
    video_pattern = os.path.join(VIDEO_DIR, "*.mp4")
    all_videos = sorted(glob.glob(video_pattern))
    
    mixed_list = []
    
    for video in all_videos:
        filename = os.path.basename(video)
        
        if filename in PROBLEM_VIDEOS:
            # 使用修复后的版本
            fixed_path = os.path.join("temp_fixed", filename)
            if os.path.exists(fixed_path):
                mixed_list.append(fixed_path)
                print(f"  📝 使用修复版: {filename}")
            else:
                print(f"  ⚠️ 修复版不存在，使用原版: {filename}")
                mixed_list.append(video)
        else:
            # 使用原版
            mixed_list.append(video)
            print(f"  📝 使用原版: {filename}")
    
    return mixed_list

def main():
    print("🎯 方案2改进版：修复问题视频 + --merge逻辑合并")
    print("=" * 60)
    print("📋 处理流程:")
    print("  1. 修复5个问题视频的音频质量")
    print("  2. 使用--merge逻辑统一所有视频编码参数")
    print("  3. 安全合并（避免DTS时间戳问题）")
    print()
    
    # 1. 创建临时目录
    temp_fixed_dir = "temp_fixed"
    temp_normalized_dir = "temp_normalized_strategy2"
    os.makedirs(temp_fixed_dir, exist_ok=True)
    os.makedirs(temp_normalized_dir, exist_ok=True)
    
    fixed_videos = []
    normalized_files = []
    
    try:
        # 第一步：修复问题视频
        print("🔧 第一步：修复问题视频音频质量")
        print("-" * 50)
        
        for problem_video in PROBLEM_VIDEOS:
            input_path = os.path.join(VIDEO_DIR, problem_video)
            output_path = os.path.join(temp_fixed_dir, problem_video)
            
            if not os.path.exists(input_path):
                print(f"  ⚠️ 文件不存在: {problem_video}")
                continue
            
            if fix_problem_video(input_path, output_path):
                print(f"    ✅ 修复成功: {problem_video}")
                fixed_videos.append(output_path)
            else:
                print(f"    ❌ 修复失败: {problem_video}")
        
        print(f"\n📊 音频修复结果: {len(fixed_videos)}/{len(PROBLEM_VIDEOS)} 个视频修复成功")
        
        # 第二步：准备混合视频列表
        print(f"\n📝 第二步：准备混合视频列表")
        print("-" * 50)
        mixed_list = create_mixed_video_list()
        
        # 第三步：分析目标分辨率
        print(f"\n🎯 第三步：分析目标分辨率")
        print("-" * 50)
        target_width, target_height = find_target_resolution(mixed_list)
        
        # 第四步：统一编码参数（--merge逻辑第一阶段）
        print(f"\n🔄 第四步：统一所有视频编码参数")
        print("-" * 50)
        
        for i, video in enumerate(mixed_list):
            temp_output = os.path.join(temp_normalized_dir, f"normalized_{i:03d}.mp4")
            
            print(f"  标准化 ({i+1}/{len(mixed_list)}): {os.path.basename(video)}")
            
            if normalize_video_resolution(video, temp_output, target_width, target_height):
                normalized_files.append(temp_output)
            else:
                print(f"⚠️ 跳过标准化失败的视频: {video}")
        
        print(f"\n📊 标准化结果: {len(normalized_files)}/{len(mixed_list)} 个视频标准化成功")
        
        if not normalized_files:
            print("❌ 没有成功标准化的视频")
            return
        
        # 第五步：安全合并（--merge逻辑第二阶段）
        print(f"\n🔗 第五步：安全合并标准化后的视频")
        print("-" * 50)
        output_path = f"merged_strategy2_fixed_{len(normalized_files)}_videos.mp4"
        
        if merge_videos_with_ffmpeg(normalized_files, output_path):
            print(f"\n🎉 方案2改进版完成！")
            print(f"📁 输出文件: {output_path}")
            
            # 显示统计
            output_size_mb = os.path.getsize(output_path) / (1024*1024)
            print(f"\n📊 处理统计:")
            print(f"  问题视频修复: {len(fixed_videos)} 个")
            print(f"  标准化视频: {len(normalized_files)} 个")
            print(f"  最终文件大小: {output_size_mb:.1f}MB")
            
            print(f"\n🎯 测试要点:")
            print(f"  1. 检查1:39位置是否解决卡顿")
            print(f"  2. 验证整个视频音频连续性")
            print(f"  3. 对比之前版本的改善效果")
        else:
            print(f"\n❌ 合并失败")
            
    finally:
        # 清理临时文件
        print(f"\n🧹 清理临时文件...")
        for temp_file in fixed_videos + normalized_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        for temp_dir in [temp_fixed_dir, temp_normalized_dir]:
            if os.path.exists(temp_dir):
                try:
                    os.rmdir(temp_dir)
                except:
                    pass

if __name__ == "__main__":
    main()
