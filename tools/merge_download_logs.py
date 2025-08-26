#!/usr/bin/env python3
"""
合并 gaoxiao 和 ai_vanvan 的下载记录
将 gaoxiao_downloads.json 的记录合并到 ai_vanvan_downloads.json
"""
import json
import os
from pathlib import Path

def merge_download_logs():
    # 文件路径
    gaoxiao_file = Path("videos/download_logs/gaoxiao_downloads.json")
    ai_vanvan_file = Path("data/download_logs/ai_vanvan_downloads.json")
    backup_file = Path("data/download_logs/ai_vanvan_downloads.json.backup")
    
    print("🔄 开始合并下载记录...")
    
    # 读取 gaoxiao 记录
    if gaoxiao_file.exists():
        with open(gaoxiao_file, 'r', encoding='utf-8') as f:
            gaoxiao_data = json.load(f)
        print(f"📂 读取 gaoxiao 记录: {len(gaoxiao_data['downloads'])} 条")
    else:
        print("❌ gaoxiao_downloads.json 不存在")
        return
    
    # 读取 ai_vanvan 记录
    if ai_vanvan_file.exists():
        with open(ai_vanvan_file, 'r', encoding='utf-8') as f:
            ai_vanvan_data = json.load(f)
        print(f"📂 读取 ai_vanvan 记录: {len(ai_vanvan_data['downloads'])} 条")
    else:
        ai_vanvan_data = {"account": "ai_vanvan", "downloads": []}
        print("📂 创建新的 ai_vanvan 记录")
    
    # 备份原文件
    if ai_vanvan_file.exists():
        os.makedirs(backup_file.parent, exist_ok=True)
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(ai_vanvan_data, f, ensure_ascii=False, indent=2)
        print(f"💾 备份原文件到: {backup_file}")
    
    # 获取已有的 shortcode
    existing_shortcodes = {item['shortcode'] for item in ai_vanvan_data['downloads']}
    print(f"🔍 ai_vanvan 已有 shortcode: {len(existing_shortcodes)} 个")
    
    # 合并记录，避免重复
    merged_count = 0
    for item in gaoxiao_data['downloads']:
        shortcode = item['shortcode']
        if shortcode not in existing_shortcodes:
            # 更新账户名
            item_copy = item.copy()
            ai_vanvan_data['downloads'].append(item_copy)
            existing_shortcodes.add(shortcode)
            merged_count += 1
    
    print(f"🔄 合并了 {merged_count} 条新记录")
    
    # 更新账户名
    ai_vanvan_data['account'] = 'ai_vanvan'
    
    # 保存合并后的文件
    os.makedirs(ai_vanvan_file.parent, exist_ok=True)
    with open(ai_vanvan_file, 'w', encoding='utf-8') as f:
        json.dump(ai_vanvan_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 合并完成!")
    print(f"📊 最终记录数: {len(ai_vanvan_data['downloads'])} 条")
    print(f"📄 保存到: {ai_vanvan_file}")
    
    # 删除旧的 gaoxiao 文件
    if gaoxiao_file.exists():
        gaoxiao_file.unlink()
        print(f"🗑️ 删除旧文件: {gaoxiao_file}")

if __name__ == "__main__":
    merge_download_logs()
