"""
高质量视频合并测试 - 保持最高分辨率
自动选择最高质量分辨率作为目标，避免降级
"""
import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.video_merger import VideoMerger

def test_high_quality_merge():
    """测试高质量合并逻辑"""
    account_name = "ai_vanvan"
    target_date = "2025-08-27"
    
    print(f"🎬 高质量智能合并测试: {account_name} - {target_date}")
    print("🔧 新功能:")
    print("  ✅ 自动选择最高质量分辨率作为目标")
    print("  ✅ 避免不必要的质量降级")
    print("  ✅ 保持1080p视频的清晰度")
    print("  ✅ 智能黑边填充")
    
    # 获取目标文件夹
    target_folder = Path(f"videos/downloads/{account_name}/{target_date}")
    
    if not target_folder.exists():
        print(f"❌ 文件夹不存在: {target_folder}")
        return
    
    # 获取所有mp4文件
    video_files = sorted(list(target_folder.glob("*.mp4")))
    
    if not video_files:
        print("❌ 没有找到mp4文件")
        return
    
    # 创建VideoMerger来分析分辨率
    merger = VideoMerger()
    
    print(f"\n📁 找到 {len(video_files)} 个视频文件，分析分辨率...")
    
    # 测试新的智能分辨率选择
    video_paths = [str(vf) for vf in video_files]
    target_width, target_height = merger.find_target_resolution(video_paths)
    
    print(f"\n🎯 新算法选择的目标分辨率: {target_width}x{target_height}")
    
    # 与之前的固定720p比较
    print(f"\n📊 与固定720p方案比较:")
    print(f"  旧方案: 固定720x1280 (可能降级1080p视频)")
    print(f"  新方案: {target_width}x{target_height} (保持最高质量)")
    
    if target_height > 1280:
        print(f"  ✅ 新方案更优: 保持了1080p清晰度!")
    elif target_height == 1280:
        print(f"  ➡️ 分辨率相同: 没有1080p视频需要保护")
    else:
        print(f"  📱 适配内容: 选择了适合的分辨率")
    
    # 询问是否执行合并
    response = input(f"\n🔄 要用新的高质量算法合并视频吗? (y/n): ")
    
    if response.lower() != 'y':
        print("❌ 取消测试")
        return
    
    # 创建输出文件
    output_dir = Path(f"videos/merged/{account_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%H-%M-%S")
    output_file = output_dir / f"{account_name}_{target_date}_{timestamp}_highquality.mp4"
    
    print(f"\n📝 输出文件: {output_file.name}")
    
    try:
        from src.utils.logger import Logger
        logger = Logger(account_name)
        video_merger = VideoMerger(account_name)
        
        print(f"\n🔄 开始高质量合并...")
        
        # 使用新的智能合并
        success = video_merger.merge_videos_with_normalization(video_paths, str(output_file))
        
        if success:
            output_size = output_file.stat().st_size / (1024*1024)
            print(f"\n✅ 高质量合并完成!")
            print(f"📁 文件: {output_file}")
            print(f"📊 大小: {output_size:.1f}MB")
            
            # 验证最终分辨率
            final_width, final_height = video_merger.get_video_resolution(str(output_file))
            if final_width and final_height:
                print(f"🎯 最终分辨率: {final_width}x{final_height}")
                
                if (final_width, final_height) == (target_width, target_height):
                    print("✅ 分辨率完全匹配!")
                    
                    # 计算质量提升
                    if final_height > 1280:
                        improvement = ((final_width * final_height) / (720 * 1280) - 1) * 100
                        print(f"🚀 比720p方案提升 {improvement:.0f}% 像素!")
                        
            logger.info(f"高质量合并完成: {len(video_files)} 个视频 -> {output_file.name}")
            
        else:
            print("❌ 合并失败")
            
    except Exception as e:
        print(f"❌ 合并过程出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_high_quality_merge()
