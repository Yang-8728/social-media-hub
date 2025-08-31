#!/usr/bin/env python3
"""
使用真实视频的B站上传测试
"""
import os
import sys
import time
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader
from src.core.models import VideoMetadata

def main():
    print("=== 使用真实视频的B站上传测试 ===")
    
    # 使用真实的合并视频文件
    test_video = r"c:\Code\social-media-hub\videos\merged\ai_vanvan\ai_vanvan_2025-08-29_10-18-52_merged_10videos.mp4"
    
    if not os.path.exists(test_video):
        print(f"❌ 视频文件不存在: {test_video}")
        return
    
    # 获取文件大小
    file_size = os.path.getsize(test_video) / (1024 * 1024)
    print(f"📹 选择视频: {os.path.basename(test_video)}")
    print(f"📊 文件大小: {file_size:.1f} MB")
    
    # 创建视频元数据
    metadata = VideoMetadata(
        title="AI助手自动合集 2025-08-29",
        description="这是AI助手自动下载并合并的10个视频的合集，包含最新的内容更新。\n\n自动化工具生成，用于测试B站上传功能。",
        tags=["AI助手", "自动化", "视频合集", "测试"],
        category="科技"
    )
    
    print(f"📋 视频信息:")
    print(f"  标题: {metadata.title}")
    print(f"  描述: {metadata.description[:50]}...")
    print(f"  标签: {', '.join(metadata.tags)}")
    print(f"  分类: {metadata.category}")
    
    # 初始化上传器
    try:
        uploader = BilibiliUploader("ai_vanvan")
        print("✅ 上传器初始化成功")
    except Exception as e:
        print(f"❌ 上传器初始化失败: {e}")
        return
    
    # 开始上传
    print("\n🚀 开始上传流程...")
    try:
        result = uploader.upload(test_video, metadata)
        
        if result.success:
            print("🎉 上传成功!")
            print(f"📺 视频ID: {result.video_id}")
            if result.url:
                print(f"🔗 视频链接: {result.url}")
        else:
            print("❌ 上传失败")
            print(f"错误信息: {result.error}")
            
    except Exception as e:
        print(f"❌ 上传过程异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
