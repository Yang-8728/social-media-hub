#!/usr/bin/env python3
"""快速预扫描测试"""

import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.logger import Logger

def quick_test():
    """快速测试记录检查功能"""
    logger = Logger("ai_vanvan")
    
    # 测试一些已知的shortcode
    test_codes = [
        "DMSpQtdt9F_",  # 应该是已下载
        "DNGwiSQRz0H",  # 应该是已下载  
        "FAKE_CODE_123"  # 应该是未下载
    ]
    
    print("🧪 测试已下载检查功能:")
    for code in test_codes:
        is_downloaded = logger.is_downloaded(code)
        status = "✅ 已下载" if is_downloaded else "❌ 未下载"
        print(f"  {code}: {status}")
    
    # 统计记录
    log_data = logger.load_download_log()
    total = len(log_data["downloads"])
    recent = len([d for d in log_data["downloads"] if "2025-08-25" in d.get("download_time", "")])
    
    print(f"\n📊 记录统计:")
    print(f"  总记录数: {total}")
    print(f"  昨天下载: {recent}")
    print(f"  历史记录: {total - recent}")

if __name__ == "__main__":
    quick_test()
