#!/usr/bin/env python3
"""
批量标记所有未合并视频为已合并 - 自动版本
"""
import os
import sys
import json
from datetime import datetime

# 添加src目录到路径
sys.path.append('src')

try:
    from utils.logger import Logger
except ImportError:
    from src.utils.logger import Logger

def auto_mark_all_merged():
    """自动标记ai_vanvan账号的所有未合并视频为已合并"""
    
    print("🚀 开始批量标记未合并视频...")
    
    # 初始化logger
    logger = Logger("ai_vanvan")
    
    # 获取未合并的视频列表
    unmerged_shortcodes = logger.get_unmerged_downloads()
    
    if not unmerged_shortcodes:
        print("✅ 没有未合并的视频")
        return
    
    print(f"📋 发现 {len(unmerged_shortcodes)} 个未合并视频")
    
    # 显示前5个shortcode作为预览
    print(f"\n📝 未合并视频预览:")
    for i, shortcode in enumerate(unmerged_shortcodes[:5]):
        print(f"   {i+1}. {shortcode}")
    
    if len(unmerged_shortcodes) > 5:
        print(f"   ... 及其他 {len(unmerged_shortcodes) - 5} 个")
    
    print(f"\n✅ 开始标记所有 {len(unmerged_shortcodes)} 个视频为已合并...")
    
    # 批量标记为已合并
    merged_file_path = "batch_marked_as_merged_" + datetime.now().strftime("%Y%m%d")
    logger.mark_batch_as_merged(unmerged_shortcodes, merged_file_path)
    
    print(f"🎉 成功标记 {len(unmerged_shortcodes)} 个视频为已合并!")
    
    # 验证结果
    remaining_unmerged = logger.get_unmerged_downloads()
    print(f"📊 剩余未合并视频: {len(remaining_unmerged)} 个")
    
    if len(remaining_unmerged) == 0:
        print("🎊 所有视频都已标记为合并状态!")
    
    # 显示最新统计
    summary = logger.get_download_summary()
    print(f"\n📈 更新后的统计:")
    print(f"   总下载: {summary['total']} 个")
    print(f"   成功: {summary['success']} 个") 
    print(f"   已合并: {summary['merged']} 个")
    print(f"   待合并: {summary['unmerged']} 个")

if __name__ == "__main__":
    auto_mark_all_merged()
