#!/usr/bin/env python3
"""
对比之前和现在的问题视频列表
"""

print("🔍 问题视频列表对比")
print("=" * 60)

print("📋 之前检测出的5个问题视频:")
old_problem_videos = [
    "2025-08-19_09-56-05_UTC.mp4",
    "2025-08-19_10-05-11_UTC.mp4", 
    "2025-08-19_15-35-12_UTC.mp4",
    "2025-08-20_15-43-46_UTC.mp4",
    "2025-08-21_14-52-42_UTC.mp4"
]

for i, video in enumerate(old_problem_videos, 1):
    print(f"  {i}. {video}")

print("\n📋 现在扫描出的5个问题视频:")
new_problem_videos = [
    "2025-04-06_20-06-00_UTC.mp4",  # 44kbps
    "2025-05-12_04-45-50_UTC.mp4",  # 38kbps
    "2025-06-11_18-34-31_UTC.mp4",  # 44kbps (1:39卡顿的那个)
    "2025-06-29_18-58-32_UTC.mp4",  # 38kbps
    "2025-08-20_15-43-46_UTC.mp4"   # 41kbps
]

for i, video in enumerate(new_problem_videos, 1):
    print(f"  {i}. {video}")

print("\n🔍 对比分析:")

# 找出相同的
same_videos = set(old_problem_videos) & set(new_problem_videos)
print(f"\n✅ 相同的问题视频 ({len(same_videos)}个):")
for video in same_videos:
    print(f"  - {video}")

# 找出之前有现在没有的（可能被删除了）
removed_videos = set(old_problem_videos) - set(new_problem_videos)
print(f"\n🗑️ 之前有现在没有的 ({len(removed_videos)}个) - 可能被删除:")
for video in removed_videos:
    print(f"  - {video}")

# 找出现在有之前没有的（新发现的）
new_found_videos = set(new_problem_videos) - set(old_problem_videos)
print(f"\n🆕 新发现的问题视频 ({len(new_found_videos)}个):")
for video in new_found_videos:
    print(f"  - {video}")

print(f"\n💡 结论:")
print(f"  - 之前检测出5个问题视频")
print(f"  - 删除了{len(removed_videos)}个问题视频")
print(f"  - 新发现了{len(new_found_videos)}个问题视频")
print(f"  - 现在仍然是5个问题视频")
print(f"  - 说明删除的数量 = 新发现的数量")

if len(removed_videos) == len(new_found_videos):
    print(f"\n🎯 这解释了为什么数量没变！")
    print(f"   你删除了一些有问题的视频，但同时发现了其他问题视频")
else:
    print(f"\n❓ 数量变化不匹配，可能有其他原因")
