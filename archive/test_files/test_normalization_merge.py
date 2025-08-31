#!/usr/bin/env python3
import os
import subprocess
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_normalization_merge():
    """测试分辨率标准化合并功能"""
    
    # 选择5个视频文件
    video_dir = r"videos\downloads\ai_vanvan\2025-08-27"
    video_files = [
        "2025-03-05_15-32-07_UTC.mp4",
        "2025-04-17_16-52-08_UTC.mp4", 
        "2025-05-19_13-33-04_UTC.mp4",
        "2025-05-19_15-05-43_UTC.mp4",
        "2025-05-25_18-50-13_UTC.mp4"
    ]
    
    video_paths = [os.path.join(video_dir, f) for f in video_files]
    
    print("选择的测试视频:")
    for i, (file, path) in enumerate(zip(video_files, video_paths)):
        if os.path.exists(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"✅ {i+1}. {file} ({size_mb:.1f}MB)")
        else:
            print(f"❌ {i+1}. {file} - 文件不存在")
            return False
    
    # 创建临时文件列表
    temp_list_file = "temp_normalize_test.txt"
    output_file = "test_normalization_merge.mp4"
    
    try:
        # 写入文件列表
        with open(temp_list_file, 'w', encoding='utf-8') as f:
            for video_path in video_paths:
                escaped_path = video_path.replace('\\', '/')
                f.write(f"file '{escaped_path}'\n")
        
        print(f"\n开始合并到: {output_file}")
        print("使用分辨率标准化模式（720x1280 + 黑边填充）...")
        
        # 使用分辨率标准化命令
        cmd = [
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
            '-i', temp_list_file,
            '-vf', 'scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-c:a', 'aac', '-b:a', '128k',
            '-avoid_negative_ts', 'make_zero',
            '-fflags', '+genpts',
            output_file
        ]
        
        print("执行FFmpeg命令...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"\n✅ 合并成功！")
                print(f"输出文件: {output_file} ({size_mb:.1f}MB)")
                print(f"所有视频已标准化为720x1280分辨率，不同分辨率的视频会自动加黑边")
                return True
            else:
                print(f"\n❌ 命令成功但输出文件不存在")
                return False
        else:
            print(f"\n❌ FFmpeg执行失败:")
            print(result.stderr)
            return False
                
    except Exception as e:
        print(f"\n❌ 执行过程出错: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(temp_list_file):
            os.remove(temp_list_file)

if __name__ == "__main__":
    print("测试分辨率标准化合并功能")
    print("=" * 50)
    print("这个测试会将5个视频合并成统一的720x1280分辨率")
    print("不同分辨率的视频会自动添加黑边以保持比例")
    print()
    
    success = test_normalization_merge()
    
    if success:
        print("\n🎉 分辨率标准化测试完成！")
        print("   可以播放 test_normalization_merge.mp4 查看效果")
        print("   注意观察是否有黑边填充，以及音视频是否同步")
    else:
        print("\n💥 测试失败")
