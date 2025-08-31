"""
下载日志同步工具
用于修复下载日志与实际文件不一致的问题
"""
import os
import json
import lzma
from datetime import datetime
from typing import Dict, List

def sync_download_logs(account_name: str) -> Dict:
    """同步下载日志与实际文件"""
    log_file = f"data/download_logs/{account_name}_downloads.json"
    base_dir = f"videos/downloads/{account_name}"
    
    # 读取现有日志
    existing_logs = {}
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for entry in data.get('downloads', []):
                    existing_logs[entry.get('shortcode')] = entry
        except Exception as e:
            print(f"读取日志文件失败: {e}")
            
    # 扫描实际文件
    found_files = []
    missing_logs = []
    
    if os.path.exists(base_dir):
        for date_folder in os.listdir(base_dir):
            date_path = os.path.join(base_dir, date_folder)
            if os.path.isdir(date_path):
                print(f"检查目录: {date_folder}")
                
                for filename in os.listdir(date_path):
                    if filename.endswith('.json.xz'):
                        json_path = os.path.join(date_path, filename)
                        try:
                            with open(json_path, 'rb') as f:
                                content = lzma.decompress(f.read()).decode('utf-8')
                                metadata = json.loads(content)
                                shortcode = metadata.get('shortcode')
                                
                                if shortcode:
                                    found_files.append({
                                        'shortcode': shortcode,
                                        'date_folder': date_folder,
                                        'file_path': json_path,
                                        'metadata': metadata
                                    })
                                    
                                    # 检查是否在日志中
                                    if shortcode not in existing_logs:
                                        missing_logs.append({
                                            'shortcode': shortcode,
                                            'date_folder': date_folder,
                                            'owner': metadata.get('owner', {}).get('username', 'unknown'),
                                            'caption': metadata.get('edge_media_to_caption', {}).get('edges', [{}])[0].get('node', {}).get('text', '')[:100],
                                            'taken_at': metadata.get('taken_at_timestamp')
                                        })
                        except Exception as e:
                            print(f"处理文件 {filename} 时出错: {e}")
    
    result = {
        'total_files_found': len(found_files),
        'missing_in_logs': len(missing_logs),
        'missing_logs_details': missing_logs,
        'sync_needed': len(missing_logs) > 0
    }
    
    return result

def fix_missing_logs(account_name: str, missing_logs: List[Dict]) -> bool:
    """修复缺失的日志记录"""
    log_file = f"data/download_logs/{account_name}_downloads.json"
    
    try:
        # 读取现有日志
        data = {"account": account_name, "downloads": [], "merged_sessions": []}
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        # 添加缺失的记录
        for entry in missing_logs:
            new_log = {
                "shortcode": entry['shortcode'],
                "download_time": datetime.now().isoformat(),
                "status": "success",
                "file_path": f"videos/downloads/{account_name}/{entry['date_folder']}",
                "error": "",
                "merged": False,
                "download_folder": f"videos/downloads/{account_name}/{entry['date_folder']}",
                "blogger_name": entry['owner'],
                "sync_fix": True  # 标记为同步修复
            }
            data['downloads'].append(new_log)
        
        # 备份原文件
        if os.path.exists(log_file):
            backup_file = f"{log_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(log_file, backup_file)
        
        # 写入新日志
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"修复日志失败: {e}")
        return False

if __name__ == "__main__":
    # 检查ai_vanvan的同步状态
    result = sync_download_logs("ai_vanvan")
    print(f"检查结果:")
    print(f"- 找到文件: {result['total_files_found']} 个")
    print(f"- 缺失日志: {result['missing_in_logs']} 个")
    
    if result['sync_needed']:
        print(f"\n缺失的日志记录:")
        for log in result['missing_logs_details']:
            print(f"  - {log['shortcode']} ({log['owner']}) 在 {log['date_folder']}")
        
        # 询问是否修复
        response = input(f"\n是否修复这些缺失的日志? (y/n): ")
        if response.lower() == 'y':
            if fix_missing_logs("ai_vanvan", result['missing_logs_details']):
                print("✅ 日志同步完成!")
            else:
                print("❌ 日志同步失败!")
    else:
        print("✅ 日志与文件同步正常!")
