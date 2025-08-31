"""
临时脚本：测试同步功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.logger import Logger

def test_sync():
    print("🔍 开始测试 ai_vanvan 的同步功能...")
    
    # 创建logger实例
    logger = Logger("ai_vanvan")
    
    # 先显示当前下载记录统计
    print(f"📊 当前状态: {logger.get_download_summary()}")
    
    # 执行完整同步
    print("\n🔄 执行完整同步...")
    sync_count = logger.sync_missing_downloads(force_full_scan=True)
    
    # 显示同步后的统计
    print(f"📊 同步后状态: {logger.get_download_summary()}")
    
    if sync_count > 0:
        print(f"✅ 成功同步了 {sync_count} 条缺失记录！")
    else:
        print("✅ 所有记录都已同步，无需补充")

if __name__ == "__main__":
    test_sync()
