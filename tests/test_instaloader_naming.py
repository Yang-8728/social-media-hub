#!/usr/bin/env python3
"""
测试 instaloader 默认文件命名格式
"""
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from instaloader import Instaloader

def test_instaloader_naming():
    """测试 instaloader 的默认命名格式"""
    print("=== instaloader 默认文件命名格式 ===")
    
    loader = Instaloader()
    
    # 查看 instaloader 的默认设置
    print(f"默认文件名模板: {loader.filename_pattern}")
    print(f"目录名模板: {loader.dirname_pattern}")
    print(f"是否保存元数据: {loader.save_metadata}")
    print(f"是否压缩 JSON: {loader.compress_json}")
    print(f"是否下载视频缩略图: {loader.download_video_thumbnails}")
    print(f"是否下载地理位置标签: {loader.download_geotags}")
    print(f"是否下载评论: {loader.download_comments}")
    
    print("\n=== 文件命名示例 ===")
    print("假设有一个 shortcode 为 'ABC123DEF' 的帖子：")
    print("- 视频文件: ABC123DEF.mp4")
    print("- 图片文件: ABC123DEF.jpg") 
    print("- 元数据文件: ABC123DEF.json")
    print("- 说明文件: ABC123DEF.txt")
    print("\n如果是多媒体帖子（多个文件）：")
    print("- 第一个文件: ABC123DEF_1.jpg")
    print("- 第二个文件: ABC123DEF_2.mp4")
    print("- 第三个文件: ABC123DEF_3.jpg")

if __name__ == "__main__":
    test_instaloader_naming()
