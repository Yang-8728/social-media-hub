#!/usr/bin/env python3
"""
上传功能主入口
Upload Main Entry Point
"""
import os
import sys

# 添加项目根目录到路径
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

from src.platforms.bilibili.uploader import BilibiliUploader


def upload_video(video_path: str, account_name: str = "ai_vanvan"):
    """
    上传视频到B站
    
    Args:
        video_path: 视频文件路径
        account_name: 账号名称 (ai_vanvan 或 aigf8728)
    """
    try:
        # 验证文件存在
        if not os.path.exists(video_path):
            print(f"❌ 视频文件不存在: {video_path}")
            return False
        
        # 创建上传器
        uploader = BilibiliUploader(account_name)
        
        # 执行上传
        result = uploader.upload(video_path)
        
        # 显示结果
        if result.success:
            print(f"✅ 上传成功！用时 {int(result.duration)} 秒")
            return True
        else:
            print(f"❌ 上传失败: {result.message}")
            if result.error:
                print(f"错误详情: {result.error}")
            return False
            
    except Exception as e:
        print(f"❌ 上传过程发生异常: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python upload.py <视频文件路径> [账号名称]")
        print("账号名称: ai_vanvan (默认) 或 aigf8728")
        print("示例: python upload.py video.mp4 ai_vanvan")
        sys.exit(1)
    
    video_path = sys.argv[1]
    account_name = sys.argv[2] if len(sys.argv) > 2 else "ai_vanvan"
    
    print(f"🚀 开始上传视频...")
    print(f"视频文件: {os.path.basename(video_path)}")
    print(f"上传账号: {account_name}")
    print("-" * 50)
    
    success = upload_video(video_path, account_name)
    sys.exit(0 if success else 1)
