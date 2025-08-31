#!/usr/bin/env python3
import os
import sys

def merge_3_weird_resolutions():
    """合并3个分辨率不标准的视频"""
    
    # 3个非标准分辨率视频
    video_dir = r"videos\downloads\ai_vanvan\2025-08-27"
    video_files = [
        "2025-03-05_15-32-07_UTC.mp4",  # 576x1024 - 左右加黑边
        "2025-05-25_18-50-13_UTC.mp4",  # 576x1024 - 左右加黑边  
        "2025-06-08_16-20-11_UTC.mp4"   # 720x1278 - 上下加黑边
    ]
    
    video_paths = [os.path.join(video_dir, f) for f in video_files]
    output_file = "test_3_weird_resolutions.mp4"
    
    print("🎬 合并3个分辨率不标准的视频")
    print("=" * 50)
    print("视频列表:")
    print("1. 2025-03-05_15-32-07_UTC.mp4 (576x1024) - 左右加黑边")
    print("2. 2025-05-25_18-50-13_UTC.mp4 (576x1024) - 左右加黑边") 
    print("3. 2025-06-08_16-20-11_UTC.mp4 (720x1278) - 上下加黑边")
    print()
    
    # 验证文件存在
    for i, (file, path) in enumerate(zip(video_files, video_paths)):
        if os.path.exists(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"✅ 视频 {i+1}: {file} ({size_mb:.1f}MB)")
        else:
            print(f"❌ 视频 {i+1}: {file} - 文件不存在")
            return None
    
    print(f"\n开始合并到: {output_file}")
    print("目标: 统一为720x1280分辨率，自动添加黑边")
    
    try:
        # 使用VideoMerger进行分辨率标准化
        sys.path.append('src')
        from utils.video_merger import VideoMerger
        
        merger = VideoMerger()
        
        print("\n使用VideoMerger进行分辨率标准化合并...")
        success = merger.merge_videos_with_normalization(video_paths, output_file)
        
        if success and os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            abs_path = os.path.abspath(output_file)
            
            print(f"\n✅ 合并成功！")
            print(f"输出文件: {output_file}")
            print(f"完整路径: {abs_path}")
            print(f"文件大小: {size_mb:.1f}MB")
            print()
            print("🎯 测试要点:")
            print("- 第1和第2个视频应该有左右黑边 (576→720宽度)")
            print("- 第3个视频应该有上下黑边 (1278→1280高度)")
            print("- 所有视频最终都是720x1280分辨率")
            print("- 检查视频切换时是否有卡顿")
            
            return abs_path
        else:
            print(f"\n❌ 合并失败")
            return None
            
    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        return None

if __name__ == "__main__":
    result_path = merge_3_weird_resolutions()
    
    if result_path:
        print(f"\n🎉 合并完成！")
        print(f"视频路径: {result_path}")
        print("\n可以播放这个视频来验证:")
        print("1. 分辨率标准化是否正确")
        print("2. 黑边添加是否合适") 
        print("3. 视频切换是否流畅")
    else:
        print(f"\n💥 合并失败")
