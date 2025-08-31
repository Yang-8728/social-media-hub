"""
检查最近下载视频的分辨率分布
分析ai_vanvan账号最近几天的视频质量
"""
import os
import sys
from pathlib import Path
from collections import defaultdict, Counter

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.video_merger import VideoMerger

def analyze_recent_video_resolutions():
    """分析最近下载视频的分辨率"""
    account_name = "ai_vanvan"
    
    print(f"🔍 分析 {account_name} 最近下载视频的分辨率分布")
    print("=" * 60)
    
    # 获取downloads目录
    downloads_base = Path(f"videos/downloads/{account_name}")
    
    if not downloads_base.exists():
        print(f"❌ 下载目录不存在: {downloads_base}")
        return
    
    # 获取所有日期文件夹
    date_folders = [d for d in downloads_base.iterdir() if d.is_dir()]
    date_folders.sort(reverse=True)  # 最新的在前
    
    print(f"📁 找到 {len(date_folders)} 个日期文件夹")
    
    # 创建VideoMerger来获取分辨率
    merger = VideoMerger()
    
    # 统计数据
    resolution_stats = Counter()
    resolution_by_date = defaultdict(list)
    quality_categories = {
        "1080p+": 0,    # 1080p或更高
        "720p": 0,      # 720p
        "低于720p": 0,   # 低于720p
        "其他": 0       # 奇怪分辨率
    }
    
    total_videos = 0
    total_size_mb = 0
    
    print(f"\n📊 按日期分析:")
    print("-" * 50)
    
    # 分析最近的日期文件夹
    for date_folder in date_folders[:10]:  # 检查最近10天
        video_files = list(date_folder.glob("*.mp4"))
        
        if not video_files:
            continue
            
        print(f"\n📅 {date_folder.name} ({len(video_files)} 个视频):")
        
        date_resolutions = []
        date_size = 0
        
        for video_file in video_files:
            width, height = merger.get_video_resolution(str(video_file))
            size_mb = video_file.stat().st_size / (1024*1024)
            
            if width and height:
                resolution_key = f"{width}x{height}"
                resolution_stats[resolution_key] += 1
                resolution_by_date[date_folder.name].append({
                    'file': video_file.name,
                    'width': width,
                    'height': height,
                    'size_mb': size_mb
                })
                
                # 分类统计
                pixel_count = width * height
                if pixel_count >= 1920 * 1080:  # 1080p或更高
                    quality_categories["1080p+"] += 1
                    quality_desc = "1080p+"
                elif pixel_count >= 1280 * 720:  # 720p
                    quality_categories["720p"] += 1
                    quality_desc = "720p"
                elif pixel_count >= 720 * 720:  # 接近720p
                    quality_categories["低于720p"] += 1
                    quality_desc = "中等"
                else:
                    quality_categories["其他"] += 1
                    quality_desc = "低"
                
                aspect_ratio = width / height
                orientation = "竖屏" if aspect_ratio < 1 else "横屏"
                
                print(f"  {video_file.name[:30]:<30} | {width:4d}x{height:<4d} | {quality_desc:<6s} | {orientation} | {size_mb:.1f}MB")
                
                date_size += size_mb
                total_videos += 1
                total_size_mb += size_mb
        
        print(f"  📊 小计: {len(video_files)} 个视频, {date_size:.1f}MB")
    
    print(f"\n" + "=" * 60)
    print(f"📈 总体统计 (最近{len([d for d in date_folders[:10] if list(d.glob('*.mp4'))])}天)")
    print("=" * 60)
    
    print(f"📁 总视频数: {total_videos} 个")
    print(f"📊 总大小: {total_size_mb:.1f}MB")
    print(f"📱 平均大小: {total_size_mb/total_videos:.1f}MB/视频" if total_videos > 0 else "")
    
    print(f"\n🎯 分辨率分布:")
    print("-" * 30)
    for resolution, count in resolution_stats.most_common():
        percentage = (count / total_videos) * 100 if total_videos > 0 else 0
        print(f"  {resolution:<12} | {count:3d} 个 ({percentage:5.1f}%)")
    
    print(f"\n📊 质量等级分布:")
    print("-" * 30)
    for category, count in quality_categories.items():
        percentage = (count / total_videos) * 100 if total_videos > 0 else 0
        print(f"  {category:<8} | {count:3d} 个 ({percentage:5.1f}%)")
    
    # 分析结论
    print(f"\n💡 分析结论:")
    print("-" * 30)
    
    if quality_categories["1080p+"] > quality_categories["720p"]:
        print("✅ 主要是1080p+视频，建议使用高质量合并模式")
        print("🎯 推荐目标分辨率: 保持最高分辨率(可能1080x1920)")
    elif quality_categories["720p"] > quality_categories["1080p+"]:
        print("📱 主要是720p视频，720p合并模式适合")
        print("🎯 推荐目标分辨率: 720x1280")
    else:
        print("🔄 混合质量视频，建议智能选择最高分辨率")
        print("🎯 推荐目标分辨率: 动态选择")
    
    # 推荐合并策略
    print(f"\n🚀 合并策略推荐:")
    print("-" * 30)
    
    most_common_resolution = resolution_stats.most_common(1)[0] if resolution_stats else None
    if most_common_resolution:
        res, count = most_common_resolution
        print(f"📍 最常见分辨率: {res} ({count}个视频)")
        
        # 解析分辨率
        try:
            w, h = map(int, res.split('x'))
            if h >= 1920:
                print("💎 建议: 使用1080p+高质量合并，保持清晰度")
            elif h >= 1280:
                print("📱 建议: 使用720p标准合并即可")
            else:
                print("🔧 建议: 使用适配性合并，添加黑边")
        except:
            pass

if __name__ == "__main__":
    analyze_recent_video_resolutions()
