"""
合并指定日期文件夹的视频
只合并 2025-08-27 文件夹中的视频
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.logger import Logger
from src.utils.video_merger import VideoMerger
from src.utils.folder_manager import FolderManager
from pathlib import Path

def merge_specific_date_videos():
    account_name = "ai_vanvan"
    target_date = "2025-08-27"
    
    print(f"🎬 开始合并 {account_name} 在 {target_date} 的视频...")
    print("⚡ 使用简单模式，避免复杂处理")
    
    # 创建logger和相关工具
    logger = Logger(account_name)
    video_merger = VideoMerger(account_name)
    
    # 获取指定日期的视频文件
    target_folder = Path(f"videos/downloads/{account_name}/{target_date}")
    
    if not target_folder.exists():
        print(f"❌ 目标文件夹不存在: {target_folder}")
        return
    
    # 查找mp4文件并按文件名排序
    video_files = sorted(list(target_folder.glob("*.mp4")))
    print(f"📁 找到 {len(video_files)} 个视频文件")
    
    if len(video_files) == 0:
        print("❌ 没有找到视频文件")
        return
    
    # 显示视频文件列表和大小
    print(f"\n📋 视频文件列表:")
    total_size = 0
    for i, video_file in enumerate(video_files, 1):
        size_mb = video_file.stat().st_size / (1024*1024)
        total_size += size_mb
        print(f"  {i}. {video_file.name} ({size_mb:.1f}MB)")
    
    print(f"\n📊 总大小: {total_size:.1f}MB")
    
    # 创建输出文件路径
    output_dir = Path(f"videos/merged/{account_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%H-%M-%S")
    output_file = output_dir / f"{account_name}_{target_date}_{timestamp}_{len(video_files)}videos.mp4"
    
    print(f"\n🎯 输出文件: {output_file.name}")
    print("⚠️  使用最简单的FFmpeg concat模式，不做分辨率处理")
    
    # 使用最简单的合并方式
    video_paths = [str(vf) for vf in video_files]
    target_shortcodes = []
    shortcode_to_file = {}
    
    print(f"\n🔍 从json.xz文件直接读取shortcode:")
    
    # 查找json.xz文件并提取shortcode
    json_files = list(target_folder.glob("*.json.xz"))
    
    for json_file in json_files:
        try:
            import lzma
            import json
            
            with open(json_file, 'rb') as f:
                content = lzma.decompress(f.read()).decode('utf-8')
                data = json.loads(content)
                
                # 从instaloader格式提取shortcode
                node = data.get('node', {})
                shortcode = node.get('shortcode')
                owner = node.get('owner', {}).get('username', 'unknown')
                
                if shortcode:
                    # 找到对应的mp4文件
                    base_name = json_file.stem.replace('.json', '')  # 去掉.json后缀
                    mp4_file = target_folder / f"{base_name}.mp4"
                    
                    if mp4_file.exists():
                        target_shortcodes.append(shortcode)
                        shortcode_to_file[shortcode] = {
                            'mp4_file': mp4_file.name,
                            'json_file': json_file.name,
                            'owner': owner
                        }
                        print(f"  - {shortcode} ({owner}) -> {mp4_file.name}")
                    
        except Exception as e:
            print(f"  ⚠️  读取 {json_file.name} 失败: {e}")
    
    print(f"\n📊 实际找到 {len(target_shortcodes)} 个唯一的shortcode:")
    for shortcode in target_shortcodes:
        info = shortcode_to_file[shortcode]
        print(f"  - {shortcode} ({info['owner']}) -> {info['mp4_file']}")
    
    if len(target_shortcodes) == 0:
        print("❌ 没有找到对应的下载记录")
        return
    
    # 询问是否继续
    print(f"\n🎯 准备合并 {target_date} 的 {len(target_shortcodes)} 个视频")
    response = input("是否继续? (y/n): ")
    
    if response.lower() != 'y':
        print("❌ 取消合并")
        return
    
    # 创建视频合并器
    video_merger = VideoMerger(account_name, account_config)
    
    # 执行合并
    print(f"\n🔄 开始合并视频...")
    
    try:
        # 使用批量合并功能
        merged_file_path = video_merger.merge_videos_by_shortcodes(target_shortcodes)
        
        if merged_file_path:
            print(f"✅ 合并成功!")
            print(f"📁 合并文件: {merged_file_path}")
            
            # 标记为已合并
            logger.mark_batch_as_merged(target_shortcodes, merged_file_path)
            print(f"✅ 已标记 {len(target_shortcodes)} 个视频为已合并")
            
        else:
            print(f"❌ 合并失败")
            
    except Exception as e:
        print(f"❌ 合并过程出错: {e}")

if __name__ == "__main__":
    merge_specific_date_videos()
