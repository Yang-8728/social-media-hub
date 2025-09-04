#!/usr/bin/env python3
"""
为 aigf8728 账户按照 ai_vanvan 的方式创建下载和合并记录
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

def create_aigf8728_records():
    """创建 aigf8728 的记录文件，模仿 ai_vanvan 的格式"""
    print("🎯 为 aigf8728 创建记录文件...")
    print("=" * 50)
    
    # 确保目录存在
    os.makedirs("logs/downloads", exist_ok=True)
    os.makedirs("logs/merges", exist_ok=True)
    
    # 从 ai_vanvan 的记录中获取所有 shortcode
    print("📋 读取 ai_vanvan 的记录作为参考...")
    
    ai_vanvan_downloads_file = "logs/downloads/ai_vanvan_downloads.json"
    if not os.path.exists(ai_vanvan_downloads_file):
        print("❌ 找不到 ai_vanvan 的下载记录文件")
        return
    
    with open(ai_vanvan_downloads_file, 'r', encoding='utf-8') as f:
        ai_vanvan_data = json.load(f)
    
    # 提取所有 shortcode
    shortcodes = []
    for download in ai_vanvan_data.get("downloads", []):
        shortcodes.append(download["shortcode"])
    
    print(f"✅ 从 ai_vanvan 找到 {len(shortcodes)} 个 shortcode")
    
    # 创建 aigf8728 的下载记录
    print("📥 创建 aigf8728 下载记录...")
    aigf8728_downloads = {
        "account": "aigf8728",
        "downloads": []
    }
    
    current_time = datetime.now().isoformat()
    
    for shortcode in shortcodes:
        download_record = {
            "shortcode": shortcode,
            "download_time": current_time,
            "status": "success",
            "file_path": "videos/downloads/aigf8728",
            "error": "",
            "merged": True,  # 标记为已合并
            "uploaded": True,  # 标记为已上传
            "imported": True,  # 标记为初始化导入
            "note": "初始化时从 ai_vanvan 导入"
        }
        aigf8728_downloads["downloads"].append(download_record)
    
    # 保存下载记录
    downloads_file = "logs/downloads/aigf8728_downloads.json"
    with open(downloads_file, 'w', encoding='utf-8') as f:
        json.dump(aigf8728_downloads, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 创建下载记录文件: {downloads_file}")
    print(f"   包含 {len(shortcodes)} 条记录")
    
    # 创建 aigf8728 的合并记录
    print("🔗 创建 aigf8728 合并记录...")
    
    # 模拟一些合并记录
    aigf8728_merges = {
        "merged_videos": [
            {
                "merge_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "output_file": "videos\\merged\\aigf8728\\imported_batch.mp4",
                "input_count": len(shortcodes),
                "input_videos": [f"videos\\downloads\\aigf8728\\{shortcode}.mp4" for shortcode in shortcodes[:10]],  # 只显示前10个
                "shortcodes": shortcodes,
                "status": "success",
                "imported": True,
                "note": "初始化时批量导入的合并记录"
            }
        ]
    }
    
    # 保存合并记录
    merges_file = "logs/merges/aigf8728_merged_record.json"
    with open(merges_file, 'w', encoding='utf-8') as f:
        json.dump(aigf8728_merges, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 创建合并记录文件: {merges_file}")
    print(f"   包含 1 条批量合并记录")
    
    return len(shortcodes)

def verify_aigf8728_records():
    """验证 aigf8728 记录文件"""
    print("\n🔍 验证记录文件...")
    
    downloads_file = "logs/downloads/aigf8728_downloads.json"
    merges_file = "logs/merges/aigf8728_merged_record.json"
    
    if os.path.exists(downloads_file):
        with open(downloads_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 下载记录: {len(data.get('downloads', []))} 条")
    else:
        print(f"❌ 下载记录文件不存在")
    
    if os.path.exists(merges_file):
        with open(merges_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 合并记录: {len(data.get('merged_videos', []))} 条")
    else:
        print(f"❌ 合并记录文件不存在")

if __name__ == "__main__":
    print("🎯 aigf8728 记录初始化工具")
    print("按照 ai_vanvan 的格式创建记录文件")
    print()
    
    if input("确认创建 aigf8728 记录文件？(y/N): ").lower() == 'y':
        count = create_aigf8728_records()
        verify_aigf8728_records()
        
        print(f"\n" + "=" * 50)
        print(f"🎉 初始化完成！")
        print(f"📥 创建了 {count} 条下载记录")
        print(f"🔗 创建了 1 条合并记录")
        print(f"📁 文件位置:")
        print(f"  logs/downloads/aigf8728_downloads.json")
        print(f"  logs/merges/aigf8728_merged_record.json")
        print(f"\n现在 aigf8728 的记录和 ai_vanvan 一样完整了！")
    else:
        print("❌ 操作已取消")
