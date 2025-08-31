import os
from datetime import datetime

# 检查下载文件夹中的视频
download_folder = 'videos/downloads/ai_vanvan/2025-08-27'
merged_folder = 'videos/merged/ai_vanvan'

print('=== 2025-08-27 文件夹视频统计 ===')

if os.path.exists(download_folder):
    all_files = os.listdir(download_folder)
    mp4_files = [f for f in all_files if f.endswith('.mp4')]
    
    print(f'📁 下载文件夹: {download_folder}')
    print(f'📊 总文件数: {len(all_files)}')
    print(f'🎬 MP4视频数: {len(mp4_files)}')
    print()
    
    # 按时间排序显示视频
    mp4_files.sort()
    print('📹 所有视频文件:')
    for i, video in enumerate(mp4_files, 1):
        # 提取日期时间
        date_part = video.split('_')[0:3]  # 2025-08-27_xx-xx-xx
        date_str = '_'.join(date_part)
        print(f'  {i:2d}. {video}')
        print(f'      📅 {date_str}')
    
    print()
else:
    print(f'❌ 文件夹不存在: {download_folder}')

# 检查已合并的视频
print('=== 已合并视频检查 ===')
if os.path.exists(merged_folder):
    merged_files = [f for f in os.listdir(merged_folder) if f.endswith('.mp4')]
    print(f'📁 合并文件夹: {merged_folder}')
    print(f'🎬 已合并视频数: {len(merged_files)}')
    
    if merged_files:
        print('📹 已合并的视频:')
        for video in sorted(merged_files):
            file_path = os.path.join(merged_folder, video)
            size_mb = os.path.getsize(file_path) / (1024*1024)
            print(f'  - {video} ({size_mb:.1f}MB)')
    print()
else:
    print(f'❌ 合并文件夹不存在: {merged_folder}')

print('💡 准备合并新视频!')
