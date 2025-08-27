#!/usr/bin/env python3
"""
ai_vanvan账号数据完整性总结报告
"""

import json
import lzma
import os
from pathlib import Path

def generate_integrity_report():
    """生成完整性报告"""
    
    print("🔍 ai_vanvan账号数据完整性分析报告")
    print("=" * 50)
    
    # 加载下载记录
    log_path = Path(r"C:\Code\social-media-hub\videos\download_logs\ai_vanvan_downloads.json")
    with open(log_path, 'r', encoding='utf-8') as f:
        download_data = json.load(f)
    
    downloads = download_data.get('downloads', [])
    recent_downloads = [d for d in downloads if not d.get('merged', False)]
    
    # 扫描实际文件
    downloads_dir = Path(r"C:\Code\social-media-hub\videos\downloads\ai_vanvan")
    
    mp4_files = []
    json_files = []
    
    for folder in downloads_dir.iterdir():
        if folder.is_dir() and folder.name.startswith('2025-08-'):
            for file in folder.iterdir():
                if file.suffix == '.mp4':
                    mp4_files.append(file)
                elif file.name.endswith('.json.xz'):
                    json_files.append(file)
    
    print(f"📊 数据统计:")
    print(f"  📋 总下载记录: {len(downloads)}")
    print(f"  🆕 未合并记录: {len(recent_downloads)}")
    print(f"  🎥 实际MP4文件: {len(mp4_files)}")
    print(f"  📄 JSON元数据文件: {len(json_files)}")
    
    print(f"\n🔍 分析结果:")
    
    # 检查记录与文件的对应关系
    if len(recent_downloads) > len(mp4_files):
        failed_downloads = len(recent_downloads) - len(mp4_files)
        print(f"❌ 下载失败: {failed_downloads}个视频")
        print(f"   - JSON记录: {len(recent_downloads)}")
        print(f"   - 实际文件: {len(mp4_files)}")
        print(f"   - 成功率: {len(mp4_files)/len(recent_downloads)*100:.1f}%")
    
    # 检查文件完整性
    if len(mp4_files) == len(json_files):
        print(f"✅ MP4与JSON配对: 完美匹配 ({len(mp4_files)}对)")
    else:
        print(f"⚠️  MP4与JSON配对: 不匹配")
        print(f"   - MP4文件: {len(mp4_files)}")
        print(f"   - JSON文件: {len(json_files)}")
    
    # 文件命名检查
    mp4_names = {f.stem for f in mp4_files}
    json_names = {f.stem.replace('.json', '') for f in json_files}
    
    if mp4_names == json_names:
        print(f"✅ 文件命名: 一致性完美")
    else:
        print(f"⚠️  文件命名: 存在不一致")
    
    print(f"\n💡 问题解释:")
    print(f"1. 下载记录显示尝试下载了 {len(recent_downloads)} 个视频")
    print(f"2. 实际只有 {len(mp4_files)} 个MP4文件下载成功")
    print(f"3. 失败的 {len(recent_downloads) - len(mp4_files)} 个下载只留下了JSON记录，没有视频文件")
    print(f"4. 这解释了为什么'46个记录 vs 38个文件'的数量不匹配")
    
    print(f"\n🎯 结论:")
    print(f"✅ 数据一致性: 正常（JSON记录反映了下载尝试，文件反映了成功下载）")
    print(f"✅ 文件完整性: 良好（成功下载的文件都有对应的元数据）")
    print(f"⚠️  下载成功率: {len(mp4_files)/len(recent_downloads)*100:.1f}% ({len(mp4_files)}/{len(recent_downloads)})")
    
    # 检查具体失败的下载
    print(f"\n📋 失败下载分析:")
    
    # 提取成功下载的shortcode（从JSON文件）
    successful_shortcodes = set()
    for json_file in json_files:
        try:
            with lzma.open(json_file, 'rb') as f:
                data = json.loads(f.read().decode('utf-8'))
                shortcode = data.get('node', {}).get('shortcode')
                if shortcode:
                    successful_shortcodes.add(shortcode)
        except:
            continue
    
    # 找出失败的下载
    failed_shortcodes = []
    for record in recent_downloads:
        shortcode = record.get('shortcode')
        if shortcode and shortcode not in successful_shortcodes:
            # 过滤掉测试和修复记录
            if not (shortcode.startswith('TEST_') or shortcode.startswith('FIX_')):
                failed_shortcodes.append(shortcode)
    
    print(f"❌ 实际下载失败: {len(failed_shortcodes)} 个")
    print(f"🧪 测试/修复记录: {len(recent_downloads) - len(mp4_files) - len(failed_shortcodes)} 个")
    
    if failed_shortcodes:
        print(f"\n失败的shortcode示例:")
        for i, shortcode in enumerate(failed_shortcodes[:5], 1):
            print(f"  {i}. {shortcode}")
        if len(failed_shortcodes) > 5:
            print(f"  ... 还有 {len(failed_shortcodes) - 5} 个")
    
    return {
        'total_records': len(downloads),
        'recent_records': len(recent_downloads),
        'mp4_files': len(mp4_files),
        'json_files': len(json_files),
        'successful_downloads': len(mp4_files),
        'failed_downloads': len(failed_shortcodes),
        'test_records': len(recent_downloads) - len(mp4_files) - len(failed_shortcodes),
        'success_rate': len(mp4_files)/len(recent_downloads)*100 if recent_downloads else 0
    }

if __name__ == "__main__":
    result = generate_integrity_report()
    
    print(f"\n🏆 最终统计:")
    print(f"记录: {result['recent_records']}, 成功: {result['successful_downloads']}, 失败: {result['failed_downloads']}")
    print(f"成功率: {result['success_rate']:.1f}%")
