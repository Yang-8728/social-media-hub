import os
import glob
from datetime import datetime, timedelta

# 获取所有mp4文件
files = glob.glob('videos/downloads/**/*.mp4', recursive=True)

# 统计最近3天
today = datetime.now().date()
stats = {}

for f in files:
    mtime = datetime.fromtimestamp(os.path.getmtime(f)).date()
    date_str = mtime.isoformat()
    stats[date_str] = stats.get(date_str, 0) + 1

print("=" * 60)
print("📊 最近3天下载统计")
print("=" * 60)

# 显示最近3天
for i in range(3):
    date = (today - timedelta(days=i)).isoformat()
    count = stats.get(date, 0)
    day_name = ["今天", "昨天", "前天"][i]
    print(f"{day_name} ({date}): {count} 个视频")

print("=" * 60)
print(f"总计: {sum(stats.get((today - timedelta(days=i)).isoformat(), 0) for i in range(3))} 个视频")
print("=" * 60)

# 显示所有日期的统计（最近7天）
print("\n📅 详细统计（最近7天）:")
for date, count in sorted(stats.items(), reverse=True)[:7]:
    print(f"  {date}: {count} 个视频")
