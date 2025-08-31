"""
奇怪分辨率视频合并测试
专门测试各种非标准分辨率的黑边处理效果
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.video_merger import VideoMerger
from src.utils.logger import Logger

def test_weird_resolution_merge():
    """测试奇怪分辨率视频的合并效果"""
    account_name = "ai_vanvan"
    
    print(f"🧪 奇怪分辨率视频合并测试")
    print("=" * 60)
    print("🎯 目标: 验证各种奇怪分辨率的黑边处理效果")
    print("📐 目标分辨率: 720x1280 (竖屏标准)")
    print()
    
    # 获取downloads目录
    downloads_base = Path(f"videos/downloads/{account_name}")
    
    # 收集各种奇怪分辨率的代表性视频
    target_weird_resolutions = [
        "576x1024",    # 奇怪竖屏 - 应该完美适配
        "720x960",     # 奇怪竖屏 - 会有上下黑边
        "966x720",     # 奇怪横屏 - 会有大量上下黑边
        "480x854",     # 小奇怪竖屏 - 应该很好适配
        "718x880",     # 超奇怪比例 - 测试极限情况
    ]
    
    print(f"🎯 寻找目标分辨率视频:")
    print("-" * 40)
    
    # 创建VideoMerger来获取分辨率
    merger = VideoMerger()
    
    # 收集目标视频
    selected_videos = []
    found_resolutions = set()
    
    for date_folder in downloads_base.iterdir():
        if not date_folder.is_dir():
            continue
            
        for video_file in date_folder.glob("*.mp4"):
            width, height = merger.get_video_resolution(str(video_file))
            if not width or not height:
                continue
                
            resolution_key = f"{width}x{height}"
            
            # 如果是我们要的奇怪分辨率，且还没收集过这种分辨率
            if resolution_key in target_weird_resolutions and resolution_key not in found_resolutions:
                selected_videos.append({
                    'path': video_file,
                    'resolution': resolution_key,
                    'width': width,
                    'height': height,
                    'size_mb': video_file.stat().st_size / (1024*1024),
                    'aspect_ratio': width / height
                })
                found_resolutions.add(resolution_key)
                print(f"  ✅ {resolution_key:<12} | {video_file.name[:40]:<40} | {video_file.stat().st_size / (1024*1024):.1f}MB")
    
    # 如果没找够，添加一些标准分辨率作为对比
    if len(selected_videos) < 5:
        print(f"\n🔍 添加标准分辨率视频作为对比:")
        for date_folder in downloads_base.iterdir():
            if not date_folder.is_dir():
                continue
            for video_file in date_folder.glob("*.mp4"):
                if len(selected_videos) >= 8:  # 最多8个视频
                    break
                    
                width, height = merger.get_video_resolution(str(video_file))
                if not width or not height:
                    continue
                    
                resolution_key = f"{width}x{height}"
                
                # 添加720x1280标准分辨率作为对比
                if resolution_key == "720x1280" and "720x1280" not in found_resolutions:
                    selected_videos.append({
                        'path': video_file,
                        'resolution': resolution_key,
                        'width': width,
                        'height': height,
                        'size_mb': video_file.stat().st_size / (1024*1024),
                        'aspect_ratio': width / height
                    })
                    found_resolutions.add(resolution_key)
                    print(f"  📱 {resolution_key:<12} | {video_file.name[:40]:<40} | {video_file.stat().st_size / (1024*1024):.1f}MB (标准对比)")
                    break
    
    if not selected_videos:
        print("❌ 没有找到合适的测试视频")
        return
    
    print(f"\n📊 测试视频汇总:")
    print("-" * 60)
    
    total_size = 0
    for i, video in enumerate(selected_videos, 1):
        # 计算黑边效果预览
        target_w, target_h = 720, 1280
        scale_w = target_w / video['width']
        scale_h = target_h / video['height']
        scale = min(scale_w, scale_h)
        
        new_w = int(video['width'] * scale)
        new_h = int(video['height'] * scale)
        pad_x = (target_w - new_w) // 2
        pad_y = (target_h - new_h) // 2
        content_ratio = (new_w * new_h) / (target_w * target_h)
        
        total_size += video['size_mb']
        
        print(f"  {i}. {video['resolution']:<12} | 比例:{video['aspect_ratio']:5.2f} | "
              f"缩放:{new_w}x{new_h:<9} | 黑边:({pad_x},{pad_y})<8 | "
              f"内容:{content_ratio*100:4.1f}% | {video['size_mb']:.1f}MB")
        print(f"     📁 {video['path'].name}")
    
    print(f"\n📊 总计: {len(selected_videos)} 个视频, {total_size:.1f}MB")
    
    # 预测合并效果
    print(f"\n🔮 预期黑边效果:")
    print("-" * 40)
    excellent = sum(1 for v in selected_videos if (min(720/v['width'], 1280/v['height']) * v['width'] * v['height']) / (720*1280) > 0.9)
    good = sum(1 for v in selected_videos if 0.7 <= (min(720/v['width'], 1280/v['height']) * v['width'] * v['height']) / (720*1280) <= 0.9)
    acceptable = len(selected_videos) - excellent - good
    
    print(f"  🟢 优秀 (内容占比>90%): {excellent} 个")
    print(f"  🟡 良好 (内容占比70-90%): {good} 个")
    print(f"  🟠 可接受 (内容占比<70%): {acceptable} 个")
    
    # 询问是否执行合并
    response = input(f"\n🔄 开始合并这 {len(selected_videos)} 个奇怪分辨率视频吗? (y/n): ")
    
    if response.lower() != 'y':
        print("❌ 取消测试")
        return
    
    # 创建输出文件
    output_dir = Path(f"videos/merged/{account_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%H-%M-%S")
    output_file = output_dir / f"{account_name}_weird_resolutions_test_{timestamp}.mp4"
    
    print(f"\n📝 输出文件: {output_file.name}")
    
    try:
        logger = Logger(account_name)
        video_merger = VideoMerger(account_name)
        
        print(f"\n🔄 开始奇怪分辨率合并测试...")
        print("⏳ 注意观察:")
        print("   1. 各种分辨率的标准化处理")
        print("   2. 黑边添加效果")
        print("   3. 内容保真情况")
        print("   4. 最终统一效果")
        
        # 使用智能合并
        video_paths = [str(v['path']) for v in selected_videos]
        success = video_merger.merge_videos_with_normalization(video_paths, str(output_file))
        
        if success:
            output_size = output_file.stat().st_size / (1024*1024)
            print(f"\n✅ 奇怪分辨率合并测试完成!")
            print(f"📁 文件: {output_file}")
            print(f"📊 大小: {output_size:.1f}MB (原始: {total_size:.1f}MB)")
            
            # 验证最终分辨率
            final_width, final_height = video_merger.get_video_resolution(str(output_file))
            if final_width and final_height:
                print(f"🎯 最终分辨率: {final_width}x{final_height}")
                
                if (final_width, final_height) == (720, 1280):
                    print("✅ 分辨率统一成功!")
                else:
                    print("⚠️  分辨率异常")
            
            # 记录测试结果
            logger.info(f"奇怪分辨率合并测试: {len(selected_videos)} 个视频 -> {output_file.name}")
            
            # 询问是否运行质量检查
            response = input("\n🔍 运行详细质量检查验证黑边效果? (y/n): ")
            if response.lower() == 'y':
                print("🔍 运行质量检查...")
                try:
                    from tools.scripts.video_quality_checker import VideoQualityChecker
                    checker = VideoQualityChecker()
                    result = checker.comprehensive_check(str(output_file))
                    
                    print(f"\n🎯 黑边处理验证结果:")
                    if not result.get('black_frames', True):
                        print("✅ 无异常黑屏问题")
                    if result.get('bilibili_compatible', False):
                        print("✅ B站兼容性良好")
                    print("💡 建议打开视频文件检查黑边效果是否符合预期")
                    
                except Exception as e:
                    print(f"⚠️  质量检查失败: {e}")
            
        else:
            print("❌ 合并失败")
            
    except Exception as e:
        print(f"❌ 测试过程出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_weird_resolution_merge()
