#!/usr/bin/env python3
"""
检查测试视频文件准备情况
"""
import os

def check_test_videos():
    """检查可用的测试视频文件"""
    print('=== 准备上传测试 ===')
    
    # 检查合并视频目录
    test_video_dir = r'c:\Code\social-media-hub\data\merged\ai_vanvan'
    
    if os.path.exists(test_video_dir):
        print(f'✅ 找到合并视频目录: {test_video_dir}')
        
        # 查找MP4文件
        videos = [f for f in os.listdir(test_video_dir) if f.endswith('.mp4')]
        
        if videos:
            print(f'✅ 找到 {len(videos)} 个测试视频:')
            for i, video in enumerate(videos[:3]):  # 只显示前3个
                video_path = os.path.join(test_video_dir, video)
                size = os.path.getsize(video_path) / (1024*1024)  # MB
                print(f'  {i+1}. {video} ({size:.1f}MB)')
                
            # 选择第一个作为测试文件
            test_video_path = os.path.join(test_video_dir, videos[0])
            print(f'\n📹 推荐测试视频: {test_video_path}')
            return test_video_path
        else:
            print('❌ 未找到MP4视频文件')
            return None
    else:
        print('❌ 合并视频目录不存在')
        
        # 检查其他可能的视频位置
        alternative_dirs = [
            r'c:\Code\social-media-hub\data\downloads\ai_vanvan',
            r'c:\Code\social-media-hub\temp',
            r'c:\Code\insDownloader\videos\merged\ai_vanvan'
        ]
        
        print('\n🔍 检查其他可能的视频位置:')
        for alt_dir in alternative_dirs:
            if os.path.exists(alt_dir):
                videos = []
                for root, dirs, files in os.walk(alt_dir):
                    videos.extend([os.path.join(root, f) for f in files if f.endswith('.mp4')])
                
                if videos:
                    print(f'✅ 在 {alt_dir} 找到 {len(videos)} 个视频')
                    video_path = videos[0]
                    size = os.path.getsize(video_path) / (1024*1024)
                    print(f'📹 可用测试视频: {video_path} ({size:.1f}MB)')
                    return video_path
                else:
                    print(f'❌ {alt_dir} - 无视频文件')
            else:
                print(f'❌ {alt_dir} - 目录不存在')
        
        return None

def create_dummy_video_if_needed():
    """如果没有测试视频，创建一个简单的测试文件"""
    print('\n🛠️ 没有找到现有视频，创建测试文件...')
    
    # 创建一个小的测试视频文件（实际上是文本文件，仅用于路径测试）
    test_dir = r'c:\Code\social-media-hub\temp'
    os.makedirs(test_dir, exist_ok=True)
    
    test_file = os.path.join(test_dir, 'test_upload.mp4')
    
    # 创建一个假的测试文件（实际上传时需要真实视频）
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write('# This is a test file, real MP4 video needed for actual upload\n')
    
    print(f'✅ 创建测试文件: {test_file}')
    print('⚠️ 注意：这只是路径测试文件，实际上传需要真实MP4视频')
    
    return test_file

if __name__ == "__main__":
    video_path = check_test_videos()
    
    if not video_path:
        video_path = create_dummy_video_if_needed()
    
    if video_path:
        print(f'\n🎯 测试视频准备完成: {video_path}')
        print('\n下一步可以开发视频上传功能！')
    else:
        print('\n❌ 无法准备测试视频文件')
