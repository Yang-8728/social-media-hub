"""
修复路径问题并分析文件记录对应关系
"""
import json
import os
from collections import defaultdict

def fix_paths_and_analyze():
    # 读取下载记录
    with open('videos/download_logs/gaoxiao_downloads.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("🔧 修复路径问题...")
    fixed_count = 0
    
    # 修复路径
    for record in data['downloads']:
        file_path = record.get('file_path', '')
        
        # 修复路径中的ai_vanvan
        if 'ai_vanvan' in file_path:
            # 替换路径
            new_path = file_path.replace('videos\\downloads\\ai_vanvan', 'videos/downloads/gaoxiao')
            new_path = new_path.replace('videos/downloads/ai_vanvan', 'videos/downloads/gaoxiao')
            record['file_path'] = new_path
            fixed_count += 1
    
    print(f"✅ 修复了 {fixed_count} 个路径")
    
    # 保存修复后的数据
    with open('videos/download_logs/gaoxiao_downloads.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("💾 已保存修复后的记录")
    
    # 分析文件和记录对应关系
    print("\n📊 分析文件和记录对应关系...")
    
    # 收集实际文件
    actual_files = set()
    for root, dirs, files in os.walk('videos/downloads/gaoxiao'):
        for file in files:
            if file.endswith('.mp4'):
                # 提取文件的基本信息（时间戳）
                if '_UTC.mp4' in file:
                    timestamp = file.replace('_UTC.mp4', '')
                    actual_files.add(timestamp)
    
    print(f"📁 实际文件数量: {len(actual_files)}")
    
    # 分析记录
    recent_records = []
    missing_files = []
    extra_records = []
    
    for record in data['downloads']:
        download_time = record.get('download_time', '')
        if download_time and download_time.startswith('2025-08-2'):  # 最近的记录
            recent_records.append(record)
            
            # 检查是否有对应文件
            shortcode = record.get('shortcode', '')
            file_path = record.get('file_path', '')
            
            # 尝试在实际文件中找到匹配
            found = False
            for actual_file in actual_files:
                # 简单匹配（这里可能需要更复杂的逻辑）
                if shortcode in actual_file or actual_file in file_path:
                    found = True
                    break
            
            if not found:
                extra_records.append({
                    'shortcode': shortcode,
                    'date': download_time[:10],
                    'file_path': file_path
                })
    
    print(f"📋 最近记录数量: {len(recent_records)}")
    print(f"❌ 可能的多余记录: {len(extra_records)}")
    
    # 按日期分组
    date_groups = defaultdict(list)
    file_date_groups = defaultdict(set)
    
    for record in recent_records:
        date = record.get('download_time', '')[:10]
        date_groups[date].append(record)
    
    # 按日期分组实际文件
    for actual_file in actual_files:
        # 从文件名提取日期
        if '2025-' in actual_file:
            parts = actual_file.split('_')
            if len(parts) >= 2:
                date_part = parts[0]  # 2025-08-25
                file_date_groups[date_part].add(actual_file)
    
    print("\n📅 按日期详细对比:")
    for date in sorted(set(list(date_groups.keys()) + list(file_date_groups.keys()))):
        records_count = len(date_groups.get(date, []))
        files_count = len(file_date_groups.get(date, set()))
        
        if records_count > 0 or files_count > 0:
            status = "✅" if records_count == files_count else "❌"
            print(f"   {date}: {status} 记录{records_count}个, 文件{files_count}个")
            
            if records_count != files_count:
                print(f"      差异: {records_count - files_count}")
                
                # 显示具体的记录
                if date in date_groups:
                    print(f"      记录: {[r.get('shortcode', '') for r in date_groups[date][:5]]}...")
                if date in file_date_groups:
                    print(f"      文件: {list(file_date_groups[date])[:5]}...")
    
    # 显示一些具体的不匹配情况
    if extra_records:
        print(f"\n🔍 可能的问题记录 (前10个):")
        for record in extra_records[:10]:
            print(f"   {record['date']}: {record['shortcode']} - {record['file_path']}")

if __name__ == "__main__":
    fix_paths_and_analyze()
