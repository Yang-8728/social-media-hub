#!/usr/bin/env python3
"""
一键自动上传 - 无需任何交互
自动选择最新视频并上传到B站
"""
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader
from src.core.models import VideoMetadata

def auto_upload():
    """完全自动化的上传流程"""
    print("🤖 AI助手自动上传启动...")
    
    # 自动找到最新视频
    video_dir = r"c:\Code\social-media-hub\videos\merged\ai_vanvan"
    
    if not os.path.exists(video_dir):
        print("❌ 视频目录不存在")
        return False
    
    videos = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    if not videos:
        print("❌ 没有找到MP4视频文件")
        return False
    
    # 选择最新的视频文件
    latest_video = max(videos, key=lambda x: os.path.getctime(os.path.join(video_dir, x)))
    video_path = os.path.join(video_dir, latest_video)
    file_size = os.path.getsize(video_path) / (1024 * 1024)
    
    print(f"📹 自动选择最新视频: {latest_video}")
    print(f"📊 文件大小: {file_size:.1f} MB")
    
    # 自动生成优化的元数据
    import datetime
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    metadata = VideoMetadata(
        title=f"AI智能助手日常合集 {today}",
        description=f"""🤖 AI智能助手自动化内容合集 - {today}

这是由AI助手自动下载、处理并上传的视频合集，展示了：

✨ 功能特点：
• 自动内容获取与整理
• 智能视频合并处理
• 全自动上传工作流
• 高效内容管理

🛠️ 技术栈：
- Python自动化框架
- Selenium浏览器自动化
- FFmpeg视频处理
- 智能工作流设计

💡 适用场景：
- 内容创作自动化
- 批量视频处理
- 效率工具演示
- 技术分享交流

🔗 项目开源，欢迎学习交流！
#AI自动化 #效率工具 #技术分享""",
        tags=[
            "AI助手",
            "自动化",
            "效率工具", 
            "Python",
            "技术分享",
            "内容创作",
            "工作流",
            "开源项目",
            "实用工具",
            "科技"
        ],
        category="科技"
    )
    
    print(f"📝 自动生成标题: {metadata.title}")
    print(f"🏷️ 自动标签: {', '.join(metadata.tags[:5])}...")
    
    # 执行自动上传
    try:
        print("🚀 开始自动上传...")
        uploader = BilibiliUploader("ai_vanvan")
        result = uploader.upload(video_path, metadata)
        
        if result.success:
            print("🎉 自动上传成功!")
            print(f"📺 视频ID: {result.video_id}")
            if result.url:
                print(f"🔗 视频链接: {result.url}")
            print(f"⏱️ 总耗时: {result.duration:.1f}秒")
            return True
        else:
            print("❌ 自动上传失败")
            print(f"错误信息: {result.error}")
            return False
            
    except Exception as e:
        print(f"❌ 自动上传异常: {e}")
        return False

if __name__ == "__main__":
    success = auto_upload()
    if success:
        print("\n✅ 自动上传任务完成!")
    else:
        print("\n❌ 自动上传任务失败!")
