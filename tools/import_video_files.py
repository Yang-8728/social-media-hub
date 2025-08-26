#!/usr/bin/env python3
"""
扫描原项目的视频文件并导入下载记录
防止重复下载已下载的视频
"""
import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.logger import Logger

class VideoFileImporter:
    """视频文件扫描和导入器"""
    
    def __init__(self):
        self.old_project_path = "C:/Code/insDownloader"
        self.video_directories = [
            "test_downloads",
            "test_downloads_aigf8728", 
            "test_downloads_vanvan"
        ]
    
    def extract_shortcode_from_filename(self, filename):
        """从文件名中提取Instagram shortcode"""
        # 匹配 blogger__shortcode.mp4 格式
        match = re.search(r'([a-zA-Z0-9_]+)__([a-zA-Z0-9_-]{11})\.mp4', filename)
        if match:
            blogger_name = match.group(1)
            shortcode = match.group(2)
            return shortcode, blogger_name
        
        # 匹配 blogger_shortcode.mp4 格式
        match = re.search(r'([a-zA-Z0-9_]+)_([a-zA-Z0-9_-]{11})\.mp4', filename)
        if match:
            blogger_name = match.group(1) 
            shortcode = match.group(2)
            return shortcode, blogger_name
        
        return None, None
    
    def generate_virtual_shortcode(self, filename):
        """为没有shortcode的视频生成虚拟shortcode"""
        # 从日期格式的文件名生成虚拟shortcode
        date_match = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})_UTC\.mp4', filename)
        if date_match:
            date_str = date_match.group(1)
            # 生成基于日期的虚拟shortcode（确保11位）
            date_clean = date_str.replace('-', '').replace('_', '')[:11]
            return f"VID{date_clean}"
        
        # 如果没有日期格式，生成基于文件名hash的shortcode
        import hashlib
        hash_obj = hashlib.md5(filename.encode())
        return f"VID{hash_obj.hexdigest()[:8]}"
    
    def scan_video_directory(self, directory_name):
        """扫描指定目录的视频文件"""
        directory_path = os.path.join(self.old_project_path, directory_name)
        
        if not os.path.exists(directory_path):
            print(f"❌ 目录不存在: {directory_path}")
            return []
        
        print(f"📁 扫描目录: {directory_name}")
        
        video_records = []
        mp4_files = [f for f in os.listdir(directory_path) if f.endswith('.mp4')]
        
        print(f"   找到 {len(mp4_files)} 个MP4文件")
        
        for filename in mp4_files:
            # 尝试从文件名提取shortcode
            shortcode, blogger_name = self.extract_shortcode_from_filename(filename)
            
            if not shortcode:
                # 生成虚拟shortcode
                shortcode = self.generate_virtual_shortcode(filename)
                blogger_name = "ai_vanvan"  # 默认账号
            
            file_path = os.path.join(directory_path, filename)
            file_size = os.path.getsize(file_path)
            
            record = {
                "shortcode": shortcode,
                "blogger_name": blogger_name,
                "filename": filename,
                "directory": directory_name,
                "file_path": file_path,
                "file_size": file_size,
                "is_virtual": shortcode.startswith("VID")
            }
            
            video_records.append(record)
        
        return video_records
    
    def import_to_account_log(self, account_name, records):
        """将记录导入到指定账号的日志中"""
        logger = Logger(account_name)
        
        # 加载现有记录
        existing_data = logger.load_download_log()
        existing_shortcodes = {d["shortcode"] for d in existing_data["downloads"]}
        
        imported_count = 0
        skipped_count = 0
        
        for record in records:
            shortcode = record["shortcode"]
            
            if shortcode in existing_shortcodes:
                skipped_count += 1
                continue
            
            # 创建下载记录
            download_record = {
                "shortcode": shortcode,
                "download_time": datetime.now().isoformat(),
                "status": "success",
                "file_path": record["file_path"],
                "error": "",
                "merged": True,
                "download_folder": record["directory"],
                "blogger_name": record["blogger_name"],
                "imported_from_old_project": True,
                "original_filename": record["filename"],
                "file_size": record["file_size"],
                "is_virtual_shortcode": record["is_virtual"]
            }
            
            existing_data["downloads"].append(download_record)
            imported_count += 1
        
        # 保存更新后的记录
        logger.save_download_log(existing_data)
        
        return imported_count, skipped_count
    
    def import_all_video_files(self):
        """扫描并导入所有视频文件"""
        print("🔄 开始扫描原项目的视频文件...")
        print("=" * 60)
        
        all_records = []
        total_files = 0
        
        # 扫描所有视频目录
        for directory in self.video_directories:
            records = self.scan_video_directory(directory)
            all_records.extend(records)
            total_files += len(records)
        
        print(f"\n📊 扫描结果:")
        print(f"   总文件数: {total_files}")
        
        # 按账号分类记录
        account_records = {
            "ai_vanvan": [],
            "aigf8728": []
        }
        
        for record in all_records:
            if "aigf8728" in record["directory"] or record["blogger_name"] == "aigf8728":
                account_records["aigf8728"].append(record)
            else:
                account_records["ai_vanvan"].append(record)
        
        print(f"   ai_vanvan账号: {len(account_records['ai_vanvan'])} 个文件")
        print(f"   aigf8728账号: {len(account_records['aigf8728'])} 个文件")
        
        # 统计shortcode类型
        real_shortcodes = sum(1 for r in all_records if not r["is_virtual"])
        virtual_shortcodes = sum(1 for r in all_records if r["is_virtual"])
        
        print(f"   真实shortcode: {real_shortcodes} 个")
        print(f"   虚拟shortcode: {virtual_shortcodes} 个")
        
        print("\n🔄 开始导入记录...")
        print("-" * 40)
        
        total_imported = 0
        
        for account_name, records in account_records.items():
            if not records:
                continue
                
            print(f"\n📱 导入账号: {account_name}")
            
            imported, skipped = self.import_to_account_log(account_name, records)
            
            print(f"   ✅ 新导入: {imported} 个")
            print(f"   ⏭️ 已存在: {skipped} 个")
            
            total_imported += imported
        
        print(f"\n🎉 导入完成！")
        print(f"   总共导入: {total_imported} 个记录")
        print(f"   总文件数: {total_files} 个")
        print("\n💡 现在运行下载命令时，这些视频会被自动跳过，避免重复下载")

def main():
    """主函数"""
    importer = VideoFileImporter()
    
    print("⚠️  重要提示:")
    print("这个工具会扫描原项目的所有视频文件并导入记录到新项目")
    print("包括有shortcode和无shortcode的视频文件")
    print("导入后，这些视频在新项目中会被标记为'已下载'")
    print()
    
    confirm = input("确认要扫描并导入吗？(y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ 导入已取消")
        return
    
    importer.import_all_video_files()

if __name__ == "__main__":
    main()
