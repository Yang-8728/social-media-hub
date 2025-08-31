#!/usr/bin/env python3
import os
import sys
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def merge_videos_with_moviepy(video_files, output_file):
    """使用moviepy合并视频（带分辨率标准化）"""
    try:
        from moviepy.editor import VideoFileClip, concatenate_videoclips
        from moviepy.video.fx.all import resize
        
        logger.info("使用moviepy进行视频合并...")
        
        clips = []
        target_size = (720, 1280)  # 目标分辨率
        
        for i, video_file in enumerate(video_files):
            logger.info(f"处理视频 {i+1}: {os.path.basename(video_file)}")
            
            if not os.path.exists(video_file):
                logger.error(f"视频文件不存在: {video_file}")
                continue
                
            clip = VideoFileClip(video_file)
            logger.info(f"原始分辨率: {clip.size}")
            
            # 标准化分辨率（保持比例，添加黑边）
            clip_resized = clip.resize(target_size)
            clips.append(clip_resized)
        
        if not clips:
            logger.error("没有有效的视频片段")
            return False
            
        # 合并视频
        logger.info("开始合并视频...")
        final_clip = concatenate_videoclips(clips, method="compose")
        
        # 输出视频
        logger.info(f"输出到: {output_file}")
        final_clip.write_videofile(
            output_file,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # 清理资源
        for clip in clips:
            clip.close()
        final_clip.close()
        
        return True
        
    except ImportError:
        logger.error("moviepy未安装，请运行: pip install moviepy")
        return False
    except Exception as e:
        logger.error(f"moviepy合并失败: {e}")
        return False

def merge_videos_simple_ffmpeg(video_files, output_file):
    """使用ffmpeg合并视频"""
    import subprocess
    
    # 创建临时文件列表
    temp_list_file = "temp_video_list_weird.txt"
    
    try:
        # 写入文件列表
        with open(temp_list_file, 'w', encoding='utf-8') as f:
            for video_file in video_files:
                escaped_path = video_file.replace('\\', '/')
                f.write(f"file '{escaped_path}'\n")
        
        logger.info("尝试使用系统ffmpeg...")
        
        cmd = [
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
            '-i', temp_list_file,
            '-vf', 'scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-c:a', 'aac', '-b:a', '128k',
            output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("ffmpeg合并成功！")
            return True
        else:
            logger.error(f"ffmpeg失败: {result.stderr}")
            return False
                
    except Exception as e:
        logger.error(f"ffmpeg合并出错: {e}")
        return False
    finally:
        if os.path.exists(temp_list_file):
            os.remove(temp_list_file)

if __name__ == "__main__":
    # 随便选5个视频文件测试
    base_dir = r"c:\Code\insDownloader\test_downloads_vanvan"
    
    # 获取所有mp4文件
    all_videos = []
    if os.path.exists(base_dir):
        all_videos = [f for f in os.listdir(base_dir) if f.endswith('.mp4')]
        all_videos.sort()
    
    if len(all_videos) < 5:
        print(f"只找到 {len(all_videos)} 个视频文件，需要至少5个")
        exit(1)
    
    # 选择前5个视频
    selected_videos = all_videos[:5]
    video_paths = [os.path.join(base_dir, video) for video in selected_videos]
    
    print("选择的视频文件:")
    for i, video in enumerate(selected_videos):
        print(f"{i+1}. {video}")
    
    output_file = "test_weird_resolution.mp4"
    
    print(f"\n开始合并到: {output_file}")
    
    # 先尝试moviepy
    success = merge_videos_with_moviepy(video_paths, output_file)
    
    # 如果moviepy失败，尝试ffmpeg
    if not success:
        logger.info("moviepy失败，尝试ffmpeg...")
        success = merge_videos_simple_ffmpeg(video_paths, output_file)
    
    if success:
        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"\n✅ 合并成功！输出文件: {output_file} ({size_mb:.1f}MB)")
        else:
            print("\n❌ 合并失败 - 输出文件不存在")
    else:
        print("\n❌ 合并失败")
