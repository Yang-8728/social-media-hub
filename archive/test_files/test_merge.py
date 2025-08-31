#!/usr/bin/env python3
"""测试合并功能"""

import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.logger import Logger

def test_unmerged_list():
    """测试未合并视频列表"""
    logger = Logger("ai_vanvan")
    unmerged = logger.get_unmerged_downloads()
    
    print(f"📊 未合并的视频: {len(unmerged)} 个")
    print("\n🕒 按下载时间排序（最新在前）:")
    
    for i, shortcode in enumerate(unmerged[:10], 1):  # 只显示前10个
        print(f"  {i}. {shortcode}")
    
    if len(unmerged) > 10:
        print(f"  ... 还有 {len(unmerged) - 10} 个")
    
    print(f"\n💡 使用方法:")
    print(f"  合并所有: python main.py --merge --ai_vanvan")
    print(f"  合并最新30个: python main.py --merge --ai_vanvan --merge-limit 30")
    print(f"  合并最新10个: python main.py --merge --ai_vanvan --merge-limit 10")

if __name__ == "__main__":
    test_unmerged_list()
