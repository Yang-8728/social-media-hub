#!/usr/bin/env python3
import os
import sys

def find_new_weird_resolutions():
    """重新找分辨率不标准的视频（排除已删除的问题视频）"""
    
    video_dir = r"videos\downloads\ai_vanvan\2025-08-27"
    
    sys.path.append('src')
    from utils.video_merger import VideoMerger
    
    merger = VideoMerger()
    
    # 获取所有mp4文件
    mp4_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    mp4_files.sort()
    
    print("🔍 重新扫描所有视频分辨率...")
    print("（已删除问题视频 2025-03-05_15-32-07_UTC.mp4）")
    print("=" * 50)
    
    standard_resolution = (720, 1280)
    non_standard_videos = []
    all_resolutions = {}
    
    for mp4_file in mp4_files:
        video_path = os.path.join(video_dir, mp4_file)
        
        try:
            width, height = merger.get_video_resolution(video_path)
            if width and height:
                resolution_key = f"{width}x{height}"
                
                if resolution_key not in all_resolutions:
                    all_resolutions[resolution_key] = []
                all_resolutions[resolution_key].append(mp4_file)
                
                is_standard = (width == standard_resolution[0] and height == standard_resolution[1])
                
                if not is_standard:
                    non_standard_videos.append({
                        'file': mp4_file,
                        'width': width,
                        'height': height,
                        'resolution': resolution_key,
                        'size_mb': os.path.getsize(video_path) / (1024 * 1024)
                    })
                
                status = "✅ 标准" if is_standard else "⚠️  非标准"
                size_mb = os.path.getsize(video_path) / (1024 * 1024)
                print(f"{status} {mp4_file}: {width}x{height} ({size_mb:.1f}MB)")
            else:
                print(f"❌ 无法检测 {mp4_file}")
        except Exception as e:
            print(f"❌ 错误 {mp4_file}: {e}")
    
    print(f"\n📊 所有分辨率统计:")
    print("-" * 30)
    for resolution, files in all_resolutions.items():
        is_standard = resolution == "720x1280"
        status = "✅ 标准" if is_standard else "⚠️  非标准"
        print(f"{status} {resolution}: {len(files)} 个视频")
        
        if not is_standard:  # 只显示非标准分辨率的文件
            for file in files:
                video_path = os.path.join(video_dir, file)
                size_mb = os.path.getsize(video_path) / (1024 * 1024)
                print(f"    - {file} ({size_mb:.1f}MB)")
        print()
    
    print(f"\n🎯 找到 {len(non_standard_videos)} 个非标准分辨率视频:")
    print("-" * 40)
    
    if len(non_standard_videos) >= 3:
        # 选择3个不同的非标准视频
        selected = non_standard_videos[:3]
        print("选择前3个进行新的合并测试:")
    else:
        print(f"只找到 {len(non_standard_videos)} 个非标准视频")
        selected = non_standard_videos
        
        # 如果不够3个，补充一些较小的标准视频做对比
        if len(selected) < 3:
            print("\n补充一些小文件标准视频:")
            standard_videos = []
            for mp4_file in mp4_files:
                if mp4_file not in [v['file'] for v in non_standard_videos]:
                    video_path = os.path.join(video_dir, mp4_file)
                    try:
                        width, height = merger.get_video_resolution(video_path)
                        if width == 720 and height == 1280:
                            size_mb = os.path.getsize(video_path) / (1024 * 1024)
                            standard_videos.append({
                                'file': mp4_file,
                                'width': width,
                                'height': height,
                                'resolution': f"{width}x{height}",
                                'size_mb': size_mb
                            })
                    except:
                        pass
            
            # 按文件大小排序，选择较小的
            standard_videos.sort(key=lambda x: x['size_mb'])
            selected.extend(standard_videos[:3-len(selected)])
    
    print("\n📹 新的测试视频组合:")
    for i, video in enumerate(selected):
        ratio = video['width'] / video['height']
        print(f"\n视频 {i+1}:")
        print(f"   文件名: {video['file']}")
        print(f"   分辨率: {video['resolution']}")
        print(f"   大小: {video['size_mb']:.1f}MB")
        print(f"   纵横比: {ratio:.3f}")
        
        if video['width'] == 720 and video['height'] == 1280:
            print(f"   状态: ✅ 标准分辨率")
        elif video['width'] < 720:
            print(f"   状态: ⚠️  较窄，需要左右加黑边")
        elif video['height'] < 1280:
            print(f"   状态: ⚠️  较矮，需要上下加黑边")
        else:
            print(f"   状态: ⚠️  需要缩放")
    
    return selected

if __name__ == "__main__":
    try:
        videos = find_new_weird_resolutions()
        
        if len(videos) >= 3:
            print(f"\n🎬 准备用这3个视频重新测试:")
            for i, video in enumerate(videos[:3]):
                print(f"  {i+1}. {video['file']} ({video['resolution']})")
        else:
            print("\n😅 可用的测试视频不足3个")
            
    except Exception as e:
        print(f"❌ 执行失败: {e}")
