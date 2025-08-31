#!/usr/bin/env python3
import os
import sys
import subprocess

def test_resolution_normalization():
    """测试分辨率标准化合并"""
    
    # 视频文件路径
    video_dir = r"videos\downloads\ai_vanvan\2025-08-27"
    
    # 选择5个不同大小的视频，可能有不同分辨率
    video_files = [
        "2025-03-05_15-32-07_UTC.mp4",    # 0.7MB 小视频
        "2025-08-08_11-23-16_UTC.mp4",    # 33MB 大视频 
        "2025-08-15_17-44-44_UTC.mp4",    # 11MB 中等视频
        "2025-08-26_12-57-05_UTC.mp4",    # 0.4MB 最小视频
        "2025-07-26_16-58-23_UTC.mp4"     # 6MB 中等视频
    ]
    
    video_paths = [os.path.join(video_dir, f) for f in video_files]
    
    print("选择的测试视频（不同大小可能代表不同分辨率）:")
    for i, (file, path) in enumerate(zip(video_files, video_paths)):
        if os.path.exists(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"✅ {i+1}. {file} ({size_mb:.1f}MB)")
        else:
            print(f"❌ {i+1}. {file} - 文件不存在")
            return False
    
    # 创建文件列表
    temp_list_file = "temp_normalization_list.txt"
    output_file = "test_resolution_normalization.mp4"
    
    try:
        with open(temp_list_file, 'w', encoding='utf-8') as f:
            for video_path in video_paths:
                # 使用相对路径，避免路径问题
                f.write(f"file '{video_path}'\n")
        
        print(f"\n开始合并测试...")
        print("这次会测试分辨率标准化功能（720x1280 + 自动加黑边）")
        
        # 使用之前成功的方法，但加上分辨率标准化
        # 首先尝试使用social-media-hub的video_merger
        try:
            # 添加src目录到Python路径
            import sys
            sys.path.append('src')
            
            from utils.video_merger import VideoMerger
            from utils.logger import Logger
            
            # 创建VideoMerger实例（不需要logger参数）
            merger = VideoMerger()
            
            print("使用VideoMerger进行分辨率标准化合并...")
            
            # 使用带标准化的合并方法
            success = merger.merge_videos_with_normalization(
                video_paths, 
                output_file
            )
            
            if success and os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"\n✅ 分辨率标准化合并成功！")
                print(f"输出文件: {output_file} ({size_mb:.1f}MB)")
                print(f"所有视频已标准化为720x1280分辨率")
                print(f"不同原始分辨率的视频应该有黑边填充")
                return True
            else:
                print("VideoMerger方法失败，尝试备用方案...")
                raise Exception("VideoMerger failed")
        
        except Exception as e:
            print(f"VideoMerger失败: {e}")
            print("使用手动方法合并...")
            
            # 手动创建带分辨率标准化的命令
            # 注意：这里我们假设系统有ffmpeg，如果没有就会失败
            cmd = [
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', temp_list_file,
                '-vf', 'scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black',
                '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
                '-c:a', 'aac', '-b:a', '128k',
                output_file
            ]
            
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                if os.path.exists(output_file):
                    size_mb = os.path.getsize(output_file) / (1024 * 1024)
                    print(f"\n✅ 手动FFmpeg分辨率标准化成功！")
                    print(f"输出文件: {output_file} ({size_mb:.1f}MB)")
                    return True
                else:
                    print("\n❌ FFmpeg执行成功但没有输出文件")
                    return False
            except subprocess.CalledProcessError as e:
                print(f"\n❌ FFmpeg执行失败: {e}")
                print("stderr:", e.stderr)
                return False
            except FileNotFoundError:
                print("\n❌ FFmpeg未找到，无法执行分辨率标准化")
                print("请安装FFmpeg或使用VideoMerger类")
                return False
                
    except Exception as e:
        print(f"\n❌ 执行过程出错: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(temp_list_file):
            os.remove(temp_list_file)

if __name__ == "__main__":
    print("分辨率标准化合并测试")
    print("=" * 50)
    print("测试目标：")
    print("1. 合并5个可能有不同分辨率的视频")
    print("2. 统一输出为720x1280分辨率") 
    print("3. 较小分辨率的视频应该有黑边填充")
    print("4. 保持原始纵横比不变形")
    print()
    
    success = test_resolution_normalization()
    
    if success:
        print("\n🎉 分辨率标准化测试完成！")
        print("   可以播放输出文件检查：")
        print("   - 是否所有视频都是720x1280分辨率")
        print("   - 原始比例较小的视频是否有黑边")
        print("   - 视频是否没有拉伸变形")
        print("   - 音视频是否同步")
    else:
        print("\n💥 测试失败")
        print("   可能需要:")
        print("   - 安装FFmpeg")
        print("   - 或使用VideoMerger类中的分辨率标准化功能")
