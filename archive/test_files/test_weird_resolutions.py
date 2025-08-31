#!/usr/bin/env python3
import os
import subprocess
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def merge_videos_with_normalization(video_files, output_file):
    """合并视频并标准化分辨率（加黑边）"""
    
    # 创建临时文件列表
    temp_list_file = "temp_weird_list.txt"
    
    try:
        # 写入文件列表
        with open(temp_list_file, 'w', encoding='utf-8') as f:
            for video_file in video_files:
                # 使用双反斜杠转义路径
                escaped_path = video_file.replace('\\', '\\\\')
                f.write(f"file '{escaped_path}'\n")
        
        logger.info(f"创建文件列表: {temp_list_file}")
        
        # 先尝试copy模式
        logger.info("尝试copy模式合并...")
        cmd_copy = [
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0', 
            '-i', temp_list_file, '-c', 'copy', output_file
        ]
        
        result = subprocess.run(cmd_copy, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("Copy模式合并成功！")
            return True
        else:
            logger.warning(f"Copy模式失败，尝试标准化模式...")
            
            # 如果copy模式失败，使用标准化分辨率（加黑边）
            cmd_normalize = [
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', temp_list_file,
                '-vf', 'scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black',
                '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
                '-c:a', 'aac', '-b:a', '128k',
                '-avoid_negative_ts', 'make_zero',
                '-fflags', '+genpts',
                output_file
            ]
            
            result = subprocess.run(cmd_normalize, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("标准化模式合并成功！")
                return True
            else:
                logger.error(f"标准化模式也失败了: {result.stderr}")
                return False
                
    except Exception as e:
        logger.error(f"合并过程中出错: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(temp_list_file):
            os.remove(temp_list_file)

if __name__ == "__main__":
    # 使用social项目中的视频
    base_dir = r"videos\downloads\ai_vanvan\2025-08-27"
    
    # 选择5个不同的视频（跟之前测试的不同）
    video_files = [
        "2025-07-15_04-30-17_UTC.mp4",
        "2025-07-18_09-22-08_UTC.mp4", 
        "2025-07-22_14-21-38_UTC.mp4",
        "2025-07-23_22-48-02_UTC.mp4",
        "2025-07-26_16-58-23_UTC.mp4"
    ]
    
    video_paths = [os.path.join(base_dir, video) for video in video_files]
    
    print("选择的视频文件（测试分辨率标准化）:")
    for i, video in enumerate(video_files):
        print(f"{i+1}. {video}")
    
    # 检查文件是否存在
    missing_files = []
    for path in video_paths:
        if not os.path.exists(path):
            missing_files.append(path)
    
    if missing_files:
        print(f"\n❌ 以下文件不存在:")
        for f in missing_files:
            print(f"  {f}")
        exit(1)
    
    output_file = "test_weird_resolutions.mp4"
    
    print(f"\n开始合并到: {output_file}")
    print("这将测试分辨率标准化和黑边添加功能...")
    
    success = merge_videos_with_normalization(video_paths, output_file)
    
    if success:
        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"\n✅ 合并成功！输出文件: {output_file} ({size_mb:.1f}MB)")
            print("请播放检查视频是否有黑边，分辨率是否统一")
        else:
            print("\n❌ 合并失败 - 输出文件不存在")
    else:
        print("\n❌ 合并失败")
