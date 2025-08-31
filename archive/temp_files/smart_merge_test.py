"""
智能视频合并 - 保留分辨率统一功能
自动检测竖屏视频，统一为标准分辨率，添加黑边避免变形
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.video_merger import VideoMerger
from src.utils.logger import Logger

def smart_merge_test():
    account_name = "ai_vanvan"
    target_date = "2025-08-27"
    
    print(f"🎬 智能视频合并: {account_name} - {target_date}")
    print("🔧 功能:")
    print("  ✅ 自动检测竖屏/横屏")
    print("  ✅ 统一为标准分辨率")
    print("  ✅ 保持长宽比，添加黑边")
    print("  ✅ 高质量编码 (H.264 + AAC)")
    
    # 获取目标文件夹
    target_folder = Path(f"videos/downloads/{account_name}/{target_date}")
    
    if not target_folder.exists():
        print(f"❌ 文件夹不存在: {target_folder}")
        return
    
    # 获取所有mp4文件，按文件名排序
    video_files = sorted(list(target_folder.glob("*.mp4")))
    
    if not video_files:
        print("❌ 没有找到mp4文件")
        return
    
    print(f"\n📁 找到 {len(video_files)} 个视频文件:")
    total_size = 0
    
    # 创建VideoMerger来检查分辨率
    temp_merger = VideoMerger()
    
    for i, vf in enumerate(video_files, 1):
        size_mb = vf.stat().st_size / (1024*1024)
        total_size += size_mb
        
        # 获取分辨率信息
        width, height = temp_merger.get_video_resolution(str(vf))
        orientation = "竖屏" if height and width and height > width else "横屏"
        resolution_str = f"{width}x{height}" if width and height else "未知"
        
        print(f"  {i}. {vf.name}")
        print(f"     📐 {resolution_str} ({orientation}) - {size_mb:.1f}MB")
    
    print(f"\n📊 总大小: {total_size:.1f}MB")
    
    # 分析目标分辨率
    video_paths = [str(vf) for vf in video_files]
    target_width, target_height = temp_merger.find_target_resolution(video_paths)
    
    orientation = "竖屏" if target_height > target_width else "横屏"
    print(f"\n🎯 目标分辨率: {target_width}x{target_height} ({orientation})")
    
    # 检查是否需要分辨率统一
    resolutions = set()
    for vf in video_files:
        w, h = temp_merger.get_video_resolution(str(vf))
        if w and h:
            resolutions.add((w, h))
    
    if len(resolutions) > 1:
        print(f"⚠️  检测到 {len(resolutions)} 种不同分辨率，需要统一处理")
        for res in resolutions:
            print(f"    - {res[0]}x{res[1]}")
    else:
        print("✅ 所有视频分辨率一致，但仍会进行标准化处理")
    
    # 创建输出目录和文件
    output_dir = Path(f"videos/merged/{account_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%H-%M-%S")
    output_file = output_dir / f"{account_name}_{target_date}_{timestamp}_normalized.mp4"
    
    print(f"\n📝 输出: {output_file.name}")
    
    # 确认是否继续
    response = input(f"\n🔄 准备处理 {len(video_files)} 个视频，统一分辨率后合并，继续吗? (y/n): ")
    
    if response.lower() != 'y':
        print("❌ 取消合并")
        return
    
    # 创建带日志的VideoMerger
    try:
        logger = Logger(account_name)
        video_merger = VideoMerger(account_name)
        
        print(f"\n🔄 开始智能合并...")
        print("⏳ 这个过程会比较慢，因为需要:")
        print("   1. 分析每个视频的分辨率")
        print("   2. 标准化分辨率(添加黑边)")
        print("   3. 重新编码为高质量格式")
        print("   4. 合并所有处理后的视频")
        
        # 使用智能分辨率统一合并
        success = video_merger.merge_videos_with_normalization(video_paths, str(output_file))
        
        if success:
            output_size = output_file.stat().st_size / (1024*1024)
            print(f"\n✅ 智能合并完成!")
            print(f"📁 文件: {output_file}")
            print(f"📊 大小: {output_size:.1f}MB")
            
            # 验证输出视频的分辨率
            final_width, final_height = video_merger.get_video_resolution(str(output_file))
            if final_width and final_height:
                print(f"🎯 最终分辨率: {final_width}x{final_height}")
                
                if (final_width, final_height) == (target_width, target_height):
                    print("✅ 分辨率统一成功!")
                else:
                    print("⚠️  最终分辨率与目标不符")
            
            # 记录到日志
            logger.info(f"智能合并完成: {len(video_files)} 个视频 -> {output_file.name}")
            
            # 可选的详细质量检查
            response = input("\n🔍 要运行详细质量检查吗? (y/n): ")
            if response.lower() == 'y':
                print("🔍 运行质量分析...")
                try:
                    from tools.scripts.video_quality_checker import VideoQualityChecker
                    checker = VideoQualityChecker()
                    result = checker.comprehensive_check(str(output_file))
                    
                    print(f"\n📊 详细质量检查结果:")
                    
                    # 计算质量评分
                    score = 0
                    total = 6
                    
                    if not result.get('resolution_issues', True): score += 1
                    if not result.get('framerate_issues', True): score += 1  
                    if result.get('audio_sync', False): score += 1
                    if not result.get('black_frames', True): score += 1
                    if not result.get('corruption', True): score += 1
                    if result.get('bilibili_compatible', False): score += 1
                    
                    print(f"  - 质量评分: {score}/{total} ({score/total*100:.0f}%)")
                    print(f"  - 分辨率: {'✅ 正常' if not result.get('resolution_issues') else '❌ 有问题'}")
                    print(f"  - 帧率: {'✅ 正常' if not result.get('framerate_issues') else '❌ 有问题'}")
                    print(f"  - 音画同步: {'✅ 正常' if result.get('audio_sync') else '❌ 有问题'}")
                    print(f"  - 黑屏检测: {'✅ 无黑屏' if not result.get('black_frames') else '❌ 有黑屏'}")
                    print(f"  - 文件完整性: {'✅ 正常' if not result.get('corruption') else '❌ 损坏'}")
                    print(f"  - B站兼容性: {'✅ 兼容' if result.get('bilibili_compatible') else '❌ 不兼容'}")
                    
                    if score == total:
                        print("\n🎉 视频质量完美，可以上传!")
                    elif score >= 4:
                        print("\n✅ 视频质量良好，基本可以使用")
                    else:
                        print("\n⚠️  视频存在质量问题，建议检查")
                        
                except Exception as e:
                    print(f"⚠️  质量检查失败: {e}")
        else:
            print("❌ 智能合并失败")
            print("💡 可能的原因:")
            print("   - FFmpeg工具问题")
            print("   - 视频文件损坏")
            print("   - 磁盘空间不足")
            
    except Exception as e:
        print(f"❌ 合并过程出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    smart_merge_test()
