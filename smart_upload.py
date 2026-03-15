"""
智能上传脚本 - 自动追踪编号，支持删除后重新上传
"""
import redis
import json
from pathlib import Path
from upload_tracker import get_next_number, record_upload

# 连接 Redis
redis_client = redis.from_url("redis://localhost:6379")

# 获取下一个编号
account = "ai_vanvan"
next_number = get_next_number(account)

print("=" * 70)
print(f"📤 准备上传 #{next_number}")
print("=" * 70)

# 检查对应文件是否存在
video_file = Path(f"videos/merged/{account}/ins海外离大谱#{next_number}.mp4")

if not video_file.exists():
    print(f"\n❌ 文件不存在: {video_file}")
    print(f"\n可用的视频文件:")
    
    merged_dir = Path(f"videos/merged/{account}")
    if merged_dir.exists():
        files = sorted(merged_dir.glob("ins海外离大谱#*.mp4"), 
                      key=lambda x: x.stat().st_mtime, reverse=True)
        for f in files[:5]:
            size_mb = f.stat().st_size / 1024 / 1024
            print(f"  - {f.name} ({size_mb:.2f} MB)")
    
    print(f"\n💡 提示:")
    print(f"  1. 如果想上传现有文件，请重命名为: ins海外离大谱#{next_number}.mp4")
    print(f"  2. 或者先运行合并任务生成新视频")
    exit(1)

# 文件存在，准备上传
file_size_mb = video_file.stat().st_size / 1024 / 1024
print(f"\n✅ 找到视频文件: {video_file.name}")
print(f"   大小: {file_size_mb:.2f} MB")

# 准备任务数据
task = {
    "account": account,
    "video_path": f"/videos/{account}/ins海外离大谱#{next_number}.mp4",
    "title": f"ins海外离大谱#{next_number}",
    "tid": 138,  # 生活 > 搞笑
    "tag": "Instagram,搞笑,离大谱,海外,沙雕"
}

print(f"\n视频信息:")
print(f"  编号: #{next_number}")
print(f"  标题: {task['title']}")
print(f"  分区: 138 (生活 > 搞笑)")
print(f"  标签: {task['tag']}")

# 发送到队列
redis_client.rpush("biliup:queue", json.dumps(task))

print(f"\n✅ 任务已发送到 biliup:queue")
print(f"\n📊 查看进度:")
print(f"   docker logs biliup-uploader --tail 30 --follow")
print(f"\n⚠️  上传成功后，请运行以下命令记录BV号:")
print(f"   python record_upload.py {next_number} <BV号>")
