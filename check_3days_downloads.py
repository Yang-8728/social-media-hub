import os
import glob
from datetime import datetime, timedelta

# 统计最近3天
today = datetime.now().date()
dates_to_check = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(3)]
date_names = ['今天', '昨天', '前天']

print("=" * 60)
print("📊 最近3天下载统计")
print("=" * 60)

total_all = 0
for i, date in enumerate(dates_to_check):
    # 查找这一天的所有目录
    paths = glob.glob(f'videos/downloads/**/{date}*', recursive=True)
    paths = [p for p in paths if os.path.isdir(p)]
    
    # 统计视频数
    total_videos = 0
    for path in paths:
        mp4s = [f for f in os.listdir(path) if f.endswith('.mp4')]
        total_videos += len(mp4s)
    
    total_all += total_videos
    print(f"{date_names[i]} ({date}): {total_videos} 个视频")

print("=" * 60)
print(f"✅ 三天总计: {total_all} 个视频")
print("=" * 60)
