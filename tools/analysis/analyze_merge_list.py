#!/usr/bin/env python3
"""
分析合并脚本会处理哪些视频
"""

from pathlib import Path

def analyze_merge_list():
    """分析将要合并的视频列表"""
    video_dir = Path('videos/downloads/ai_vanvan/2025-09-01')
    
    # 获取所有mp4文件并排序
    all_videos = list(video_dir.glob('*.mp4'))
    all_videos.sort()
    
    print("=" * 80)
    print("合并脚本视频分析")
    print("=" * 80)
    
    print(f"总共发现: {len(all_videos)} 个视频文件\n")
    
    # 排除规则
    excluded_patterns = ['_std.mp4', '_fixed.mp4', '_normalized.mp4', '_aac_fixed.mp4']
    excluded_videos = ['2025-08-20_15-43-46_UTC.mp4']
    
    # 根据之前的分析，音频比特率<50k的问题视频
    problem_videos = [
        '2025-04-06_20-06-00_UTC.mp4',      # 44,500 bps
        '2025-05-12_04-45-50_UTC.mp4',      # 37,674 bps
        '2025-06-11_18-34-31_UTC.mp4',      # 43,936 bps
        '2025-06-29_18-58-32_UTC.mp4',      # 37,579 bps
        '2025-08-20_15-43-46_UTC.mp4'       # 41,113 bps (已排除)
    ]
    
    # 分类视频
    will_merge = []
    excluded_by_pattern = []
    excluded_by_name = []
    
    for video in all_videos:
        # 检查是否匹配排除模式
        if any(pattern in video.name for pattern in excluded_patterns):
            excluded_by_pattern.append(video.name)
            continue
        # 检查是否是被排除的具体视频
        if video.name in excluded_videos:
            excluded_by_name.append(video.name)
            continue
        will_merge.append(video.name)
    
    print(f"📹 将要合并的视频: {len(will_merge)} 个")
    print("-" * 50)
    for i, name in enumerate(will_merge, 1):
        status = "⚠️ 有潜在问题" if name in problem_videos else "✅ 正常"
        print(f"  {i:2d}. {name} {status}")
    
    print(f"\n🚫 按模式排除的视频: {len(excluded_by_pattern)} 个")
    print("-" * 50)
    for name in excluded_by_pattern:
        print(f"     {name}")
    
    print(f"\n🚫 按名称排除的视频: {len(excluded_by_name)} 个")
    print("-" * 50)
    for name in excluded_by_name:
        print(f"     {name}")
    
    # 分析问题视频
    problem_in_merge = [name for name in will_merge if name in problem_videos]
    
    print(f"\n⚠️  合并列表中包含的问题视频: {len(problem_in_merge)} 个")
    print("-" * 50)
    if problem_in_merge:
        for name in problem_in_merge:
            print(f"     {name} (音频比特率 < 50kbps)")
    else:
        print("     无问题视频")
    
    print(f"\n📊 总结:")
    print(f"   - 总视频数: {len(all_videos)}")
    print(f"   - 将合并: {len(will_merge)} 个")
    print(f"   - 其中有问题: {len(problem_in_merge)} 个")
    print(f"   - 排除的: {len(excluded_by_pattern) + len(excluded_by_name)} 个")
    
    if problem_in_merge:
        print(f"\n❌ 警告: 合并列表包含 {len(problem_in_merge)} 个低音质视频!")
        print("   这可能会影响最终合并视频的质量。")
    else:
        print(f"\n✅ 良好: 合并列表不包含已知的问题视频。")

if __name__ == "__main__":
    analyze_merge_list()
