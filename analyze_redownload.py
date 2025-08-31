#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析删除文件夹后重新下载的行为
"""

import os
import json
import lzma
from pathlib import Path
import sys
sys.path.append('src')

from utils.logger import Logger

def analyze_redownload_behavior():
    """分析删除文件夹后重新下载的行为"""
    print("🔍 分析删除8-27文件夹后重新下载的行为")
    print("=" * 60)
    
    # 检查当前8-27文件夹
    target_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    
    print(f"📂 检查文件夹: {target_folder}")
    
    if target_folder.exists():
        files = list(target_folder.glob("*.mp4"))
        json_files = list(target_folder.glob("*.json.xz"))
        
        print(f"  📹 MP4文件: {len(files)} 个")
        print(f"  📄 JSON文件: {len(json_files)} 个")
        
        if files:
            print(f"\n📋 当前8-27文件夹中的视频:")
            for i, file in enumerate(files, 1):
                size_mb = file.stat().st_size / (1024*1024)
                print(f"  {i}. {file.name} ({size_mb:.1f}MB)")
                
        # 提取这些文件的shortcode
        shortcodes_in_folder = set()
        for json_file in json_files:
            try:
                with lzma.open(json_file, 'rb') as f:
                    data = json.loads(f.read().decode('utf-8'))
                    shortcode = data.get('node', {}).get('shortcode')
                    if shortcode:
                        shortcodes_in_folder.add(shortcode)
            except Exception as e:
                print(f"  ⚠️  无法读取 {json_file.name}: {e}")
        
        print(f"\n🔍 提取到的shortcode: {len(shortcodes_in_folder)} 个")
        
    else:
        print("  ❌ 8-27文件夹不存在")
        shortcodes_in_folder = set()
    
    # 检查下载日志记录
    print(f"\n📋 检查下载日志记录")
    logger = Logger("ai_vanvan")
    log_data = logger.load_download_log()
    
    # 统计下载记录
    total_records = len(log_data.get("downloads", []))
    print(f"  📊 总下载记录: {total_records} 个")
    
    # 检查8-27的记录
    records_827 = []
    for record in log_data.get("downloads", []):
        download_time = record.get("download_time", "")
        file_path = record.get("file_path", "")
        if "2025-08-27" in download_time or "2025-08-27" in file_path:
            records_827.append(record)
    
    print(f"  📅 8-27相关记录: {len(records_827)} 个")
    
    if records_827:
        print(f"\n📝 8-27下载记录详情:")
        for i, record in enumerate(records_827, 1):
            shortcode = record.get("shortcode", "NO_SHORTCODE")
            status = record.get("status", "unknown")
            time = record.get("download_time", "")
            print(f"  {i}. {shortcode} | {status} | {time}")
    
    # 分析删除后重新下载的行为
    print(f"\n🎯 删除后重新下载行为分析:")
    print("=" * 50)
    
    print(f"1️⃣ 下载器检查逻辑:")
    print(f"   - 下载器使用 Logger.is_downloaded(shortcode) 检查")
    print(f"   - 这个方法检查的是下载日志，不是文件系统")
    print(f"   - 即使删除了文件，日志记录仍然存在")
    
    print(f"\n2️⃣ 如果删除8-27文件夹会发生什么:")
    if shortcodes_in_folder:
        print(f"   📁 文件夹中有 {len(shortcodes_in_folder)} 个视频")
        print(f"   📋 日志中有 {len(records_827)} 条记录")
        
        # 检查记录和文件的对应关系
        recorded_shortcodes = {r.get("shortcode") for r in records_827 if r.get("shortcode")}
        
        print(f"\n🔍 检查记录和文件对应关系:")
        print(f"   📄 文件shortcode: {len(shortcodes_in_folder)} 个")
        print(f"   📋 记录shortcode: {len(recorded_shortcodes)} 个")
        
        # 找出只在文件中存在的
        only_in_files = shortcodes_in_folder - recorded_shortcodes
        # 找出只在记录中存在的  
        only_in_records = recorded_shortcodes - shortcodes_in_folder
        # 两者都有的
        in_both = shortcodes_in_folder & recorded_shortcodes
        
        print(f"   ✅ 两者都有: {len(in_both)} 个")
        print(f"   📁 只有文件: {len(only_in_files)} 个")
        print(f"   📋 只有记录: {len(only_in_records)} 个")
        
        if only_in_files:
            print(f"\n⚠️  只有文件没有记录的shortcode:")
            for code in list(only_in_files)[:5]:
                print(f"      {code}")
        
        if only_in_records:
            print(f"\n⚠️  只有记录没有文件的shortcode:")
            for code in list(only_in_records)[:5]:
                print(f"      {code}")
    
    print(f"\n3️⃣ 重新下载结果预测:")
    print(f"   ❌ 不会重新下载已记录的视频")
    print(f"   📋 下载器会跳过所有已有记录的shortcode")
    print(f"   🔄 只有完全新的收藏视频才会被下载")
    
    print(f"\n4️⃣ 如果想重新下载，需要:")
    print(f"   🗑️  删除对应的下载记录（从JSON文件中）")
    print(f"   📁 或者删除整个下载日志文件")
    print(f"   ⚠️  但这会影响所有历史记录")
    
    # 提供解决方案
    print(f"\n💡 解决方案:")
    print("=" * 30)
    print(f"如果您想重新下载8-27的视频:")
    print(f"1. 🗑️  删除8-27文件夹")
    print(f"2. 📝 从下载日志中删除8-27的记录")  
    print(f"3. 🔄 运行下载器，会重新下载这些视频")
    
    if records_827:
        print(f"\n📋 需要删除的记录示例:")
        for i, record in enumerate(records_827[:3], 1):
            shortcode = record.get("shortcode", "NO_SHORTCODE")
            print(f"   {i}. shortcode: {shortcode}")
    
    return {
        'folder_files': len(shortcodes_in_folder) if shortcodes_in_folder else 0,
        'log_records': len(records_827),
        'will_redownload': False  # 关键：不会重新下载
    }

def create_redownload_script():
    """创建重新下载脚本"""
    print(f"\n🛠️ 创建重新下载辅助脚本")
    
    script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新下载8-27视频的辅助脚本
"""

import json
import shutil
from pathlib import Path

def remove_827_records_and_files():
    """删除8-27的记录和文件，准备重新下载"""
    print("🗑️ 准备删除8-27的记录和文件")
    
    # 1. 删除文件夹
    folder_path = Path("videos/downloads/ai_vanvan/2025-08-27")
    if folder_path.exists():
        shutil.rmtree(folder_path)
        print("✅ 删除了8-27文件夹")
    else:
        print("⚠️  8-27文件夹不存在")
    
    # 2. 删除日志记录
    log_path = Path("data/download_logs/ai_vanvan_downloads.json")
    
    with open(log_path, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
    
    original_count = len(log_data["downloads"])
    
    # 过滤掉8-27的记录
    filtered_downloads = []
    removed_count = 0
    
    for record in log_data["downloads"]:
        download_time = record.get("download_time", "")
        file_path = record.get("file_path", "")
        
        # 如果不是8-27的记录，保留
        if "2025-08-27" not in download_time and "2025-08-27" not in file_path:
            filtered_downloads.append(record)
        else:
            removed_count += 1
    
    log_data["downloads"] = filtered_downloads
    
    # 保存更新后的日志
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 从下载日志中删除了 {removed_count} 条8-27记录")
    print(f"📊 原记录: {original_count} → 现记录: {len(filtered_downloads)}")
    print("🎯 现在可以重新下载8-27的视频了")

if __name__ == "__main__":
    print("⚠️  警告：这将永久删除8-27的文件和记录！")
    confirm = input("确认执行吗？(y/N): ")
    if confirm.lower() == 'y':
        remove_827_records_and_files()
    else:
        print("❌ 已取消操作")
'''
    
    with open("remove_827_for_redownload.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ 已创建脚本: remove_827_for_redownload.py")

def main():
    result = analyze_redownload_behavior()
    create_redownload_script()
    
    print(f"\n" + "=" * 60)
    print(f"🎯 结论:")
    print(f"  📁 8-27文件夹有 {result['folder_files']} 个视频")
    print(f"  📋 下载日志有 {result['log_records']} 条记录")
    print(f"  🔄 删除文件夹后会重新下载吗: {'否' if not result['will_redownload'] else '是'}")
    print(f"\n💡 如果想重新下载，请运行: python remove_827_for_redownload.py")

if __name__ == "__main__":
    main()
