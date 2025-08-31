#!/usr/bin/env python3
"""
完整的B站视频上传功能测试
"""
from src.platforms.bilibili.uploader import BilibiliUploader
from src.core.models import VideoMetadata
import time
import os

def test_full_upload():
    """测试完整的视频上传流程"""
    print('=== 完整B站上传功能测试 ===')
    
    # 测试视频路径
    test_video = r'c:\Code\social-media-hub\temp\test_upload.mp4'
    
    if not os.path.exists(test_video):
        print(f'❌ 测试视频不存在: {test_video}')
        return False
    
    print(f'📹 使用测试视频: {test_video}')
    
    try:
        # 创建上传器
        uploader = BilibiliUploader('ai_vanvan')
        
        # 创建视频元数据
        metadata = VideoMetadata(
            title="测试视频上传 - AI助手测试",
            description="这是一个自动化上传测试视频，用于验证B站上传功能。",
            tags=["测试", "自动化", "AI助手"],
            category="科技"
        )
        
        print('📋 视频元数据:')
        print(f'  标题: {metadata.title}')
        print(f'  描述: {metadata.description}')
        print(f'  标签: {", ".join(metadata.tags)}')
        print(f'  分类: {metadata.category}')
        
        print('\n🚀 开始上传流程...')
        
        # 调用上传功能
        result = uploader.upload(test_video, metadata)
        
        print(f'\n📊 上传结果:')
        print(f'  成功: {result.success}')
        print(f'  消息: {result.message}')
        if result.video_id:
            print(f'  视频ID: {result.video_id}')
        if result.url:
            print(f'  视频链接: {result.url}')
        
        return result.success
        
    except Exception as e:
        print(f'❌ 上传测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_full_upload()
    if success:
        print('\n🎉 上传功能测试成功！')
    else:
        print('\n💥 上传功能需要进一步调试')
