#!/usr/bin/env python3
"""
一键上传最新视频到B站
"""
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader
from src.core.models import VideoMetadata

def main():
    # 自动选择最新的视频文件
    video_dir = r"c:\Code\social-media-hub\videos\merged\ai_vanvan"
    videos = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    
    if not videos:
        print("❌ 没有找到视频文件")
        return
    
    # 选择最新的文件
    latest_video = max(videos, key=lambda x: os.path.getctime(os.path.join(video_dir, x)))
    video_path = os.path.join(video_dir, latest_video)
    file_size = os.path.getsize(video_path) / (1024 * 1024)
    
    print(f"🚀 一键上传最新视频: {latest_video} ({file_size:.1f} MB)")
    
    # 自动生成元数据
    metadata = VideoMetadata(
        title=f"AI助手自动合集 - {latest_video[:20]}",
        description="AI助手自动下载并合并的最新视频合集\n\n包含最新内容更新，由自动化工具生成上传。",
        tags=["AI助手", "自动化", "视频合集", "最新"],
        category="科技"
    )
    
    # 上传
    uploader = BilibiliUploader("ai_vanvan")
    result = uploader.upload(video_path, metadata)
    
    if result.success:
        print("🎉 上传成功!")
        print(f"📺 视频ID: {result.video_id}")
    else:
        print(f"❌ 上传失败: {result.error}")

if __name__ == "__main__":
    main()
