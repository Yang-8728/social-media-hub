"""
检查合并记录情况
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.logger import Logger

def check_merge_sessions():
    print("🔍 检查 ai_vanvan 的合并记录...")
    
    logger = Logger("ai_vanvan")
    log_data = logger.load_download_log()
    
    merge_sessions = log_data.get("merged_sessions", [])
    print(f"📊 总共有 {len(merge_sessions)} 个合并会话")
    
    if len(merge_sessions) > 0:
        print(f"\n📅 最近的合并记录:")
        # 显示最近10个合并会话
        for i, session in enumerate(merge_sessions[-10:]):
            merge_time = session.get("merge_time", "unknown")
            
            if "shortcodes" in session:
                # 批量合并
                count = session.get("video_count", len(session.get("shortcodes", [])))
                merged_file = session.get("merged_file", "unknown")
                print(f"  {i+1}. {merge_time[:16]} - 批量合并 {count} 个视频")
                print(f"     -> {merged_file}")
            else:
                # 单个合并
                shortcode = session.get("shortcode", "unknown")
                merged_file = session.get("merged_file", "unknown")
                print(f"  {i+1}. {merge_time[:16]} - 单个合并 {shortcode}")
                print(f"     -> {merged_file}")
    else:
        print("❌ 没有找到任何合并记录")
    
    # 检查最近几天是否有合并
    from datetime import datetime, timedelta
    recent_merges = []
    three_days_ago = datetime.now() - timedelta(days=3)
    
    for session in merge_sessions:
        try:
            merge_time = datetime.fromisoformat(session["merge_time"])
            if merge_time >= three_days_ago:
                recent_merges.append(session)
        except:
            continue
    
    print(f"\n📈 最近3天的合并:")
    print(f"  - 合并会话: {len(recent_merges)} 个")
    
    total_merged_videos = 0
    for session in recent_merges:
        if "shortcodes" in session:
            total_merged_videos += session.get("video_count", len(session.get("shortcodes", [])))
        else:
            total_merged_videos += 1
    
    print(f"  - 已合并视频: {total_merged_videos} 个")
    print(f"  - 待合并视频: 73 个")
    print(f"  - 是否匹配: {'✅' if total_merged_videos < 73 else '❓'}")

if __name__ == "__main__":
    check_merge_sessions()
