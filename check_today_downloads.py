import os
import glob

# 查找所有2025-10-30相关的目录
paths = glob.glob('videos/downloads/**/2025-10-30*', recursive=True)
paths = [p for p in paths if os.path.isdir(p)]

print("=" * 60)
print("📊 今天(2025-10-30)下载的视频")
print("=" * 60)

total_videos = 0
for path in sorted(paths):
    mp4s = [f for f in os.listdir(path) if f.endswith('.mp4')]
    total_videos += len(mp4s)
    
    print(f"\n📁 {path}:")
    print(f"   视频数: {len(mp4s)}")
    for mp4 in mp4s:
        print(f"   - {mp4}")

print("\n" + "=" * 60)
print(f"✅ 总计: {total_videos} 个视频")
print("=" * 60)
