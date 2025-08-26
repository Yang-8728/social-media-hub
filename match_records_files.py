"""
基于shortcode精确匹配记录和文件
"""
import json
import os
import re
from collections import defaultdict

def extract_shortcode_from_filename(filename):
    """从文件名中提取可能的shortcode"""
    # 移除扩展名
    name = filename.replace('.mp4', '').replace('.jpg', '').replace('.txt', '').replace('.json.xz', '')
    
    # 如果是时间戳格式，我们需要其他方法匹配
    if re.match(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_UTC', name):
        return None
    
    return name

def find_matching_files():
    """通过目录结构和文件名匹配记录和文件"""
    
    # 读取下载记录
    with open('videos/download_logs/gaoxiao_downloads.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("🔍 通过目录和文件内容匹配记录和文件...")
    
    # 收集所有文件和对应信息
    all_files = {}  # {文件路径: {文件信息}}
    
    for root, dirs, files in os.walk('videos/downloads/gaoxiao'):
        for file in files:
            if file.endswith('.mp4'):
                full_path = os.path.join(root, file)
                relative_path = full_path.replace('videos\\downloads\\gaoxiao\\', '').replace('videos/downloads/gaoxiao/', '')
                
                # 查找同名的txt文件（包含shortcode）
                txt_file = file.replace('.mp4', '.txt')
                txt_path = os.path.join(root, txt_file)
                
                shortcode = None
                if os.path.exists(txt_path):
                    try:
                        with open(txt_path, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                            # shortcode通常在第一行
                            if content:
                                shortcode = content.split('\n')[0].strip()
                    except:
                        pass
                
                all_files[relative_path] = {
                    'mp4_file': file,
                    'full_path': full_path,
                    'shortcode': shortcode,
                    'size': os.path.getsize(full_path) if os.path.exists(full_path) else 0
                }
    
    print(f"📁 找到 {len(all_files)} 个视频文件")
    
    # 匹配记录
    matched_records = []
    unmatched_records = []
    unmatched_files = list(all_files.keys())
    
    recent_records = [r for r in data['downloads'] if r.get('download_time', '').startswith('2025-08-2')]
    
    for record in recent_records:
        record_shortcode = record.get('shortcode', '')
        matched = False
        
        # 尝试通过shortcode匹配
        for file_path, file_info in all_files.items():
            if file_info['shortcode'] == record_shortcode:
                matched_records.append({
                    'record': record,
                    'file': file_info,
                    'match_type': 'shortcode'
                })
                if file_path in unmatched_files:
                    unmatched_files.remove(file_path)
                matched = True
                break
        
        if not matched:
            unmatched_records.append(record)
    
    print(f"✅ 成功匹配: {len(matched_records)} 个")
    print(f"❌ 未匹配记录: {len(unmatched_records)} 个")
    print(f"📄 未匹配文件: {len(unmatched_files)} 个")
    
    # 显示详细信息
    print(f"\n📊 匹配结果详情:")
    
    # 按日期分组匹配结果
    date_matches = defaultdict(list)
    for match in matched_records:
        date = match['record'].get('download_time', '')[:10]
        date_matches[date].append(match)
    
    for date in sorted(date_matches.keys()):
        matches = date_matches[date]
        print(f"   {date}: {len(matches)} 个匹配")
    
    # 显示一些未匹配的记录
    if unmatched_records:
        print(f"\n❌ 未匹配的记录 (前10个):")
        for record in unmatched_records[:10]:
            print(f"   {record.get('download_time', '')[:10]}: {record.get('shortcode', '')} - {record.get('file_path', '')}")
    
    # 显示一些未匹配的文件
    if unmatched_files:
        print(f"\n📄 未匹配的文件 (前10个):")
        for file_path in unmatched_files[:10]:
            file_info = all_files[file_path]
            print(f"   {file_path}: shortcode={file_info['shortcode']}")
    
    # 检查是否有下载失败的情况
    failed_downloads = len(unmatched_records)
    if failed_downloads > 0:
        print(f"\n⚠️  可能有 {failed_downloads} 个下载失败的记录")
    
    return {
        'total_records': len(recent_records),
        'total_files': len(all_files),
        'matched': len(matched_records),
        'unmatched_records': len(unmatched_records),
        'unmatched_files': len(unmatched_files)
    }

if __name__ == "__main__":
    result = find_matching_files()
    print(f"\n📋 总结:")
    print(f"   记录总数: {result['total_records']}")
    print(f"   文件总数: {result['total_files']}")
    print(f"   成功匹配: {result['matched']}")
    print(f"   失败下载: {result['unmatched_records']}")
    print(f"   孤立文件: {result['unmatched_files']}")
