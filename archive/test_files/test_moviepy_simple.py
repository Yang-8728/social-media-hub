#!/usr/bin/env python3
import os
import sys

def test_moviepy_simple():
    """简单测试moviepy是否可用"""
    try:
        from moviepy.editor import VideoFileClip, concatenate_videoclips
        print("✅ moviepy导入成功")
        return True
    except ImportError as e:
        print(f"❌ moviepy导入失败: {e}")
        return False

def merge_5_videos():
    """合并5个视频，测试分辨率标准化"""
    if not test_moviepy_simple():
        return False
    
    try:
        from moviepy.editor import VideoFileClip, concatenate_videoclips
        
        # 视频文件路径
        base_dir = r"videos\downloads\ai_vanvan\2025-08-27"
        video_files = [
            "2025-03-05_15-32-07_UTC.mp4",
            "2025-04-17_16-52-08_UTC.mp4", 
            "2025-05-19_13-33-04_UTC.mp4",
            "2025-05-19_15-05-43_UTC.mp4",
            "2025-05-25_18-50-13_UTC.mp4"
        ]
        
        video_paths = [os.path.join(base_dir, f) for f in video_files]
        
        print("检查视频文件...")
        for i, path in enumerate(video_paths):
            if os.path.exists(path):
                print(f"✅ 视频 {i+1}: {video_files[i]}")
            else:
                print(f"❌ 视频 {i+1}: {video_files[i]} - 文件不存在")
                return False
        
        print("\n开始处理视频...")
        clips = []
        target_size = (720, 1280)  # 9:16 aspect ratio
        
        for i, path in enumerate(video_paths):
            print(f"处理视频 {i+1}/{len(video_paths)}: {video_files[i]}")
            
            clip = VideoFileClip(path)
            original_size = clip.size
            print(f"  原始分辨率: {original_size[0]}x{original_size[1]}")
            
            # 计算缩放比例，保持纵横比
            scale_w = target_size[0] / original_size[0]
            scale_h = target_size[1] / original_size[1]
            scale = min(scale_w, scale_h)
            
            new_w = int(original_size[0] * scale)
            new_h = int(original_size[1] * scale)
            
            print(f"  缩放后: {new_w}x{new_h}")
            
            # 调整大小并居中（添加黑边）
            clip_resized = clip.resize((new_w, new_h))
            
            # 添加黑边使其达到目标尺寸
            clip_padded = clip_resized.on_color(size=target_size, color=(0,0,0), pos='center')
            
            clips.append(clip_padded)
            clip.close()  # 释放原始clip
        
        print("\n合并视频...")
        final_clip = concatenate_videoclips(clips)
        
        output_file = "test_weird_resolution_moviepy.mp4"
        print(f"输出到: {output_file}")
        
        final_clip.write_videofile(
            output_file,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        # 清理资源
        for clip in clips:
            clip.close()
        final_clip.close()
        
        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"\n✅ 合并成功！输出文件: {output_file} ({size_mb:.1f}MB)")
            return True
        else:
            print("\n❌ 合并失败 - 输出文件不存在")
            return False
            
    except Exception as e:
        print(f"\n❌ 合并过程出错: {e}")
        return False

if __name__ == "__main__":
    print("测试分辨率标准化合并（moviepy版本）")
    print("=" * 50)
    
    success = merge_5_videos()
    
    if success:
        print("\n🎉 测试完成！现在可以测试不同分辨率的视频合并功能了")
    else:
        print("\n💥 测试失败")
