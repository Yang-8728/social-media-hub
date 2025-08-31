#!/usr/bin/env python3
"""
实际B站上传测试
"""
import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader
from src.core.models import VideoMetadata

def main():
    print("=== 实际B站上传测试 ===")
    
    # 测试视频
    test_video = r"c:\Code\social-media-hub\temp\test_upload.mp4"
    if not os.path.exists(test_video):
        print(f"❌ 测试视频不存在: {test_video}")
        return
    
    print(f"✅ 测试视频: {test_video}")
    print(f"📁 文件大小: {os.path.getsize(test_video) / 1024:.1f} KB")
    
    # 创建元数据
    metadata = VideoMetadata(
        title="AI助手测试上传",
        description="这是一个自动化测试视频，用于验证B站上传功能。",
        tags=["测试", "自动化"],
        category="科技"
    )
    
    print("📋 视频元数据:")
    print(f"  标题: {metadata.title}")
    print(f"  描述: {metadata.description}")
    print(f"  标签: {metadata.tags}")
    
    # 执行上传
    try:
        uploader = BilibiliUploader("ai_vanvan")
        print("🚀 开始上传...")
        
        result = uploader.upload(test_video, metadata)
        
        print(f"\n=== 上传结果 ===")
        print(f"成功: {result.success}")
        print(f"平台: {result.platform}")
        print(f"账号: {result.account}")
        print(f"耗时: {result.duration:.1f}秒")
        print(f"消息: {result.message}")
        
        if not result.success:
            print(f"错误: {result.error}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
