#!/usr/bin/env python3
"""
测试博主ID提取功能的修复
"""
import os
import sys

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.platforms.bilibili.uploader import BilibiliUploader
from src.utils.video_merger import VideoMerger

def test_uploader_extraction():
    """测试上传器的博主ID提取"""
    print("🧪 测试上传器博主ID提取功能")
    print("=" * 50)
    
    uploader = BilibiliUploader("aigf8728")
    
    # 测试用例
    test_cases = [
        # 正常的博主ID提取
        "c:\\Code\\social-media-hub\\videos\\downloads\\aigf8728\\2025-09-04_lanagrace18.judge\\video.mp4",
        "c:\\Code\\social-media-hub\\videos\\downloads\\aigf8728\\2025-09-10_iimsaarah\\video.mp4",
        
        # 问题文件：包含时间戳的路径
        "c:\\Code\\social-media-hub\\videos\\downloads\\aigf8728\\2025-10-07_unknown\\2025-10-07_03-19-36_UTC.mp4",
        "c:\\Code\\social-media-hub\\videos\\downloads\\aigf8728\\2025-10-06_unknown\\2025-10-06_06-40-39_UTC.mp4",
        
        # 合并后的视频
        "c:\\Code\\social-media-hub\\videos\\merged\\aigf8728\\ins你的海外第10个女友_03-19-36_UTC.mp4.mp4",
        "c:\\Code\\social-media-hub\\videos\\merged\\aigf8728\\ins你的海外第10个女友_nabilaprilllaofficial.mp4",
    ]
    
    for i, video_path in enumerate(test_cases, 1):
        print(f"\n{i}. 测试路径: {video_path}")
        blogger_id = uploader._extract_blogger_id(video_path)
        print(f"   提取结果: '{blogger_id}'")
        
        # 检查是否是时间戳格式
        if any(x in blogger_id for x in ['-', ':', 'UTC']):
            print(f"   ❌ 错误：提取了时间戳格式")
        elif blogger_id == "[博主ID]":
            print(f"   ⚠️  警告：未能提取博主ID")
        else:
            print(f"   ✅ 成功：提取了有效的博主ID")

def test_merger_extraction():
    """测试合并器的博主ID提取"""
    print("\n🧪 测试合并器博主ID提取功能")
    print("=" * 50)
    
    merger = VideoMerger("aigf8728")
    
    # 测试用例：模拟视频路径列表
    test_video_lists = [
        # 正常情况
        [
            "c:\\Code\\social-media-hub\\videos\\downloads\\aigf8728\\2025-09-04_lanagrace18.judge\\video1.mp4",
            "c:\\Code\\social-media-hub\\videos\\downloads\\aigf8728\\2025-09-04_lanagrace18.judge\\video2.mp4"
        ],
        
        # 包含时间戳的情况
        [
            "c:\\Code\\social-media-hub\\videos\\downloads\\aigf8728\\2025-10-07_unknown\\2025-10-07_03-19-36_UTC.mp4",
            "c:\\Code\\social-media-hub\\videos\\downloads\\aigf8728\\2025-10-07_unknown\\2025-10-07_06-40-39_UTC.mp4"
        ],
        
        # 混合情况
        [
            "c:\\Code\\social-media-hub\\videos\\downloads\\aigf8728\\2025-09-10_iimsaarah\\video1.mp4",
            "c:\\Code\\social-media-hub\\videos\\downloads\\aigf8728\\2025-10-07_unknown\\2025-10-07_03-19-36_UTC.mp4"
        ]
    ]
    
    for i, video_list in enumerate(test_video_lists, 1):
        print(f"\n{i}. 测试视频列表:")
        for video in video_list:
            print(f"   - {video}")
        
        blogger_id = merger._extract_blogger_id_from_videos(video_list)
        print(f"   提取结果: '{blogger_id}'")
        
        # 检查是否是时间戳格式
        if any(x in blogger_id for x in ['-', ':', 'UTC']):
            print(f"   ❌ 错误：提取了时间戳格式")
        elif blogger_id == "blogger":
            print(f"   ⚠️  警告：使用了默认值")
        else:
            print(f"   ✅ 成功：提取了有效的博主ID")

def test_title_generation():
    """测试标题生成"""
    print("\n🧪 测试标题生成功能")
    print("=" * 50)
    
    uploader = BilibiliUploader("aigf8728")
    
    test_videos = [
        "c:\\Code\\social-media-hub\\videos\\merged\\aigf8728\\ins你的海外第10个女友_nabilaprilllaofficial.mp4",
        "c:\\Code\\social-media-hub\\videos\\downloads\\aigf8728\\2025-09-10_iimsaarah\\video.mp4"
    ]
    
    for video_path in test_videos:
        print(f"\n视频路径: {video_path}")
        title = uploader._generate_title_preview(video_path)
        print(f"生成标题: '{title}'")
        
        # 检查标题格式
        if "ins你的海外第" in title and "个女友:" in title:
            blogger_part = title.split("个女友:")[1]
            if any(x in blogger_part for x in ['-', ':', 'UTC']):
                print(f"   ❌ 错误：标题包含时间戳格式")
            else:
                print(f"   ✅ 成功：标题格式正确")
        else:
            print(f"   ⚠️  警告：标题格式不符合预期")

if __name__ == "__main__":
    test_uploader_extraction()
    test_merger_extraction() 
    test_title_generation()
    
    print(f"\n🎯 测试完成！")
    print(f"💡 如果看到❌错误，说明还需要进一步修复")
    print(f"💡 如果全部✅成功，说明博主ID提取功能已修复")