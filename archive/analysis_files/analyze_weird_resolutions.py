"""
分析奇怪分辨率视频的黑边处理能力
检查非标准分辨率视频是否能正确添加黑边
"""
import os
import sys
from pathlib import Path
from collections import Counter
import math

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.video_merger import VideoMerger

def analyze_weird_resolutions():
    """分析奇怪分辨率视频的处理情况"""
    account_name = "ai_vanvan"
    
    print(f"🔍 分析奇怪分辨率视频的黑边处理能力")
    print("=" * 60)
    
    # 获取downloads目录
    downloads_base = Path(f"videos/downloads/{account_name}")
    
    # 标准分辨率定义
    standard_resolutions = {
        '720x1280',    # 标准竖屏720p
        '1080x1920',   # 标准竖屏1080p
        '1280x720',    # 标准横屏720p
        '1920x1080',   # 标准横屏1080p
        '720x720',     # 标准正方形
        '1080x1080',   # 1080p正方形
    }
    
    # 目标分辨率
    target_width, target_height = 720, 1280
    
    print(f"🎯 目标分辨率: {target_width}x{target_height}")
    print(f"📐 标准分辨率: {', '.join(standard_resolutions)}")
    print()
    
    # 创建VideoMerger
    merger = VideoMerger()
    
    # 收集所有视频文件
    all_videos = []
    for date_folder in downloads_base.iterdir():
        if date_folder.is_dir():
            for video_file in date_folder.glob("*.mp4"):
                all_videos.append(video_file)
    
    print(f"📁 总共找到 {len(all_videos)} 个视频文件")
    
    # 分析分辨率
    resolution_analysis = {
        'standard': [],      # 标准分辨率
        'weird_portrait': [],  # 奇怪竖屏
        'weird_landscape': [], # 奇怪横屏
        'weird_square': [],    # 奇怪正方形
        'very_weird': []       # 非常奇怪的比例
    }
    
    print(f"\n📊 分辨率分析:")
    print("-" * 50)
    
    for video_file in all_videos:
        width, height = merger.get_video_resolution(str(video_file))
        
        if not width or not height:
            continue
            
        resolution_key = f"{width}x{height}"
        aspect_ratio = width / height
        
        # 分类
        if resolution_key in standard_resolutions:
            category = 'standard'
            category_desc = "标准"
        elif abs(aspect_ratio - 1.0) < 0.05:  # 正方形
            category = 'weird_square'
            category_desc = "奇怪正方形"
        elif aspect_ratio < 0.8:  # 竖屏
            category = 'weird_portrait'
            category_desc = "奇怪竖屏"
        elif aspect_ratio > 1.2:  # 横屏
            category = 'weird_landscape'
            category_desc = "奇怪横屏"
        else:  # 非常奇怪的比例
            category = 'very_weird'
            category_desc = "超奇怪"
        
        # 计算黑边效果
        scale_w = target_width / width
        scale_h = target_height / height
        scale = min(scale_w, scale_h)  # 保持比例的缩放系数
        
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        pad_x = (target_width - new_width) // 2
        pad_y = (target_height - new_height) // 2
        
        # 计算填充比例
        content_area = new_width * new_height
        total_area = target_width * target_height
        content_ratio = content_area / total_area
        
        video_info = {
            'file': video_file.name,
            'original': f"{width}x{height}",
            'aspect_ratio': aspect_ratio,
            'scaled': f"{new_width}x{new_height}",
            'padding': f"({pad_x},{pad_y})",
            'content_ratio': content_ratio,
            'date': video_file.parent.name
        }
        
        resolution_analysis[category].append(video_info)
    
    # 打印分析结果
    print(f"📈 分类统计:")
    for category, videos in resolution_analysis.items():
        count = len(videos)
        total = len(all_videos)
        percentage = (count / total) * 100 if total > 0 else 0
        
        category_names = {
            'standard': '标准分辨率',
            'weird_portrait': '奇怪竖屏',
            'weird_landscape': '奇怪横屏', 
            'weird_square': '奇怪正方形',
            'very_weird': '超奇怪比例'
        }
        
        print(f"  {category_names[category]:<10}: {count:3d} 个 ({percentage:5.1f}%)")
    
    # 详细分析奇怪分辨率
    print(f"\n🔍 奇怪分辨率详细分析:")
    print("=" * 80)
    
    weird_categories = ['weird_portrait', 'weird_landscape', 'weird_square', 'very_weird']
    
    for category in weird_categories:
        videos = resolution_analysis[category]
        if not videos:
            continue
            
        category_names = {
            'weird_portrait': '🔸 奇怪竖屏分辨率',
            'weird_landscape': '🔹 奇怪横屏分辨率',
            'weird_square': '🔶 奇怪正方形分辨率',
            'very_weird': '🔴 超奇怪比例分辨率'
        }
        
        print(f"\n{category_names[category]} ({len(videos)} 个):")
        print("-" * 70)
        
        # 按分辨率分组
        resolution_groups = {}
        for video in videos:
            res = video['original']
            if res not in resolution_groups:
                resolution_groups[res] = []
            resolution_groups[res].append(video)
        
        for resolution, group_videos in resolution_groups.items():
            sample = group_videos[0]  # 取一个样本
            
            print(f"  📐 {resolution:<12} | 比例:{sample['aspect_ratio']:5.2f} | "
                  f"缩放到:{sample['scaled']:<12} | 黑边:{sample['padding']:<10} | "
                  f"内容占比:{sample['content_ratio']*100:4.1f}% | {len(group_videos)}个视频")
            
            # 显示几个示例文件
            for i, video in enumerate(group_videos[:3]):
                print(f"    └─ {video['date']}/{video['file'][:40]}")
            if len(group_videos) > 3:
                print(f"    └─ ... 还有 {len(group_videos)-3} 个")
    
    # 黑边处理能力评估
    print(f"\n🎯 黑边处理能力评估:")
    print("=" * 50)
    
    all_weird = []
    for category in weird_categories:
        all_weird.extend(resolution_analysis[category])
    
    if all_weird:
        # 计算统计数据
        content_ratios = [v['content_ratio'] for v in all_weird]
        min_ratio = min(content_ratios)
        max_ratio = max(content_ratios)
        avg_ratio = sum(content_ratios) / len(content_ratios)
        
        print(f"📊 内容占比统计:")
        print(f"  最小内容占比: {min_ratio*100:.1f}% (黑边最多)")
        print(f"  最大内容占比: {max_ratio*100:.1f}% (黑边最少)")
        print(f"  平均内容占比: {avg_ratio*100:.1f}%")
        
        # 评估处理效果
        print(f"\n✅ 黑边处理结论:")
        
        very_low_content = sum(1 for r in content_ratios if r < 0.5)
        low_content = sum(1 for r in content_ratios if 0.5 <= r < 0.7)
        good_content = sum(1 for r in content_ratios if 0.7 <= r < 0.9)
        excellent_content = sum(1 for r in content_ratios if r >= 0.9)
        
        print(f"  🔴 内容占比 <50% (黑边过多): {very_low_content} 个")
        print(f"  🟡 内容占比 50-70% (黑边较多): {low_content} 个") 
        print(f"  🟢 内容占比 70-90% (黑边适中): {good_content} 个")
        print(f"  🟢 内容占比 >90% (黑边很少): {excellent_content} 个")
        
        if very_low_content == 0:
            print(f"\n🎉 所有奇怪分辨率都能很好地处理!")
        elif very_low_content < len(all_weird) * 0.1:
            print(f"\n✅ 绝大部分奇怪分辨率都能很好地处理!")
        else:
            print(f"\n⚠️  部分视频黑边较多，但仍可正常处理")
    else:
        print("✅ 没有发现奇怪分辨率视频")
    
    # 推荐策略
    total_weird = len(all_weird)
    total_videos = len(all_videos)
    weird_percentage = (total_weird / total_videos) * 100 if total_videos > 0 else 0
    
    print(f"\n🚀 处理策略推荐:")
    print("=" * 50)
    print(f"📊 奇怪分辨率比例: {total_weird}/{total_videos} ({weird_percentage:.1f}%)")
    
    if weird_percentage < 10:
        print("✅ 奇怪分辨率很少，黑边处理完全可行")
    elif weird_percentage < 30:
        print("✅ 奇怪分辨率适中，黑边处理效果良好")
    else:
        print("⚠️  奇怪分辨率较多，需要重点测试黑边效果")
    
    print(f"\n💡 建议:")
    print("  ✅ 固定720x1280目标分辨率")
    print("  ✅ 使用FFmpeg自动黑边填充") 
    print("  ✅ 保持原视频长宽比不变形")
    print("  ✅ 适用于所有检测到的奇怪分辨率")

if __name__ == "__main__":
    analyze_weird_resolutions()
