#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深入分析同步扫描机制对重新下载的影响
"""

import os
import json
import lzma
from pathlib import Path
import sys
sys.path.append('src')

def analyze_sync_scan_impact():
    """分析同步扫描对比如何影响重新下载"""
    print("🔍 深入分析：同步扫描对比机制")
    print("=" * 60)
    
    print("📊 扫描对比的详细流程:")
    print("-" * 40)
    
    print("1️⃣ **快速同步模式** (默认):")
    print("   - 扫描最近3天的文件夹")
    print("   - 提取每个json.xz文件的shortcode")
    print("   - 与下载日志中的shortcode进行对比")
    print("   - 如果文件存在但日志中无记录 → 补充日志记录")
    print("   - 如果日志中有记录但文件不存在 → **不做任何操作**")
    
    print("\n2️⃣ **完整同步模式** (force_full=True):")
    print("   - 扫描所有下载文件夹")
    print("   - 全面对比所有shortcode")
    print("   - 补充所有缺失的日志记录")
    
    print("\n3️⃣ **关键判断逻辑**:")
    print("   ```python")
    print("   def is_downloaded(shortcode):")
    print("       # 步骤1: 检查下载日志")
    print("       if shortcode in download_log:")
    print("           return True  # 🚫 停止检查，不会下载")
    print("       ")
    print("       # 步骤2: 检查文件系统")
    print("       if file_exists(shortcode):")
    print("           return True  # 🚫 停止检查，不会下载")
    print("       ")
    print("       return False     # ✅ 允许下载")
    print("   ```")
    
    print("\n🎯 **核心问题解答**:")
    print("=" * 50)
    
    print("❓ 删除8-27文件夹后，扫描对比会影响下载吗？")
    print()
    
    print("**情况A: 仅删除文件夹，保留日志记录**")
    print("   📝 日志记录存在 → is_downloaded()返回True")
    print("   🚫 结果: **不会下载** (日志检查直接阻止)")
    print("   🔍 扫描对比: **无影响** (日志检查在前)")
    
    print("\n**情况B: 删除文件夹 + 删除日志记录**")
    print("   📝 日志记录不存在 → 进入文件系统检查")
    print("   📁 文件不存在 → is_downloaded()返回False")
    print("   ✅ 结果: **会重新下载**")
    print("   🔍 扫描对比: **无影响** (没有文件可扫描)")
    
    print("\n**情况C: 删除日志记录，保留文件夹**")
    print("   📝 日志记录不存在 → 进入文件系统检查")
    print("   📁 文件存在 → is_downloaded()返回True")
    print("   🚫 结果: **不会下载** (文件系统检查阻止)")
    print("   🔍 扫描对比: **会补充日志记录**")
    
    # 模拟扫描对比的具体行为
    print("\n🧪 **模拟扫描对比的实际影响**:")
    print("=" * 50)
    
    target_folder = Path("videos/downloads/ai_vanvan/2025-08-27")
    
    if target_folder.exists():
        json_files = list(target_folder.glob("*.json.xz"))
        print(f"📂 8-27文件夹: {len(json_files)} 个文件")
        
        # 读取第一个文件作为示例
        if json_files:
            try:
                with lzma.open(json_files[0], 'rb') as f:
                    data = json.loads(f.read().decode('utf-8'))
                    shortcode = data.get('node', {}).get('shortcode')
                    
                    print(f"\n📄 示例文件: {json_files[0].name}")
                    print(f"🔑 Shortcode: {shortcode}")
                    
                    print(f"\n🔄 扫描对比过程:")
                    print(f"   1. 扫描器找到文件: {json_files[0].name}")
                    print(f"   2. 提取shortcode: {shortcode}")
                    print(f"   3. 查询下载日志: 检查是否有记录")
                    print(f"   4. 如果有记录: 无操作")
                    print(f"   5. 如果无记录: 添加 sync_added=True 的记录")
                    
                    print(f"\n⚠️ **重要**: 扫描对比只是**补充日志记录**")
                    print(f"   它**不会影响**下载决策！")
                    print(f"   下载决策完全由 is_downloaded() 控制。")
                    
            except Exception as e:
                print(f"❌ 读取文件失败: {e}")
    
    else:
        print("❌ 8-27文件夹不存在")
    
    print(f"\n💡 **总结回答你的问题**:")
    print("=" * 40)
    print(f"\"删除以后在重新执行下载会有一个扫描和对比动作，对比shortcode和文件名，这个会影响下载吗\"")
    print()
    print(f"**答案: ❌ 不会影响下载**")
    print()
    print(f"**原因:**")
    print(f"1. 🎯 扫描对比的目的是**补充缺失的日志记录**")
    print(f"2. 🚫 下载决策由 is_downloaded() 独立控制")
    print(f"3. 📝 is_downloaded() 优先检查日志记录")
    print(f"4. 🔍 只有日志记录为空时才检查文件系统")
    print(f"5. ⚡ 扫描对比在下载检查**之前或之后**运行都不影响结果")
    
    print(f"\n🎯 **实际测试场景**:")
    print(f"删除8-27文件夹 → 所有日志记录仍存在 → is_downloaded()返回True → 跳过下载")
    print(f"扫描对比发现文件缺失 → 无操作 → 不影响下载决策")

def demonstrate_sync_behavior():
    """演示同步行为"""
    print(f"\n🎬 **同步行为演示**:")
    print("=" * 40)
    
    # 检查缓存文件
    cache_files = list(Path("videos/downloads").glob("**/.sync_cache"))
    
    print(f"📋 当前同步缓存:")
    if cache_files:
        for cache_file in cache_files:
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                    print(f"   📁 {cache_file.parent.name}: {cache_data.get('last_sync', 'Unknown')}")
            except:
                print(f"   📁 {cache_file.parent.name}: 缓存文件损坏")
    else:
        print(f"   ❌ 没有找到同步缓存文件")
    
    print(f"\n🔧 同步缓存的作用:")
    print(f"   - 24小时内跳过重复扫描")
    print(f"   - 提高性能，避免重复的文件系统操作")
    print(f"   - 不影响下载逻辑，只影响扫描频率")

def main():
    analyze_sync_scan_impact()
    demonstrate_sync_behavior()
    
    print(f"\n" + "="*60)
    print(f"🎯 **最终结论**:")
    print(f"扫描对比机制**不会影响**删除文件后的重新下载行为！")
    print(f"删除8-27文件夹后，这些视频**不会重新下载**，因为日志记录仍然存在。")
    print(f"要重新下载，必须同时删除文件和日志记录。")

if __name__ == "__main__":
    main()
