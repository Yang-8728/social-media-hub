#!/usr/bin/env python3
"""
精确检查记录与文件的对应关系
"""

import json
import lzma
import os
from pathlib import Path

def check_record_file_mapping():
    """检查记录与文件的精确对应关系"""
    
    print("🔍 记录与文件对应关系精确检查")
    print("=" * 60)
    
    # 加载下载记录
    log_path = Path(r"C:\Code\social-media-hub\videos\download_logs\gaoxiao_downloads.json")
    with open(log_path, 'r', encoding='utf-8') as f:
        download_data = json.load(f)
    
    downloads = download_data.get('downloads', [])
    unmerged_downloads = [d for d in downloads if d.get('status') == 'success' and not d.get('merged', False)]
    
    print(f"📋 未合并记录: {len(unmerged_downloads)} 个")
    
    # 获取实际文件和它们的shortcode
    downloads_dir = Path(r"C:\Code\social-media-hub\videos\downloads\gaoxiao")
    
    file_shortcodes = {}
    mp4_files = []
    
    for folder in downloads_dir.iterdir():
        if folder.is_dir() and folder.name.startswith('2025-08-'):
            for file in folder.iterdir():
                if file.suffix == '.mp4':
                    mp4_files.append(file)
                    # 尝试从对应的JSON文件获取shortcode
                    json_file = file.with_suffix('.json.xz')
                    if json_file.exists():
                        try:
                            with lzma.open(json_file, 'rb') as f:
                                data = json.loads(f.read().decode('utf-8'))
                                shortcode = data.get('node', {}).get('shortcode')
                                if shortcode:
                                    file_shortcodes[shortcode] = {
                                        'mp4_path': file,
                                        'json_path': json_file
                                    }
                        except Exception as e:
                            print(f"⚠️  无法读取 {json_file}: {e}")
    
    print(f"🎥 实际MP4文件: {len(mp4_files)} 个")
    print(f"🔗 有shortcode的文件: {len(file_shortcodes)} 个")
    
    # 检查记录与文件的匹配情况
    record_shortcodes = {d['shortcode'] for d in unmerged_downloads}
    file_shortcode_set = set(file_shortcodes.keys())
    
    # 匹配的shortcode
    matched_shortcodes = record_shortcodes & file_shortcode_set
    
    # 只有记录没有文件的shortcode
    record_only = record_shortcodes - file_shortcode_set
    
    # 只有文件没有记录的shortcode
    file_only = file_shortcode_set - record_shortcodes
    
    print(f"\n📊 匹配结果:")
    print(f"  ✅ 完美匹配: {len(matched_shortcodes)} 个")
    print(f"  📋 仅有记录: {len(record_only)} 个")
    print(f"  📁 仅有文件: {len(file_only)} 个")
    
    if record_only:
        print(f"\n📋 只有记录没有文件的shortcode:")
        for i, shortcode in enumerate(sorted(record_only), 1):
            # 找到对应的记录
            record = next((d for d in unmerged_downloads if d['shortcode'] == shortcode), None)
            if record:
                download_time = record.get('download_time', 'NO_TIME')[:16]  # 只显示到分钟
                blogger = record.get('blogger_name', 'unknown')
                print(f"  {i:2d}. {shortcode} - {download_time} - {blogger}")
            else:
                print(f"  {i:2d}. {shortcode} - 记录丢失")
    
    if file_only:
        print(f"\n📁 只有文件没有记录的shortcode:")
        for i, shortcode in enumerate(sorted(file_only), 1):
            file_info = file_shortcodes[shortcode]
            print(f"  {i:2d}. {shortcode} - {file_info['mp4_path'].name}")
    
    # 分析缺失文件的原因
    if record_only:
        print(f"\n🔍 缺失文件原因分析:")
        test_fix_count = 0
        real_missing_count = 0
        
        for shortcode in record_only:
            if shortcode.startswith('TEST_') or shortcode.startswith('FIX_'):
                test_fix_count += 1
            else:
                real_missing_count += 1
        
        print(f"  🧪 测试/修复记录: {test_fix_count} 个")
        print(f"  ❌ 真正缺失文件: {real_missing_count} 个")
    
    # 最终可合并数量
    actual_mergeable = len(matched_shortcodes)
    
    print(f"\n🎬 实际可合并视频:")
    print(f"  📈 确认可合并: {actual_mergeable} 个视频")
    print(f"  📁 对应文件数: {len(mp4_files)} 个")
    
    if actual_mergeable == len(mp4_files):
        print(f"  ✅ 完美对应！所有文件都可以合并")
    else:
        print(f"  ⚠️  数量不匹配，需要进一步检查")
    
    return {
        'unmerged_records': len(unmerged_downloads),
        'mp4_files': len(mp4_files),
        'matched': len(matched_shortcodes),
        'record_only': len(record_only),
        'file_only': len(file_only),
        'actual_mergeable': actual_mergeable
    }

if __name__ == "__main__":
    result = check_record_file_mapping()
    
    print(f"\n🎯 合并总结:")
    print(f"实际可合并: {result['actual_mergeable']} 个视频")
    print(f"对应文件: {result['mp4_files']} 个")
    
    if result['actual_mergeable'] > 0:
        print(f"✅ 可以进行视频合并！")
    else:
        print(f"❌ 没有可合并的视频")
