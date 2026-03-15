"""
标记旧的 YouTube 视频为"已合并"
只保留最后 4 个视频为未合并状态
"""
import os
import json
import glob
from datetime import datetime

def mark_old_videos_as_merged():
    """标记旧视频为已合并，只保留最后 4 个为未合并"""
    
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
    
    # 按修改时间排序（最早的在前）
    video_files.sort(key=lambda x: os.path.getmtime(x))
    
    print(f"📁 找到 {len(video_files)} 个视频文件")
    print(f"📊 按下载时间排序：")
    for i, video in enumerate(video_files, 1):
        mtime = datetime.fromtimestamp(os.path.getmtime(video))
        print(f"   {i}. {os.path.basename(video)} - {mtime.strftime('%H:%M:%S')}")
    
    # 计算要标记为已合并的视频数量
    total_videos = len(video_files)
    keep_unmerged = 4  # 保留最后 4 个为未合并
    
    if total_videos <= keep_unmerged:
        print(f"\n✅ 视频总数 ({total_videos}) <= {keep_unmerged}，全部保持未合并状态")
        return
    
    # 前面的视频标记为已合并
    videos_to_mark = video_files[:-keep_unmerged]
    videos_to_keep = video_files[-keep_unmerged:]
    
    print(f"\n📋 处理方案：")
    print(f"   标记为已合并：前 {len(videos_to_mark)} 个视频")
    print(f"   保持未合并：最后 {len(videos_to_keep)} 个视频")
    
    # 加载或创建合并记录
    merged_record_file = f"logs/merges/{account_name}_merged_record.json"
    os.makedirs(os.path.dirname(merged_record_file), exist_ok=True)
    
    if os.path.exists(merged_record_file):
        with open(merged_record_file, 'r', encoding='utf-8') as f:
            record = json.load(f)
        print(f"\n📝 加载现有记录：{len(record.get('merged_videos', []))} 条")
    else:
        record = {"merged_videos": []}
        print(f"\n📝 创建新记录文件")
    
    # 创建合并记录（标记为已合并）
    merge_info = {
        "timestamp": datetime.now().isoformat(),
        "output_file": "旧视频_已跳过.mp4",
        "input_videos": [os.path.abspath(v) for v in videos_to_mark],
        "input_count": len(videos_to_mark),
        "note": f"手动标记为已合并（保留最后{keep_unmerged}个为未合并）"
    }
    
    record["merged_videos"].append(merge_info)
    
    # 保存记录
    with open(merged_record_file, 'w', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已标记 {len(videos_to_mark)} 个视频为'已合并'")
    print(f"📝 记录文件: {merged_record_file}")
    
    print(f"\n📊 标记为已合并的视频：")
    for video in videos_to_mark:
        print(f"   ✅ {os.path.basename(video)}")
    
    print(f"\n📊 保持未合并的视频（最后{keep_unmerged}个）：")
    for video in videos_to_keep:
        print(f"   ⏳ {os.path.basename(video)}")
    
    print(f"\n💡 现在运行完整流程时：")
    print(f"   1. 会下载新点赞的视频")
    print(f"   2. 只合并最后 {keep_unmerged} 个旧视频 + 新视频")
    print(f"   3. 前 {len(videos_to_mark)} 个旧视频会被跳过")

if __name__ == "__main__":
    mark_old_videos_as_merged()
