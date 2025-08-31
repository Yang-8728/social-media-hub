#!/usr/bin/env python3
"""
验证下载器的"新视频"判断逻辑问题
"""

import json
import lzma
from pathlib import Path
from src.utils.logger import Logger

def test_download_logic():
    """测试下载逻辑的问题"""
    
    print("🔍 下载器'新视频'判断逻辑问题分析")
    print("=" * 60)
    
    # 初始化logger
    logger = Logger("ai_vanvan")  # 修复：现在使用ai_vanvan
    
    # 获取实际文件的shortcode
    downloads_dir = Path(r"C:\Code\social-media-hub\videos\downloads\ai_vanvan")
    
    actual_shortcodes = set()
    for folder in downloads_dir.iterdir():
        if folder.is_dir() and folder.name.startswith('2025-08-'):
            for file in folder.iterdir():
                if file.name.endswith('.json.xz'):
                    try:
                        with lzma.open(file, 'rb') as f:
                            data = json.loads(f.read().decode('utf-8'))
                            shortcode = data.get('node', {}).get('shortcode')
                            if shortcode:
                                actual_shortcodes.add(shortcode)
                    except:
                        continue
    
    print(f"📁 实际文件中的shortcode数量: {len(actual_shortcodes)}")
    
    # 测试logger的is_downloaded方法
    downloaded_count = 0
    not_downloaded_count = 0
    
    for shortcode in actual_shortcodes:
        if logger.is_downloaded(shortcode):
            downloaded_count += 1
        else:
            not_downloaded_count += 1
    
    print(f"📊 Logger判断结果:")
    print(f"  ✅ 被认为已下载: {downloaded_count}")
    print(f"  🆕 被认为是新的: {not_downloaded_count}")
    
    # 检查logger使用的文件
    print(f"\n🔍 Logger配置分析:")
    print(f"  📂 Logger账号名: ai_vanvan")
    print(f"  📄 使用的日志文件: {logger.download_log_file}")
    print(f"  🎯 实际文件所在文件夹: gaoxiao")
    
    # 检查gaoxiao的日志文件
    # 这个测试不再需要，因为现在统一使用ai_vanvan
    print(f"\n📊 统一使用 ai_vanvan:")
    print(f"  ✅ 被认为已下载: {downloaded_count}")
    print(f"  🆕 被认为是新的: {not_downloaded_count}")
    
    # 分析问题
    print(f"\n❗ 问题分析:")
    
    if not_downloaded_count > 0:
        print(f"  🐛 还有未记录的文件")
        print(f"  📁 文件保存在ai_vanvan文件夹")
        print(f"  🔄 需要检查为什么没有记录")
        print(f"  📊 结果: {not_downloaded_count}个已存在文件被误判为'新视频'")
    
    # 检查账号映射问题
    print(f"\n🔧 账号映射问题:")
    print(f"  1. 下载器参数: --gaoxiao")
    print(f"  2. 映射到账号: ai_vanvan")
    print(f"  3. Logger使用: ai_vanvan_downloads.json") 
    print(f"  4. 但文件在: gaoxiao文件夹")
    print(f"  5. 实际记录在: gaoxiao_downloads.json")
    
    # 解决方案
    print(f"\n💡 解决方案:")
    print(f"  1. 修复账号映射: --gaoxiao 应该映射到 'gaoxiao'账号")
    print(f"  2. 确保所有组件都使用ai_vanvan作为账号名")
    print(f"  3. 文件夹、Logger、配置保持一致")
    
    return {
        'actual_files': len(actual_shortcodes),
        'ai_vanvan_downloaded': downloaded_count,
        'ai_vanvan_new': not_downloaded_count
    }

if __name__ == "__main__":
    result = test_download_logic()
    
    print(f"\n🎯 总结:")
    print(f"实际文件: {result['actual_files']}")
    print(f"ai_vanvan logger看到的新视频: {result['ai_vanvan_new']}")
    
    if result['ai_vanvan_new'] > 0:
        print(f"🐛 确认BUG: 还有未记录的文件！")
