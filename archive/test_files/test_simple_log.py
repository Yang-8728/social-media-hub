#!/usr/bin/env python3
"""
测试简化后的下载日志显示
"""
import time
import sys

def test_simplified_progress():
    """模拟简化后的下载进度显示"""
    
    print("🚀 ai_vanvan")
    print("📥 发现 3 个新视频")
    
    total = 3
    for i in range(1, total + 1):
        progress = (i / total) * 100
        progress_bar = "█" * int(progress // 10) + "░" * (10 - int(progress // 10))
        
        # 简洁显示：进度数字 + 一个进度条
        print(f"\r📥 {i}/{total} [{progress_bar}] {progress:.0f}%", end="", flush=True)
        time.sleep(1)
    
    print()  # 换行
    print("✅ 完成: 3个")
    
    print("\n" + "="*50)
    print("对比之前复杂的显示:")
    print("❌ 旧版: 📥 下载中: 2/3 ✅2 ⏭️0 [████████████████░░░░] 1分23秒")
    print("✅ 新版: 📥 2/3 [████████░░] 67%")
    print("="*50)

if __name__ == "__main__":
    test_simplified_progress()
