#!/usr/bin/env python3
"""测试下载记录功能"""

import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.logger import Logger

def test_record_function():
    """测试记录功能"""
    logger = Logger("ai_vanvan")
    
    # 读取当前记录数量
    log_data = logger.load_download_log()
    initial_count = len(log_data["downloads"])
    print(f"初始记录数量: {initial_count}")
    
    # 测试添加一条记录
    test_shortcode = "TEST_123_456"
    logger.record_download(
        shortcode=test_shortcode,
        status="success",
        file_path="test_path",
        folder="test_folder",
        blogger="test_blogger"
    )
    
    # 检查是否保存成功
    log_data_after = logger.load_download_log()
    final_count = len(log_data_after["downloads"])
    print(f"添加后记录数量: {final_count}")
    
    # 查找测试记录
    test_record = next((d for d in log_data_after["downloads"] if d["shortcode"] == test_shortcode), None)
    if test_record:
        print(f"✅ 测试记录保存成功: {test_record}")
        
        # 清理测试记录
        log_data_after["downloads"] = [d for d in log_data_after["downloads"] if d["shortcode"] != test_shortcode]
        logger.save_download_log(log_data_after)
        print("🧹 测试记录已清理")
    else:
        print("❌ 测试记录保存失败")

if __name__ == "__main__":
    test_record_function()
