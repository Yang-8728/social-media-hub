"""
测试合并记录检查逻辑
"""
import os
import sys
sys.path.append('.')

from src.utils.video_merger import VideoMerger

# 初始化VideoMerger
merger = VideoMerger("ai_vanvan")

# 测试刚才的3个视频
test_videos = [
    "videos/downloads/ai_vanvan/2025-10-14/2025-10-13_17-51-15_UTC.mp4",
    "videos/downloads/ai_vanvan/2025-10-14/2025-10-13_00-02-09_UTC.mp4",
    "videos/downloads/ai_vanvan/2025-10-14/2025-10-12_23-07-00_UTC.mp4"
]

print("检查这3个视频的合并状态：\n")

for video in test_videos:
    video_abs = os.path.abspath(video)
    is_merged = merger.is_video_merged(video_abs)
    status = "✅ 已合并" if is_merged else "❌ 未合并"
    print(f"{status}: {os.path.basename(video)}")

# 统计今天所有视频的合并状态
print("\n" + "="*60)
print("统计今天所有视频的合并状态：\n")

from datetime import datetime
import glob

today = datetime.now().strftime("%Y-%m-%d")
today_path = f"videos/downloads/ai_vanvan/{today}"

if os.path.exists(today_path):
    all_videos = glob.glob(os.path.join(today_path, "*.mp4"))
    
    merged_count = 0
    unmerged_count = 0
    
    for video in all_videos:
        if merger.is_video_merged(video):
            merged_count += 1
        else:
            unmerged_count += 1
    
    print(f"今天总视频数: {len(all_videos)}")
    print(f"已合并: {merged_count}")
    print(f"未合并: {unmerged_count}")
else:
    print(f"目录不存在: {today_path}")
