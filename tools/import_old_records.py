#!/usr/bin/env python3
"""
导入原项目的下载记录到新项目
防止重复下载已下载的视频
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.logger import Logger

class DownloadRecordImporter:
    """下载记录导入器"""
    
    def __init__(self):
        self.old_project_path = "C:/Code/insDownloader"
        self.accounts = {
            "ai_vanvan": "test_logs/test_downloaded_ai_vanvan.log",
            "aigf8728": "test_logs/test_downloaded_aigf8728.log"
        }
    
    def import_account_records(self, account_name: str) -> dict:
        """导入指定账号的下载记录"""
        old_log_file = os.path.join(self.old_project_path, self.accounts[account_name])
        
        if not os.path.exists(old_log_file):
            print(f"❌ 未找到原项目的日志文件: {old_log_file}")
            return {"imported": 0, "skipped": 0}
        
        # 读取原项目的shortcode列表
        with open(old_log_file, 'r', encoding='utf-8') as f:
            old_shortcodes = [line.strip() for line in f if line.strip()]
        
        print(f"📄 从原项目找到 {len(old_shortcodes)} 个已下载的视频记录")
        
        # 初始化新项目的日志器
        logger = Logger(account_name)
        
        # 加载新项目现有记录
        existing_data = logger.load_download_log()
        existing_shortcodes = {d["shortcode"] for d in existing_data["downloads"]}
        
        print(f"📄 新项目中已有 {len(existing_shortcodes)} 个下载记录")
        
        # 导入记录
        imported_count = 0
        skipped_count = 0
        
        for shortcode in old_shortcodes:
            if shortcode in existing_shortcodes:
                skipped_count += 1
                continue
            
            # 添加历史记录
            download_record = {
                "shortcode": shortcode,
                "download_time": "2025-01-01T00:00:00",  # 历史记录的默认时间
                "status": "success",
                "file_path": f"原项目已下载",
                "error": "",
                "merged": True,  # 假设原项目的都已处理过
                "download_folder": f"原项目/{account_name}",
                "blogger_name": "unknown",
                "imported_from_old_project": True  # 标记为导入的记录
            }
            
            existing_data["downloads"].append(download_record)
            imported_count += 1
        
        # 保存更新后的记录
        logger.save_download_log(existing_data)
        
        return {
            "imported": imported_count,
            "skipped": skipped_count,
            "total_old": len(old_shortcodes),
            "total_new": len(existing_data["downloads"])
        }
    
    def import_all_accounts(self):
        """导入所有账号的记录"""
        print("🔄 开始导入原项目的下载记录...")
        print("=" * 50)
        
        total_imported = 0
        
        for account_name in self.accounts.keys():
            print(f"\n📱 处理账号: {account_name}")
            print("-" * 30)
            
            result = self.import_account_records(account_name)
            
            print(f"✅ 导入完成:")
            print(f"   新导入: {result['imported']} 个")
            print(f"   已存在: {result['skipped']} 个")
            print(f"   原项目总计: {result['total_old']} 个")
            print(f"   新项目总计: {result['total_new']} 个")
            
            total_imported += result['imported']
        
        print(f"\n🎉 全部导入完成！总共导入了 {total_imported} 个历史记录")
        print("\n💡 现在运行下载命令时，这些视频会被自动跳过，避免重复下载")

def main():
    """主函数"""
    importer = DownloadRecordImporter()
    
    print("⚠️  重要提示:")
    print("这个工具会将原项目的下载记录导入到新项目")
    print("导入后，这些视频在新项目中会被标记为'已下载'，避免重复下载")
    print()
    
    confirm = input("确认要导入吗？(y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ 导入已取消")
        return
    
    importer.import_all_accounts()

if __name__ == "__main__":
    main()
