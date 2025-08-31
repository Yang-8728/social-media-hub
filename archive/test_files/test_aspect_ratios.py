"""
测试各种视频比例的黑边处理
演示如何处理正方形、横屏、竖屏、奇怪比例的视频
"""
import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.video_merger import VideoMerger

def test_aspect_ratio_handling():
    """测试不同比例视频的处理逻辑"""
    
    print("🧪 测试视频比例处理逻辑")
    print("=" * 50)
    
    # 模拟各种奇怪的视频分辨率
    test_cases = [
        # (宽, 高, 描述)
        (720, 1280, "标准竖屏 9:16"),
        (1080, 1080, "正方形 1:1"), 
        (1920, 1080, "标准横屏 16:9"),
        (640, 360, "小横屏 16:9"),
        (480, 854, "小竖屏 9:16"),
        (1200, 1200, "大正方形 1:1"),
        (1440, 1080, "奇怪比例 4:3"),
        (960, 720, "奇怪比例 4:3"),
        (320, 568, "超小竖屏"),
        (2560, 1440, "2K横屏"),
        (1080, 1350, "Instagram Story比例"),
        (1080, 1920, "抖音竖屏"),
        (800, 600, "4:3老比例"),
        (1366, 768, "笔记本屏幕比例"),
    ]
    
    print("📐 原始分辨率分析:")
    print("-" * 30)
    
    for width, height, desc in test_cases:
        aspect_ratio = width / height
        
        # 分类逻辑（与VideoMerger中的逻辑一致）
        if abs(aspect_ratio - 1.0) < 0.05:  # 接近1:1
            category = "正方形"
        elif aspect_ratio < 0.8:  # 明显竖屏
            category = "竖屏"
        elif aspect_ratio > 1.2:  # 明显横屏
            category = "横屏"
        else:  # 其他奇怪比例
            category = "特殊比例"
            
        print(f"  {width:4d}x{height:<4d} | {aspect_ratio:4.2f} | {category:8s} | {desc}")
    
    print(f"\n🎯 统一目标分辨率处理:")
    print("-" * 30)
    
    # 假设选择竖屏目标 720x1280
    target_w, target_h = 720, 1280
    print(f"目标分辨率: {target_w}x{target_h} (竖屏)")
    print(f"")
    
    print("各种原始分辨率 -> 黑边效果:")
    for width, height, desc in test_cases:
        # 计算缩放后的尺寸（保持比例）
        scale_w = target_w / width
        scale_h = target_h / height
        scale = min(scale_w, scale_h)  # 选择较小的缩放比例
        
        new_w = int(width * scale)
        new_h = int(height * scale)
        
        # 计算黑边
        pad_x = (target_w - new_w) // 2
        pad_y = (target_h - new_h) // 2
        
        print(f"  {width:4d}x{height:<4d} -> {new_w:3d}x{new_h:<4d} + 黑边({pad_x:3d},{pad_y:3d}) | {desc}")
    
    print(f"\n💡 关键点:")
    print("  ✅ 原视频内容完全保留，不变形")
    print("  ✅ 通过黑边填充到统一分辨率") 
    print("  ✅ 支持任意奇怪比例的视频")
    print("  ✅ FFmpeg自动计算最佳缩放和居中")

def test_real_videos():
    """测试真实视频文件的比例处理"""
    account_name = "ai_vanvan"
    target_date = "2025-08-27"
    
    target_folder = Path(f"videos/downloads/{account_name}/{target_date}")
    
    if not target_folder.exists():
        print(f"❌ 测试文件夹不存在: {target_folder}")
        return
    
    video_files = list(target_folder.glob("*.mp4"))
    if not video_files:
        print("❌ 没有找到测试视频文件")
        return
        
    print(f"\n🎬 真实视频文件分析:")
    print("=" * 50)
    
    # 创建VideoMerger来测试新逻辑
    merger = VideoMerger()
    
    # 分析真实视频的分辨率
    print("📁 视频文件分辨率:")
    for video in video_files:
        width, height = merger.get_video_resolution(str(video))
        if width and height:
            aspect_ratio = width / height
            size_mb = video.stat().st_size / (1024*1024)
            print(f"  {video.name}")
            print(f"    分辨率: {width}x{height} (比例: {aspect_ratio:.2f}) | {size_mb:.1f}MB")
    
    # 测试新的分辨率选择逻辑
    print(f"\n🧠 智能分辨率选择测试:")
    video_paths = [str(vf) for vf in video_files]
    target_width, target_height = merger.find_target_resolution(video_paths)
    
    print(f"\n✅ 测试完成!")
    print(f"   推荐目标分辨率: {target_width}x{target_height}")
    
if __name__ == "__main__":
    test_aspect_ratio_handling()
    test_real_videos()
