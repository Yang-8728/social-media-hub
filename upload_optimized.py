#!/usr/bin/env python3
"""
优化的B站上传配置
包含更好的标签和分区设置
"""
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader
from src.core.models import VideoMetadata

def get_optimized_metadata(video_name=""):
    """获取优化的视频元数据"""
    
    # 智能标题生成
    if "合集" in video_name or "merged" in video_name:
        title = f"AI智能助手自动合集 - {video_name[:15]}"
    else:
        title = f"AI助手自动化工具演示 - {video_name[:15]}"
    
    # 优化描述
    description = """🤖 AI智能助手自动化工具演示

这是一个展示AI助手自动化功能的视频，包含：
• 自动内容下载和整理
• 智能视频合并处理  
• 自动化工作流程演示
• 实用工具分享

🛠️ 技术特点：
- Python自动化脚本
- 智能内容处理
- 高效工作流程
- 开源工具分享

💡 适用场景：
- 内容创作者
- 技术爱好者
- 效率提升需求
- 自动化学习

#AI助手 #自动化 #效率工具 #技术分享"""

    # 优化标签组合
    tags = [
        "AI助手",
        "人工智能", 
        "自动化工具",
        "效率提升",
        "编程技术",
        "实用工具",
        "科技分享",
        "创作工具",
        "B站原创",
        "技术教程"
    ]
    
    return VideoMetadata(
        title=title,
        description=description,
        tags=tags,
        category="科技"  # 最适合的分区
    )

def main():
    print("=== 优化版B站上传工具 ===")
    
    # 视频文件选择
    video_dir = r"c:\Code\social-media-hub\videos\merged\ai_vanvan"
    videos = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    
    if not videos:
        print("❌ 没有找到视频文件")
        return
    
    print("📁 可用视频:")
    for i, video in enumerate(videos[-5:]):  # 显示最新5个
        file_path = os.path.join(video_dir, video)
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        print(f"  {i+1}. {video} ({file_size:.1f} MB)")
    
    # 选择视频
    choice = input("\n选择视频序号 (回车=最新): ").strip()
    if choice.isdigit():
        selected_video = videos[int(choice)-1]
    else:
        selected_video = max(videos, key=lambda x: os.path.getctime(os.path.join(video_dir, x)))
    
    video_path = os.path.join(video_dir, selected_video)
    print(f"✅ 选择: {selected_video}")
    
    # 获取优化的元数据
    metadata = get_optimized_metadata(selected_video)
    
    print(f"\n📋 优化后的视频信息:")
    print(f"📝 标题: {metadata.title}")
    print(f"🏷️ 标签: {', '.join(metadata.tags)}")
    print(f"📂 分区: {metadata.category}")
    print(f"📄 描述长度: {len(metadata.description)} 字符")
    
    # 确认上传
    confirm = input("\n🚀 确认上传? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ 取消上传")
        return
    
    # 执行上传
    try:
        uploader = BilibiliUploader("ai_vanvan")
        print("🔄 开始上传...")
        
        result = uploader.upload(video_path, metadata)
        
        if result.success:
            print("🎉 上传成功!")
            print(f"📺 视频ID: {result.video_id}")
            if result.url:
                print(f"🔗 视频链接: {result.url}")
            print(f"⏱️ 耗时: {result.duration:.1f}秒")
        else:
            print("❌ 上传失败")
            print(f"错误: {result.error}")
            
    except Exception as e:
        print(f"❌ 上传异常: {e}")

if __name__ == "__main__":
    main()
