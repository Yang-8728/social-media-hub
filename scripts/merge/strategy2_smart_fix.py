#!/usr/bin/env python3
"""
方案2：智能修复 - 只处理有问题的视频然后合并
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
            "-c:v", "copy",      # 视频流直接复制，不重新编码
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

def create_merge_list():
    """创建合并用的视频列表（使用修复后的版本）"""
    # 获取所有视频文件
    video_pattern = os.path.join(VIDEO_DIR, "*.mp4")
    all_videos = sorted(glob.glob(video_pattern))
    
    merge_list = []
    
    for video in all_videos:
        filename = os.path.basename(video)
        
        if filename in PROBLEM_VIDEOS:
            # 使用修复后的版本
            fixed_path = os.path.join("temp_fixed", filename)
            if os.path.exists(fixed_path):
                merge_list.append(fixed_path)
                print(f"  📝 使用修复版: {filename}")
            else:
                print(f"  ⚠️ 修复版不存在，使用原版: {filename}")
                merge_list.append(video)
        else:
            # 使用原版
            merge_list.append(video)
            print(f"  📝 使用原版: {filename}")
    
    return merge_list

def merge_videos_simple(video_files, output_path):
    """简单合并视频（因为已经处理过问题视频）"""
    if not video_files:
        print("❌ 没有视频文件需要合并")
        return False
    
    print(f"\n🔗 合并 {len(video_files)} 个视频:")
    
    # 创建文件列表
    filelist_path = "temp_filelist_strategy2.txt"
    
    try:
        with open(filelist_path, 'w', encoding='utf-8') as f:
            for video in video_files:
                abs_path = os.path.abspath(video).replace('\\', '/')
                f.write(f"file '{abs_path}'\n")
        
        # FFmpeg合并命令
        ffmpeg_exe = os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe")
        cmd = [
            ffmpeg_exe,
            "-f", "concat",
            "-safe", "0",
            "-i", filelist_path,
            "-c", "copy",  # 因为问题视频已修复，可以直接copy
            "-y",
            output_path
        ]
        
        print(f"🚀 开始合并到: {output_path}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            output_size_mb = os.path.getsize(output_path) / (1024*1024)
            print(f"✅ 合并成功! 大小: {output_size_mb:.1f}MB")
            return True
        else:
            print(f"❌ 合并失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 合并出错: {e}")
        return False
    finally:
        if os.path.exists(filelist_path):
            os.remove(filelist_path)

def verify_audio_bitrate(video_path):
    """验证视频的音频比特率"""
    try:
        ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
        cmd = [
            ffprobe_exe,
            "-v", "quiet",
            "-select_streams", "a:0",
            "-show_entries", "stream=bit_rate",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        bitrate = int(result.stdout.strip())
        return bitrate / 1000  # 转换为kbps
    except:
        return 0

def main():
    print("🎯 方案2：智能修复策略")
    print("=" * 50)
    print("📋 处理流程:")
    print("  1. 修复5个问题视频的音频质量")
    print("  2. 与18个正常视频一起合并")
    print("  3. 测试合并结果")
    print()
    
    # 1. 创建临时目录
    temp_dir = "temp_fixed"
    os.makedirs(temp_dir, exist_ok=True)
    
    fixed_videos = []
    
    try:
        # 2. 修复问题视频
        print("🔧 第一步：修复问题视频音频质量")
        print("-" * 40)
        
        for problem_video in PROBLEM_VIDEOS:
            input_path = os.path.join(VIDEO_DIR, problem_video)
            output_path = os.path.join(temp_dir, problem_video)
            
            if not os.path.exists(input_path):
                print(f"  ⚠️ 文件不存在: {problem_video}")
                continue
            
            if fix_problem_video(input_path, output_path):
                # 验证修复效果
                new_bitrate = verify_audio_bitrate(output_path)
                print(f"    ✅ 修复成功，新比特率: {new_bitrate:.0f}kbps")
                fixed_videos.append(output_path)
            else:
                print(f"    ❌ 修复失败: {problem_video}")
        
        print(f"\n📊 修复结果: {len(fixed_videos)}/{len(PROBLEM_VIDEOS)} 个视频修复成功")
        
        # 3. 创建合并列表
        print(f"\n📝 第二步：准备合并列表")
        print("-" * 40)
        merge_list = create_merge_list()
        
        # 4. 合并视频
        print(f"\n🔗 第三步：合并所有视频")
        print("-" * 40)
        output_path = f"merged_strategy2_{len(merge_list)}_videos.mp4"
        
        if merge_videos_simple(merge_list, output_path):
            print(f"\n🎉 方案2完成！")
            print(f"📁 输出文件: {output_path}")
            
            # 显示对比
            print(f"\n📊 修复统计:")
            print(f"  问题视频: {len(PROBLEM_VIDEOS)} 个")
            print(f"  修复成功: {len(fixed_videos)} 个")
            print(f"  正常视频: {len(merge_list) - len(fixed_videos)} 个")
            print(f"  总合并: {len(merge_list)} 个")
            
            print(f"\n🎯 测试建议:")
            print(f"  1. 播放检查1:39位置是否还卡顿")
            print(f"  2. 对比原始合并版本的效果")
            print(f"  3. 检查整体音频质量")
        else:
            print(f"\n❌ 合并失败")
            
    finally:
        # 5. 清理临时文件
        print(f"\n🧹 清理临时文件...")
        for fixed_file in fixed_videos:
            if os.path.exists(fixed_file):
                os.remove(fixed_file)
        if os.path.exists(temp_dir):
            try:
                os.rmdir(temp_dir)
            except:
                pass

if __name__ == "__main__":
    main()
