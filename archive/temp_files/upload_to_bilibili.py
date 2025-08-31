#!/usr/bin/env python3
"""
B站上传工具 - 简单易用版本
直接运行即可上传视频到B站
"""
import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader
from src.core.models import VideoMetadata

def list_available_videos():
    """列出可用的视频文件"""
    video_dir = r"c:\Code\social-media-hub\videos\merged\ai_vanvan"
    if not os.path.exists(video_dir):
        print(f"❌ 视频目录不存在: {video_dir}")
        return []
    
    videos = []
    for file in os.listdir(video_dir):
        if file.endswith('.mp4'):
            file_path = os.path.join(video_dir, file)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            videos.append({
                'name': file,
                'path': file_path,
                'size': file_size
            })
    
    return sorted(videos, key=lambda x: x['size'])

def main():
    print("=== B站视频上传工具 ===")
    
    # 列出可用视频
    videos = list_available_videos()
    if not videos:
        print("❌ 没有找到可用的视频文件")
        return
    
    print("📁 可用视频文件:")
    for i, video in enumerate(videos):
        print(f"  {i+1}. {video['name']} ({video['size']:.1f} MB)")
    
    # 让用户选择
    try:
        choice = input("\n请选择视频序号 (直接回车选择最新的): ").strip()
        if not choice:
            selected_video = videos[-1]  # 选择最后一个（通常是最新的）
        else:
            idx = int(choice) - 1
            if 0 <= idx < len(videos):
                selected_video = videos[idx]
            else:
                print("❌ 无效的选择")
                return
    except (ValueError, KeyboardInterrupt):
        print("❌ 取消上传")
        return
    
    print(f"✅ 选择视频: {selected_video['name']} ({selected_video['size']:.1f} MB)")
    
    # 输入视频信息
    title = input("视频标题 (可选): ").strip()
    if not title:
        title = f"AI助手自动合集 {selected_video['name'][:19]}"
    
    description = input("视频描述 (可选): ").strip()
    if not description:
        description = "这是AI助手自动下载并合并的视频合集。\n\n包含最新的内容更新，由自动化工具生成。"
    
    tags_input = input("视频标签 (用逗号分隔，可选): ").strip()
    if tags_input:
        tags = [tag.strip() for tag in tags_input.split(',')]
    else:
        tags = ["AI助手", "自动化", "视频合集"]
    
    # 创建元数据
    metadata = VideoMetadata(
        title=title,
        description=description,
        tags=tags,
        category="科技"
    )
    
    print(f"\n📋 上传信息确认:")
    print(f"  视频: {selected_video['name']}")
    print(f"  标题: {metadata.title}")
    print(f"  标签: {', '.join(metadata.tags)}")
    
    confirm = input("\n确认上传? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ 取消上传")
        return
    
    # 开始上传
    print("\n🚀 开始上传...")
    try:
        uploader = BilibiliUploader("ai_vanvan")
        result = uploader.upload(selected_video['path'], metadata)
        
        if result.success:
            print("🎉 上传成功!")
            print(f"📺 视频ID: {result.video_id}")
            if result.url:
                print(f"🔗 视频链接: {result.url}")
            print(f"⏱️ 上传耗时: {result.duration:.1f}秒")
        else:
            print("❌ 上传失败")
            print(f"错误信息: {result.error}")
            
    except Exception as e:
        print(f"❌ 上传异常: {e}")

if __name__ == "__main__":
    main()
