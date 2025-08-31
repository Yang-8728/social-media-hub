"""
详细检查2025-08-27文件夹中的视频记录
"""
import sys
import os
import lzma
import json
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.logger import Logger

def check_specific_folder():
    print("🔍 检查 2025-08-27 文件夹中的视频...")
    
    # 检查文件夹中的视频
    folder_path = Path("videos/downloads/ai_vanvan/2025-08-27")
    
    if not folder_path.exists():
        print("❌ 文件夹不存在")
        return
    
    # 获取所有json.xz文件
    json_files = list(folder_path.glob("*.json.xz"))
    print(f"📁 文件夹中有 {len(json_files)} 个json.xz文件")
    
    # 提取shortcode
    folder_shortcodes = []
    for json_file in json_files:
        try:
            with open(json_file, 'rb') as f:
                content = lzma.decompress(f.read()).decode('utf-8')
                metadata = json.loads(content)
                shortcode = metadata.get('shortcode')
                owner = metadata.get('owner', {}).get('username', 'unknown')
                if shortcode:
                    folder_shortcodes.append((shortcode, owner, json_file.name))
        except Exception as e:
            print(f"⚠️  读取 {json_file.name} 失败: {e}")
    
    print(f"\n📝 文件夹中的视频shortcode:")
    for shortcode, owner, filename in folder_shortcodes:
        print(f"  - {shortcode} ({owner}) - {filename}")
    
    # 检查日志中的记录
    logger = Logger("ai_vanvan")
    log_data = logger.load_download_log()
    
    print(f"\n🔍 检查这些shortcode在日志中的状态:")
    for shortcode, owner, filename in folder_shortcodes:
        is_in_log = any(d["shortcode"] == shortcode and d["status"] == "success" 
                       for d in log_data["downloads"])
        status = "✅ 已记录" if is_in_log else "❌ 缺失"
        print(f"  - {shortcode}: {status}")
    
    # 统计
    in_log_count = sum(1 for shortcode, _, _ in folder_shortcodes 
                      if any(d["shortcode"] == shortcode and d["status"] == "success" 
                            for d in log_data["downloads"]))
    
    print(f"\n📊 统计:")
    print(f"  - 文件夹中的视频: {len(folder_shortcodes)} 个")
    print(f"  - 已记录在日志: {in_log_count} 个")
    print(f"  - 缺失记录: {len(folder_shortcodes) - in_log_count} 个")

if __name__ == "__main__":
    check_specific_folder()
