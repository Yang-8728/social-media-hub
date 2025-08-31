"""
简单的视频合并测试 - 避免复杂处理
只用最基本的FFmpeg concat功能
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.video_merger import VideoMerger

def simple_merge_test():
    account_name = "ai_vanvan"
    target_date = "2025-08-27"
    
    print(f"🎬 简单合并测试: {account_name} - {target_date}")
    print("⚡ 使用最基本的FFmpeg concat，避免任何智能处理")
    
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
    for i, vf in enumerate(video_files, 1):
        size_mb = vf.stat().st_size / (1024*1024)
        total_size += size_mb
        print(f"  {i}. {vf.name} ({size_mb:.1f}MB)")
    
    print(f"\n📊 总大小: {total_size:.1f}MB")
    
    # 创建输出目录和文件
    output_dir = Path(f"videos/merged/{account_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%H-%M-%S")
    output_file = output_dir / f"{account_name}_{target_date}_{timestamp}_simple.mp4"
    
    print(f"\n🎯 输出: {output_file.name}")
    
    # 确认是否继续
    response = input("\n⚠️  使用最简单模式合并，可能有分辨率不一致问题，继续吗? (y/n): ")
    
    if response.lower() != 'y':
        print("❌ 取消合并")
        return
    
    # 创建简单的VideoMerger，不传账号配置
    try:
        video_merger = VideoMerger()  # 不传account_name避免配置加载
        video_paths = [str(vf) for vf in video_files]
        
        print(f"\n🔄 开始合并 {len(video_paths)} 个视频...")
        print("⚡ 使用直接concat模式（最快但可能有画面问题）")
        
        # 使用最简单的FFmpeg concat
        success = video_merger.merge_videos_with_ffmpeg(video_paths, str(output_file))
        
        if success:
            output_size = output_file.stat().st_size / (1024*1024)
            print(f"\n✅ 合并完成!")
            print(f"📁 文件: {output_file}")
            print(f"📊 大小: {output_size:.1f}MB")
            
            # 可选的质量检查
            response = input("\n🔍 要运行质量检查吗? (y/n): ")
            if response.lower() == 'y':
                print("🔍 检查视频质量...")
                try:
                    # 快速检查文件是否能正常读取
                    from src.utils.video_merger import VideoMerger
                    temp_merger = VideoMerger()
                    width, height = temp_merger.get_video_resolution(str(output_file))
                    
                    if width and height:
                        print(f"✅ 视频可正常读取，分辨率: {width}x{height}")
                        
                        # 检查文件大小是否合理
                        if output_size > total_size * 0.8:  # 至少保持80%的原大小
                            print("✅ 文件大小正常")
                        else:
                            print("⚠️  文件大小偏小，可能有问题")
                    else:
                        print("❌ 无法读取视频信息，可能损坏")
                        
                except Exception as e:
                    print(f"⚠️  质量检查失败: {e}")
        else:
            print("❌ 合并失败")
            
    except Exception as e:
        print(f"❌ 合并过程出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_merge_test()
