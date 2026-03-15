"""
标记 YouTube 测试视频为"已合并"
这样系统会跳过这些视频，不会重复合并
"""
import os
import json
import glob
from datetime import datetime

def mark_videos_as_merged():
    """标记今天下载的 YouTube 视频为已合并"""
    
    account_name = "youtube"
    
    # 查找今天的视频
    today = datetime.now().strftime("%Y-%m-%d")
    video_dir = f"videos/downloads/{account_name}/{today}"
    
    if not os.path.exists(video_dir):
        print(f"❌ 视频目录不存在: {video_dir}")
        return
    
    # 获取所有视频文件
    video_files = glob.glob(os.path.join(video_dir, "*.mp4"))
    
    if not video_files:
        print(f"❌ 没有找到视频文件")
        return
    
    print(f"📁 找到 {len(video_files)} 个视频文件")
    for video in video_files:
        print(f"   - {os.path.basename(video)}")
    
    # 加载或创建合并记录
    merged_record_file = f"logs/merges/{account_name}_merged_record.json"
    os.makedirs(os.path.dirname(merged_record_file), exist_ok=True)
    
    if os.path.exists(merged_record_file):
        with open(merged_record_file, 'r', encoding='utf-8') as f:
            record = json.load(f)
    else:
        record = {"merged_videos": []}
    
    # 创建一个虚拟的合并记录
    merge_info = {
        "timestamp": datetime.now().isoformat(),
        "output_file": "测试视频_已跳过.mp4",
        "input_videos": [os.path.abspath(v) for v in video_files],
        "input_count": len(video_files),
        "note": "手动标记为已合并（测试视频）"
    }
    
    record["merged_videos"].append(merge_info)
    
    # 保存记录
    with open(merged_record_file, 'w', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已标记 {len(video_files)} 个视频为'已合并'")
    print(f"📝 记录文件: {merged_record_file}")
    print(f"\n💡 现在这些视频会被跳过，不会重复合并")
    print(f"🎯 你可以：")
    print(f"   1. 去 YouTube 点赞新的视频")
    print(f"   2. 运行: python main.py --youtube")
    print(f"   3. 系统会只处理新点赞的视频")

if __name__ == "__main__":
    mark_videos_as_merged()
