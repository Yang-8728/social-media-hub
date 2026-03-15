#!/usr/bin/env python3
"""
视频编号计数器管理工具

用法:
  python manage_video_counter.py get              # 查询当前编号
  python manage_video_counter.py set 125          # 设置为125（下次上传会是#126）
  python manage_video_counter.py reset            # 重置为0
"""

import sys
import requests

API_BASE = "http://localhost:8080"
ACCOUNT = "ai_vanvan"

def get_counter():
    """查询当前计数"""
    response = requests.get(f"{API_BASE}/api/biliup/counter")
    if response.status_code == 200:
        data = response.json()
        current = data['current_number']
        print(f"当前计数: {current}")
        print(f"下次上传视频编号将是: #{current + 1}")
        return current
    else:
        print(f"错误: {response.text}")
        return None

def set_counter(value):
    """设置计数器"""
    response = requests.post(
        f"{API_BASE}/api/biliup/counter",
        json={"account": ACCOUNT, "value": value}
    )
    if response.status_code == 200:
        print(f"✅ 计数器已设置为: {value}")
        print(f"下次上传视频编号将是: #{value + 1}")
    else:
        print(f"❌ 错误: {response.text}")

def reset_counter():
    """重置计数器"""
    response = requests.delete(
        f"{API_BASE}/api/biliup/counter",
        json={"account": ACCOUNT}
    )
    if response.status_code == 200:
        print(f"✅ 计数器已重置")
        print(f"下次上传视频编号将是: #1")
    else:
        print(f"❌ 错误: {response.text}")

def upload_with_auto_number(video_path, **kwargs):
    """使用自动编号上传视频"""
    payload = {
        "account": ACCOUNT,
        "video_path": video_path,
        "auto_number": True,
        **kwargs
    }
    response = requests.post(f"{API_BASE}/api/biliup/upload", json=payload)
    if response.status_code == 200:
        data = response.json()
        task = data['task']
        print(f"✅ 上传任务已添加")
        print(f"   标题: {task['title']}")
        print(f"   视频: {task['video_path']}")
        print(f"   分区: {task['tid']}")
        print(f"   标签: {task['tag']}")
    else:
        print(f"❌ 错误: {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "get":
        get_counter()
    
    elif command == "set":
        if len(sys.argv) < 3:
            print("错误: 需要提供数值")
            print("用法: python manage_video_counter.py set 125")
            sys.exit(1)
        try:
            value = int(sys.argv[2])
            set_counter(value)
        except ValueError:
            print(f"错误: '{sys.argv[2]}' 不是有效数字")
            sys.exit(1)
    
    elif command == "reset":
        confirm = input("确认要重置计数器吗? (y/N): ")
        if confirm.lower() == 'y':
            reset_counter()
        else:
            print("已取消")
    
    elif command == "upload":
        if len(sys.argv) < 3:
            print("错误: 需要提供视频路径")
            print("用法: python manage_video_counter.py upload /videos/ai_vanvan/merged_20251104.mp4")
            sys.exit(1)
        video_path = sys.argv[2]
        upload_with_auto_number(video_path)
    
    else:
        print(f"未知命令: {command}")
        print(__doc__)
        sys.exit(1)
