#!/usr/bin/env python3
import os
import subprocess
import json

def check_video_resolution(video_path):
    """检查视频分辨率"""
    try:
        # 使用ffprobe检查分辨率
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_streams', '-select_streams', 'v:0', video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        if data['streams']:
            stream = data['streams'][0]
            width = stream.get('width', 0)
            height = stream.get('height', 0)
            return width, height
    except:
        # 如果ffprobe失败，尝试用原项目的方法
        try:
            from src.utils.video_merger import VideoMerger
            merger = VideoMerger()
            # 这里可以添加其他检查方法
        except:
            pass
    return None, None

def find_weird_resolution_videos():
    """找出分辨率奇怪的视频"""
    video_dir = r"videos\downloads\ai_vanvan\2025-08-27"
    
    if not os.path.exists(video_dir):
        print(f"视频目录不存在: {video_dir}")
        return []
    
    # 获取所有mp4文件
    mp4_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    mp4_files.sort()
    
    print(f"找到 {len(mp4_files)} 个视频文件")
    print("检查分辨率...")
    
    video_info = []
    target_ratio = 9/16  # 目标比例 720:1280
    
    for mp4_file in mp4_files:
        video_path = os.path.join(video_dir, mp4_file)
        width, height = check_video_resolution(video_path)
        
        if width and height:
            ratio = width / height
            is_weird = abs(ratio - target_ratio) > 0.1  # 比例差异超过0.1就算奇怪
            
            video_info.append({
                'file': mp4_file,
                'width': width,
                'height': height,
                'ratio': ratio,
                'is_weird': is_weird
            })
            
            status = "⚠️ 奇怪" if is_weird else "✅ 正常"
            print(f"{status} {mp4_file}: {width}x{height} (比例: {ratio:.3f})")
        else:
            print(f"❌ 无法检测 {mp4_file}")
    
    # 找出5个分辨率最奇怪的视频
    weird_videos = [v for v in video_info if v['is_weird']]
    
    if len(weird_videos) >= 5:
        print(f"\n找到 {len(weird_videos)} 个奇怪分辨率的视频，选择前5个:")
        selected = weird_videos[:5]
    else:
        print(f"\n只找到 {len(weird_videos)} 个奇怪分辨率的视频，补充一些正常的:")
        normal_videos = [v for v in video_info if not v['is_weird']]
        selected = weird_videos + normal_videos[:5-len(weird_videos)]
    
    print("\n选择的视频:")
    for i, video in enumerate(selected):
        print(f"{i+1}. {video['file']}: {video['width']}x{video['height']} (比例: {video['ratio']:.3f})")
    
    return [v['file'] for v in selected]

if __name__ == "__main__":
    weird_files = find_weird_resolution_videos()
    
    if weird_files:
        print(f"\n可以用这些文件测试分辨率标准化:")
        for f in weird_files:
            print(f"  {f}")
    else:
        print("\n没有找到合适的测试文件")
