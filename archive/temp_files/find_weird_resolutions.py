#!/usr/bin/env python3
import os
import sys

def find_non_standard_videos():
    """找出分辨率不标准的视频"""
    
    video_dir = r"videos\downloads\ai_vanvan\2025-08-27"
    
    # 添加src路径
    sys.path.append('src')
    from utils.video_merger import VideoMerger
    
    merger = VideoMerger()
    
    # 获取所有mp4文件
    mp4_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    mp4_files.sort()
    
    print("🔍 检查所有视频的分辨率...")
    print("=" * 50)
    
    standard_resolution = (720, 1280)  # 标准分辨率
    non_standard_videos = []
    all_resolutions = {}
    
    for mp4_file in mp4_files[:10]:  # 先检查前10个，避免太多输出
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
                        'resolution': resolution_key
                    })
                
                status = "✅ 标准" if is_standard else "⚠️  非标准"
                print(f"{status} {mp4_file}: {width}x{height}")
            else:
                print(f"❌ 无法检测 {mp4_file}")
        except Exception as e:
            print(f"❌ 错误 {mp4_file}: {e}")
    
    print("\n📊 分辨率统计:")
    print("-" * 30)
    for resolution, files in all_resolutions.items():
        print(f"{resolution}: {len(files)} 个视频")
        for file in files[:3]:  # 只显示前3个例子
            print(f"  - {file}")
        if len(files) > 3:
            print(f"  - ... 还有 {len(files)-3} 个")
        print()
    
    print(f"\n🎯 找到 {len(non_standard_videos)} 个非标准分辨率视频:")
    print("-" * 40)
    
    if len(non_standard_videos) >= 3:
        selected = non_standard_videos[:3]
        print("选择前3个进行测试:")
    else:
        print(f"只找到 {len(non_standard_videos)} 个，全部显示:")
        selected = non_standard_videos
        
        # 如果不够3个，从其他视频中补充一些
        if len(selected) < 3:
            print("\n补充一些其他视频进行对比:")
            standard_videos = [f for f in mp4_files if f not in [v['file'] for v in non_standard_videos]]
            for i, video in enumerate(standard_videos[:3-len(selected)]):
                video_path = os.path.join(video_dir, video)
                try:
                    width, height = merger.get_video_resolution(video_path)
                    if width and height:
                        selected.append({
                            'file': video,
                            'width': width,
                            'height': height,
                            'resolution': f"{width}x{height}"
                        })
                except:
                    pass
    
    for i, video in enumerate(selected):
        ratio = video['width'] / video['height']
        print(f"\n📹 视频 {i+1}:")
        print(f"   文件名: {video['file']}")
        print(f"   分辨率: {video['resolution']}")
        print(f"   纵横比: {ratio:.3f}")
        
        if video['width'] == 720 and video['height'] == 1280:
            print(f"   状态: ✅ 标准分辨率 (9:16)")
        elif video['width'] < 720 or video['height'] < 1280:
            print(f"   状态: ⚠️  较小分辨率，需要加黑边")
        elif video['width'] > 720 or video['height'] > 1280:
            print(f"   状态: ⚠️  较大分辨率，需要缩放")
        else:
            print(f"   状态: ⚠️  特殊比例")
    
    return selected

if __name__ == "__main__":
    try:
        videos = find_non_standard_videos()
        
        if videos:
            print(f"\n🎬 可以用这{len(videos)}个视频测试分辨率标准化:")
            for video in videos:
                print(f"  - {video['file']} ({video['resolution']})")
        else:
            print("\n😅 没有找到非标准分辨率的视频")
            print("   所有视频都是标准的720x1280分辨率")
            
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        print("可能需要检查VideoMerger类或视频文件")
