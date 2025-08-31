"""
检查待合并视频的详细信息
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.logger import Logger
from datetime import datetime

def check_unmerged_videos():
    print("🔍 检查 ai_vanvan 的待合并视频...")
    
    logger = Logger("ai_vanvan")
    log_data = logger.load_download_log()
    
    # 获取所有待合并的视频
    unmerged_videos = [d for d in log_data["downloads"] 
                      if d["status"] == "success" and not d.get("merged", False)]
    
    print(f"📊 总共有 {len(unmerged_videos)} 个待合并视频")
    
    # 按日期分组
    date_groups = {}
    for video in unmerged_videos:
        download_time = video.get("download_time", "")
        try:
            # 提取日期部分
            date_str = download_time.split("T")[0] if "T" in download_time else download_time[:10]
            if date_str not in date_groups:
                date_groups[date_str] = []
            date_groups[date_str].append(video)
        except:
            if "unknown" not in date_groups:
                date_groups["unknown"] = []
            date_groups["unknown"].append(video)
    
    # 按日期排序显示
    sorted_dates = sorted(date_groups.keys(), reverse=True)
    
    print(f"\n📅 待合并视频按日期分布:")
    for date_str in sorted_dates[:10]:  # 只显示最近10天
        videos = date_groups[date_str]
        print(f"  {date_str}: {len(videos)} 个")
        
        # 显示前几个视频的详细信息
        for video in videos[:3]:
            shortcode = video.get("shortcode", "unknown")
            blogger = video.get("blogger_name", "unknown")
            sync_added = video.get("sync_added", False)
            sync_flag = " [同步添加]" if sync_added else ""
            print(f"    - {shortcode} ({blogger}){sync_flag}")
        
        if len(videos) > 3:
            print(f"    ... 还有 {len(videos) - 3} 个")
    
    # 统计最近几天的
    recent_count = 0
    for date_str in sorted_dates:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            days_ago = (datetime.now() - date_obj).days
            if days_ago <= 7:  # 最近7天
                recent_count += len(date_groups[date_str])
        except:
            continue
    
    print(f"\n📈 统计:")
    print(f"  - 最近7天待合并: {recent_count} 个")
    print(f"  - 总待合并: {len(unmerged_videos)} 个")
    
    # 检查是否有很多同步添加的
    sync_added_count = sum(1 for v in unmerged_videos if v.get("sync_added", False))
    print(f"  - 其中同步添加的: {sync_added_count} 个")

if __name__ == "__main__":
    check_unmerged_videos()
