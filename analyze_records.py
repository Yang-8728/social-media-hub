"""
分析下载记录与实际文件的对应关系
"""
import json
import os
from datetime import datetime

def analyze_ai_vanvan_records():
    # 读取下载记录
    with open('videos/download_logs/ai_vanvan_downloads.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 gaoxiao下载记录分析：")
    print(f"总记录数：{len(data['downloads'])}")
    
    # 统计各状态
    merged_count = 0
    unmerged_count = 0
    success_count = 0
    
    # 按日期分组统计
    date_stats = {}
    recent_unmerged = []
    
    for record in data['downloads']:
        # 统计状态
        if record.get('merged', False):
            merged_count += 1
        else:
            unmerged_count += 1
            
        if record.get('status') == 'success':
            success_count += 1
            
        # 分析下载时间
        download_time = record.get('download_time', '')
        if download_time and download_time != '2025-01-01T00:00:00':  # 不是默认时间
            try:
                date_obj = datetime.fromisoformat(download_time.replace('Z', '+00:00'))
                date_str = date_obj.strftime('%Y-%m-%d')
                
                if date_str not in date_stats:
                    date_stats[date_str] = {'total': 0, 'merged': 0, 'unmerged': 0}
                
                date_stats[date_str]['total'] += 1
                if record.get('merged', False):
                    date_stats[date_str]['merged'] += 1
                else:
                    date_stats[date_str]['unmerged'] += 1
                    
                # 收集最近的未合并记录
                if not record.get('merged', False) and date_str >= '2025-08-20':
                    recent_unmerged.append({
                        'date': date_str,
                        'shortcode': record.get('shortcode', ''),
                        'file_path': record.get('file_path', '')
                    })
            except:
                pass
    
    print(f"✅ 已合并：{merged_count}")
    print(f"❌ 未合并：{unmerged_count}")
    print(f"✨ 成功状态：{success_count}")
    print()
    
    # 显示实际文件数量
    actual_files_8_25 = 0
    actual_files_8_26 = 0
    
    gaoxiao_25_path = 'videos/downloads/gaoxiao/2025-08-25'
    gaoxiao_26_path = 'videos/downloads/gaoxiao/2025-08-26'
    
    if os.path.exists(gaoxiao_25_path):
        actual_files_8_25 = len([f for f in os.listdir(gaoxiao_25_path) if f.endswith('.mp4')])
    
    if os.path.exists(gaoxiao_26_path):
        actual_files_8_26 = len([f for f in os.listdir(gaoxiao_26_path) if f.endswith('.mp4')])
    
    print(f"📁 实际视频文件：")
    print(f"   2025-08-25: {actual_files_8_25}个")
    print(f"   2025-08-26: {actual_files_8_26}个")
    print(f"   总计: {actual_files_8_25 + actual_files_8_26}个")
    print()
    
    # 显示按日期的统计
    print(f"📅 按日期分组统计（仅显示有数据的日期）：")
    for date_str in sorted(date_stats.keys()):
        stats = date_stats[date_str]
        if stats['total'] > 0:
            print(f"   {date_str}: 总共{stats['total']}个, 已合并{stats['merged']}个, 未合并{stats['unmerged']}个")
    
    print()
    print(f"🔍 最近的未合并记录 (8-20以后)：")
    for item in recent_unmerged[:10]:  # 显示前10个
        print(f"   {item['date']}: {item['shortcode']} - {item['file_path']}")
    
    if len(recent_unmerged) > 10:
        print(f"   ... 还有{len(recent_unmerged) - 10}个未合并记录")

if __name__ == "__main__":
    analyze_ai_vanvan_records()
