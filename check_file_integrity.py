#!/usr/bin/env python3
"""
检查文件完整性 - 对比下载记录与实际文件
"""

import json
import lzma
import os
from pathlib import Path

def extract_shortcode_from_json_xz(json_xz_path):
    """从json.xz文件中提取shortcode"""
    try:
        with lzma.open(json_xz_path, 'rb') as f:
            data = json.loads(f.read().decode('utf-8'))
            return data.get('node', {}).get('shortcode')
    except Exception as e:
        print(f"无法读取 {json_xz_path}: {e}")
        return None

def check_ai_vanvan_integrity():
    """检查ai_vanvan账号的文件完整性"""
    # 加载下载记录
    log_path = Path(r"C:\Code\social-media-hub\videos\download_logs\ai_vanvan_downloads.json")
    with open(log_path, 'r', encoding='utf-8') as f:
        download_data = json.load(f)
    
    downloads = download_data.get('downloads', [])
    recent_downloads = [d for d in downloads if not d.get('merged', False)]
    
    print(f"🔍 检查ai_vanvan账号文件完整性")
    print(f"📋 总下载记录: {len(downloads)}")
    print(f"🆕 未合并记录: {len(recent_downloads)}")
    
    # 扫描实际文件
    downloads_dir = Path(r"C:\Code\social-media-hub\videos\downloads\gaoxiao")
    
    # 获取所有MP4文件
    mp4_files = []
    json_files = []
    
    for folder in downloads_dir.iterdir():
        if folder.is_dir() and folder.name.startswith('2025-08-'):
            for file in folder.iterdir():
                if file.suffix == '.mp4':
                    mp4_files.append(file)
                elif file.name.endswith('.json.xz'):
                    json_files.append(file)
    
    print(f"🎥 实际MP4文件: {len(mp4_files)}")
    print(f"📄 JSON元数据文件: {len(json_files)}")
    
    # 从JSON文件提取shortcode
    file_shortcodes = {}
    for json_file in json_files:
        shortcode = extract_shortcode_from_json_xz(json_file)
        if shortcode:
            # 对应的MP4文件（同名但后缀不同）
            mp4_file = json_file.with_suffix('.mp4')
            if mp4_file.exists():
                file_shortcodes[shortcode] = {
                    'mp4_path': mp4_file,
                    'json_path': json_file,
                    'matched': False
                }
            else:
                print(f"⚠️  JSON有shortcode但缺失MP4: {json_file.name} -> {shortcode}")
    
    print(f"✅ 有效shortcode: {len(file_shortcodes)}")
    
    # 匹配记录
    record_shortcodes = {}
    matched_count = 0
    missing_files = []
    
    for record in recent_downloads:
        shortcode = record.get('shortcode')
        if shortcode:
            record_shortcodes[shortcode] = record
            if shortcode in file_shortcodes:
                file_shortcodes[shortcode]['matched'] = True
                matched_count += 1
            else:
                missing_files.append(record)
    
    # 孤儿文件（有文件但没有记录）
    orphan_files = [info for shortcode, info in file_shortcodes.items() 
                   if not info['matched']]
    
    print(f"\n📊 匹配结果:")
    print(f"✅ 成功匹配: {matched_count}")
    print(f"❌ 缺失文件: {len(missing_files)}")
    print(f"🏷️  孤儿文件: {len(orphan_files)}")
    
    if missing_files:
        print(f"\n❌ 缺失的文件 ({len(missing_files)}):")
        for i, record in enumerate(missing_files, 1):
            print(f"  {i}. {record.get('shortcode', 'NO_SHORTCODE')} - {record.get('download_time', 'NO_TIME')}")
    
    if orphan_files:
        print(f"\n🏷️  孤儿文件 ({len(orphan_files)}):")
        for i, info in enumerate(orphan_files, 1):
            print(f"  {i}. {info['mp4_path'].name}")
    
    # 验证文件-JSON对应关系
    print(f"\n🔗 文件-JSON对应关系:")
    mp4_without_json = []
    json_without_mp4 = []
    
    for json_file in json_files:
        mp4_file = json_file.with_suffix('.mp4')
        if not mp4_file.exists():
            json_without_mp4.append(json_file)
    
    for mp4_file in mp4_files:
        json_file = mp4_file.with_suffix('.json.xz')
        if not json_file.exists():
            mp4_without_json.append(mp4_file)
    
    print(f"📄 JSON无对应MP4: {len(json_without_mp4)}")
    print(f"🎥 MP4无对应JSON: {len(mp4_without_json)}")
    
    if json_without_mp4:
        print("  JSON无MP4:")
        for f in json_without_mp4:
            print(f"    {f.name}")
    
    if mp4_without_json:
        print("  MP4无JSON:")
        for f in mp4_without_json:
            print(f"    {f.name}")
    
    return {
        'total_records': len(downloads),
        'recent_records': len(recent_downloads),
        'mp4_files': len(mp4_files),
        'json_files': len(json_files),
        'matched': matched_count,
        'missing_files': len(missing_files),
        'orphan_files': len(orphan_files),
        'json_without_mp4': len(json_without_mp4),
        'mp4_without_json': len(mp4_without_json)
    }

if __name__ == "__main__":
    result = check_ai_vanvan_integrity()
    
    print(f"\n🎯 完整性总结:")
    print(f"记录: {result['recent_records']}, 文件: {result['mp4_files']}, 匹配: {result['matched']}")
    print(f"丢失: {result['missing_files']}, 孤儿: {result['orphan_files']}")
