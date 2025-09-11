#!/usr/bin/env python3
"""
终极版合并脚本 - 完整的--merge逻辑 + 全面修复
1. 全部视频转换为AAC 128kbps
2. 修复负数时间戳问题
3. 统一所有编码参数
4. 使用--merge逻辑安全合并
"""
import os
import subprocess
import glob
import time

VIDEO_DIR = "videos/downloads/ai_vanvan/2025-09-01"

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

def ultimate_video_standardization(input_path, output_path, target_width, target_height):
    """终极视频标准化：修复所有问题并统一参数"""
    try:
        ffmpeg_exe = os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe")
        
        # 终极修复命令
        cmd = [
            ffmpeg_exe,
            "-i", input_path,
            # 修复时间戳问题
            "-avoid_negative_ts", "make_zero",      # 将负时间戳设为0
            "-fflags", "+genpts",                   # 重新生成时间戳
            # 视频处理
            "-vf", f"scale={target_width}:{target_height}:force_original_aspect_ratio=decrease,pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2:black",
            "-c:v", "libx264",                      # 统一视频编码
            "-crf", "23",                           # 高质量
            "-preset", "medium",                    # 平衡速度和质量
            "-profile:v", "high",                   # 高配置
            "-level", "4.0",                        # 兼容性级别
            "-pix_fmt", "yuv420p",                  # 统一像素格式
            "-r", "30",                             # 统一帧率为30fps
            # 音频处理
            "-c:a", "aac",                          # 统一音频编码
            "-b:a", "128k",                         # 统一音频比特率
            "-ar", "44100",                         # 统一采样率
            "-ac", "2",                             # 统一声道数
            "-sample_fmt", "fltp",                  # 统一音频格式
            # 其他修复参数
            "-max_muxing_queue_size", "1024",       # 增大缓冲区
            "-vsync", "1",                          # 视频同步
            "-async", "1",                          # 音频同步
            "-y",                                   # 覆盖输出
            output_path
        ]
        
        print(f"  🔧 标准化: {os.path.basename(input_path)}")
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        process_time = time.time() - start_time
        
        if result.returncode == 0:
            # 验证输出文件
            if os.path.exists(output_path):
                output_size_mb = os.path.getsize(output_path) / (1024*1024)
                print(f"    ✅ 成功 ({process_time:.1f}s, {output_size_mb:.1f}MB)")
                return True
            else:
                print(f"    ❌ 输出文件不存在")
                return False
        else:
            print(f"    ❌ 失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"    ❌ 出错: {e}")
        return False

def merge_standardized_videos(video_files, output_path):
    """合并已标准化的视频（安全的concat）"""
    if not video_files:
        print("⚠️ 没有视频文件需要合并")
        return False
    
    print(f"\n🔗 合并 {len(video_files)} 个标准化视频:")
    for i, video in enumerate(video_files, 1):
        size_mb = os.path.getsize(video) / (1024*1024)
        print(f"  {i:2d}. {os.path.basename(video)} ({size_mb:.1f}MB)")
    
    filelist_path = "temp_filelist_ultimate.txt"
    
    try:
        # 创建文件列表
        with open(filelist_path, 'w', encoding='utf-8') as f:
            for video in video_files:
                abs_path = os.path.abspath(video).replace('\\', '/')
                f.write(f"file '{abs_path}'\n")
        
        # FFmpeg合并命令（现在绝对安全）
        ffmpeg_exe = os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe")
        cmd = [
            ffmpeg_exe,
            "-f", "concat",
            "-safe", "0",
            "-i", filelist_path,
            "-c", "copy",                           # 安全复制，因为已完全标准化
            "-avoid_negative_ts", "make_zero",      # 额外保险
            "-y",
            output_path
        ]
        
        print(f"\n🚀 开始合并到: {output_path}")
        start_time = time.time()
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        merge_time = time.time() - start_time
        
        if result.returncode == 0:
            output_size_mb = os.path.getsize(output_path) / (1024*1024)
            print(f"✅ 合并成功! ({merge_time:.1f}s)")
            print(f"📁 输出文件: {output_path} ({output_size_mb:.1f}MB)")
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

def verify_final_video(video_path):
    """验证最终合并视频的质量"""
    try:
        ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
        
        # 获取基本信息
        cmd = [
            ffprobe_exe,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        import json
        data = json.loads(result.stdout)
        
        format_info = data.get('format', {})
        duration = float(format_info.get('duration', 0))
        file_size_mb = os.path.getsize(video_path) / (1024*1024)
        
        print(f"\n📊 最终视频验证:")
        print(f"  文件大小: {file_size_mb:.1f}MB")
        print(f"  总时长: {duration:.1f}秒 ({duration/60:.1f}分钟)")
        
        # 视频流信息
        video_streams = [s for s in data.get('streams', []) if s.get('codec_type') == 'video']
        if video_streams:
            v = video_streams[0]
            print(f"  视频: {v.get('codec_name')} {v.get('width')}x{v.get('height')}")
            if 'avg_frame_rate' in v:
                fps_str = v['avg_frame_rate']
                if '/' in fps_str:
                    num, den = fps_str.split('/')
                    fps = float(num) / float(den) if float(den) != 0 else 0
                    print(f"  帧率: {fps:.2f}fps")
        
        # 音频流信息
        audio_streams = [s for s in data.get('streams', []) if s.get('codec_type') == 'audio']
        if audio_streams:
            a = audio_streams[0]
            bitrate = int(a.get('bit_rate', 0)) / 1000 if a.get('bit_rate') else 0
            print(f"  音频: {a.get('codec_name')} {bitrate:.0f}kbps {a.get('sample_rate')}Hz")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

def main():
    print("🎯 终极版视频合并脚本")
    print("=" * 60)
    print("📋 完整处理流程:")
    print("  1. 全部视频转换AAC 128kbps")
    print("  2. 修复负数时间戳问题")
    print("  3. 统一所有编码参数")
    print("  4. 统一分辨率和帧率")
    print("  5. 使用--merge逻辑安全合并")
    print()
    
    # 获取所有视频文件
    video_pattern = os.path.join(VIDEO_DIR, "*.mp4")
    all_videos = sorted(glob.glob(video_pattern))
    
    if not all_videos:
        print(f"❌ 在 {VIDEO_DIR} 中没有找到视频文件")
        return
    
    print(f"📁 找到 {len(all_videos)} 个视频文件")
    
    # 分析目标分辨率
    target_width, target_height = find_target_resolution(all_videos)
    
    # 创建临时目录
    temp_dir = "temp_ultimate_standardized"
    os.makedirs(temp_dir, exist_ok=True)
    
    standardized_files = []
    
    try:
        # 第一阶段：完全标准化所有视频
        print(f"\n🔄 第一阶段：完全标准化所有视频")
        print("-" * 60)
        
        total_start_time = time.time()
        
        for i, video in enumerate(all_videos):
            temp_output = os.path.join(temp_dir, f"ultimate_{i:03d}.mp4")
            
            print(f"  处理 ({i+1}/{len(all_videos)}):", end=" ")
            
            if ultimate_video_standardization(video, temp_output, target_width, target_height):
                standardized_files.append(temp_output)
            else:
                print(f"⚠️ 跳过标准化失败的视频: {os.path.basename(video)}")
        
        total_process_time = time.time() - total_start_time
        
        print(f"\n📊 第一阶段完成:")
        print(f"  标准化成功: {len(standardized_files)}/{len(all_videos)} 个")
        print(f"  处理时间: {total_process_time/60:.1f}分钟")
        
        if not standardized_files:
            print("❌ 没有成功标准化的视频")
            return
        
        # 第二阶段：安全合并
        print(f"\n🔗 第二阶段：安全合并标准化视频")
        print("-" * 60)
        
        output_path = f"ultimate_merged_{len(standardized_files)}_videos.mp4"
        
        if merge_standardized_videos(standardized_files, output_path):
            # 验证最终结果
            verify_final_video(output_path)
            
            total_time = time.time() - total_start_time
            
            print(f"\n🎉 终极版合并完成！")
            print(f"📁 输出文件: {output_path}")
            print(f"⏱️ 总处理时间: {total_time/60:.1f}分钟")
            print(f"\n🎯 关键测试点:")
            print(f"  1. 检查1:39位置是否完全解决")
            print(f"  2. 验证全程音频连续性")
            print(f"  3. 检查视频画质统一性")
            print(f"  4. 测试完整播放无卡顿")
        else:
            print(f"\n❌ 合并失败")
            
    finally:
        # 清理临时文件
        print(f"\n🧹 清理临时文件...")
        for temp_file in standardized_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        if os.path.exists(temp_dir):
            try:
                os.rmdir(temp_dir)
            except:
                pass

if __name__ == "__main__":
    main()
