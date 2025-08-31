#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析下载器的扫描对比机制对删除文件的影响
"""

import os
import json
import lzma
from pathlib import Path
import sys
sys.path.append('src')

from utils.logger import Logger

def analyze_scan_comparison_mechanism():
    """分析扫描对比机制"""
    print("🔍 分析下载器的扫描对比机制")
    print("=" * 60)
    
    print("📋 下载器的双重检查机制:")
    print("1️⃣ **下载日志检查** (`Logger.is_downloaded()`)")
    print("   - 首先检查下载日志中是否有成功记录")
    print("   - 如果有记录且状态为'success'，返回True")
    
    print("\n2️⃣ **文件系统检查** (`_check_file_exists_by_shortcode()`)")
    print("   - 如果日志中没有记录，扫描实际文件系统")
    print("   - 查找对应shortcode的json.xz文件")
    print("   - 如果找到文件，返回True")
    
    print("\n3️⃣ **智能同步机制** (`sync_missing_downloads()`)")
    print("   - 自动发现文件存在但日志缺失的情况")
    print("   - 补充缺失的下载记录到日志中")
    print("   - 分为快速同步(最近3天)和完整同步")
    
    # 模拟删除8-27文件夹的情况
    print(f"\n🎯 模拟删除8-27文件夹后的下载行为:")
    print("=" * 50)
    
    # 检查当前8-27文件夹的文件
    target_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    
    if target_folder.exists():
        json_files = list(target_folder.glob("*.json.xz"))
        
        print(f"📂 当前8-27文件夹: {len(json_files)} 个视频")
        
        # 提取shortcode
        folder_shortcodes = []
        for json_file in json_files:
            try:
                with lzma.open(json_file, 'rb') as f:
                    data = json.loads(f.read().decode('utf-8'))
                    shortcode = data.get('node', {}).get('shortcode')
                    if shortcode:
                        folder_shortcodes.append(shortcode)
            except:
                continue
        
        print(f"🔍 提取到shortcode: {len(folder_shortcodes)} 个")
        
        # 检查这些shortcode在日志中的状态
        logger = Logger("ai_vanvan")
        log_data = logger.load_download_log()
        
        logged_shortcodes = {d["shortcode"]: d for d in log_data["downloads"] if d["status"] == "success"}
        
        print(f"\n📋 下载日志分析:")
        in_log_count = 0
        for shortcode in folder_shortcodes:
            if shortcode in logged_shortcodes:
                in_log_count += 1
        
        print(f"   ✅ 在日志中有记录: {in_log_count}/{len(folder_shortcodes)} 个")
        print(f"   ❓ 日志中无记录: {len(folder_shortcodes) - in_log_count} 个")
        
    else:
        print("❌ 8-27文件夹不存在")
        folder_shortcodes = []
        in_log_count = 0
    
    print(f"\n🔄 删除文件夹后下载器的行为分析:")
    print("=" * 50)
    
    print(f"**步骤1: 扫描Instagram收藏**")
    print(f"   - 获取所有收藏的视频shortcode")
    print(f"   - 假设包含之前下载的8-27视频")
    
    print(f"\n**步骤2: 逐个检查是否已下载**")
    print(f"   - 调用 `logger.is_downloaded(shortcode)`")
    print(f"   - 对于8-27的视频:")
    
    if in_log_count > 0:
        print(f"     ✅ {in_log_count}个视频: 日志检查→发现记录→返回True→**跳过下载**")
    
    if len(folder_shortcodes) - in_log_count > 0:
        print(f"     🔍 {len(folder_shortcodes) - in_log_count}个视频: 日志检查→无记录→文件检查→**找不到文件**→返回False→**会重新下载**")
    
    print(f"\n**步骤3: 同步机制触发**")
    print(f"   - 如果启用了同步(`sync_missing_downloads`)")
    print(f"   - 发现文件缺失，不会添加记录")
    print(f"   - 这些视频会被识别为'新视频'")
    
    print(f"\n🎯 **结论**:")
    print("=" * 30)
    
    if in_log_count == len(folder_shortcodes):
        print(f"❌ **不会重新下载** - 所有视频在日志中都有记录")
        print(f"   即使删除了文件，日志检查会阻止重新下载")
        
    elif in_log_count == 0:
        print(f"✅ **会重新下载** - 所有视频在日志中都没有记录")
        print(f"   文件系统检查找不到文件，会被识别为新视频")
        
    else:
        print(f"⚠️ **部分重新下载**:")
        print(f"   - {in_log_count}个视频: 有日志记录 → 不会重新下载")
        print(f"   - {len(folder_shortcodes) - in_log_count}个视频: 无日志记录 → 会重新下载")
    
    # 提供详细的重新下载条件
    print(f"\n💡 **重新下载的必要条件**:")
    print("=" * 40)
    print(f"要让视频重新下载，必须同时满足:")
    print(f"1. 🗑️ 删除对应的视频文件")
    print(f"2. 📝 删除下载日志中的对应记录")
    print(f"3. 🔄 或者清空整个下载日志")
    
    print(f"\n⚠️ **注意**:")
    print(f"仅删除文件夹不够！下载器主要依赖日志记录判断。")
    
    return {
        'total_files': len(folder_shortcodes) if folder_shortcodes else 0,
        'in_log': in_log_count if 'in_log_count' in locals() else 0,
        'will_redownload_count': len(folder_shortcodes) - in_log_count if folder_shortcodes and 'in_log_count' in locals() else 0
    }

def test_actual_download_check():
    """测试实际的下载检查"""
    print(f"\n🧪 实际测试下载检查")
    print("=" * 40)
    
    logger = Logger("ai_vanvan")
    
    # 从8-27文件夹中选几个shortcode测试
    target_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    
    if target_folder.exists():
        json_files = list(target_folder.glob("*.json.xz"))[:3]  # 测试前3个
        
        print(f"🔍 测试前3个视频的下载检查:")
        
        for i, json_file in enumerate(json_files, 1):
            try:
                with lzma.open(json_file, 'rb') as f:
                    data = json.loads(f.read().decode('utf-8'))
                    shortcode = data.get('node', {}).get('shortcode')
                    
                    if shortcode:
                        # 测试当前的检查结果
                        is_downloaded = logger.is_downloaded(shortcode)
                        status = "✅ 已下载" if is_downloaded else "❌ 未下载"
                        
                        print(f"   {i}. {shortcode}: {status}")
                        
                        # 如果删除文件夹，这个检查会返回什么？
                        print(f"      📁 当前文件存在，日志记录存在")
                        print(f"      🗑️ 删除文件夹后: 日志记录仍存在 → 仍会返回'已下载'")
                        
            except Exception as e:
                print(f"   {i}. 读取失败: {e}")
    else:
        print("❌ 8-27文件夹不存在，无法测试")

def main():
    result = analyze_scan_comparison_mechanism()
    test_actual_download_check()
    
    print(f"\n" + "=" * 60)
    print(f"🎯 **最终答案**:")
    print(f"删除8-27文件夹后，会重新下载吗？")
    
    if result['will_redownload_count'] == 0:
        print(f"❌ **不会重新下载** ({result['in_log']}/{result['total_files']}个视频有日志记录)")
    elif result['will_redownload_count'] == result['total_files']:
        print(f"✅ **全部重新下载** (所有视频都没有日志记录)")
    else:
        print(f"⚠️ **部分重新下载** ({result['will_redownload_count']}/{result['total_files']}个会重新下载)")
    
    print(f"\n💡 关键：**下载器主要看日志记录，不是文件存在**")
    print(f"如果想重新下载，必须同时删除文件和日志记录！")

if __name__ == "__main__":
    main()
