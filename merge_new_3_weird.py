#!/usr/bin/env python3
import os
import sys

def merge_new_3_weird():
    """合并3个新的分辨率不标准视频（避开问题视频）"""
    
    # 新的3个非标准分辨率视频
    video_dir = r"videos\downloads\ai_vanvan\2025-08-27"
    video_files = [
        "2025-05-25_18-50-13_UTC.mp4",  # 576x1024 - 左右加黑边
        "2025-06-08_16-20-11_UTC.mp4",  # 720x1278 - 上下加黑边
        "2025-06-14_17-45-06_UTC.mp4"   # 480x854  - 左右加黑边
    ]
    
    video_paths = [os.path.join(video_dir, f) for f in video_files]
    output_file = "test_new_3_weird_resolutions.mp4"
    
    print("🎬 合并3个新的分辨率不标准视频")
    print("（已排除有问题的2025-03-05视频）")
    print("=" * 50)
    print("新视频列表:")
    print("1. 2025-05-25_18-50-13_UTC.mp4 (576x1024) - 左右加黑边")
    print("2. 2025-06-08_16-20-11_UTC.mp4 (720x1278) - 上下加黑边") 
    print("3. 2025-06-14_17-45-06_UTC.mp4 (480x854)  - 左右加黑边")
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
    print("预期效果:")
    print("- 第1个视频: 576→720宽度，左右加黑边")
    print("- 第2个视频: 1278→1280高度，上下加黑边")
    print("- 第3个视频: 480→720宽度，左右加黑边")
    
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
            print("🎯 新的测试要点:")
            print("- 第1个视频(576x1024): 应该有明显的左右黑边")
            print("- 第2个视频(720x1278): 应该有细微的上下黑边")  
            print("- 第3个视频(480x854):  应该有更宽的左右黑边")
            print("- 所有视频最终都是720x1280分辨率")
            print("- 检查是否没有卡顿问题")
            
            return abs_path
        else:
            print(f"\n❌ 合并失败")
            return None
            
    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        return None

if __name__ == "__main__":
    result_path = merge_new_3_weird()
    
    if result_path:
        print(f"\n🎉 新的合并完成！")
        print(f"视频路径: {result_path}")
        print("\n现在应该可以清楚看到黑边效果:")
        print("1. 第1和第3个视频有左右黑边（宽度扩展）")
        print("2. 第2个视频有上下黑边（高度扩展）") 
        print("3. 没有视频卡顿问题")
    else:
        print(f"\n💥 合并失败")
