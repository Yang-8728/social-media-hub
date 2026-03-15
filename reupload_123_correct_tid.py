import redis
import json

# 连接 Redis
redis_client = redis.from_url("redis://localhost:6379")

# 准备任务数据 - 重新上传 #123 到正确分区
task = {
    "account": "ai_vanvan",
    "video_path": "/videos/ai_vanvan/ins海外离大谱#123.mp4",
    "title": "ins海外离大谱#123",
    "tid": 138,  # 生活 > 搞笑（修正！）
    "tag": "Instagram,搞笑,离大谱,海外,沙雕"
}

print("=" * 70)
print("📤 重新上传 #123 到正确分区")
print("=" * 70)
print(f"\n视频信息:")
print(f"  标题: {task['title']}")
print(f"  分区: 138 (生活 > 搞笑) ← 修正！")
print(f"  标签: {task['tag']}")
print(f"  路径: {task['video_path']}")

print(f"\n⚠️  注意: 需要先在B站删除之前的 #123 (BV1cx1kBvEtG)")
print(f"  或者改成 #124 避免重复")

choice = input("\n继续上传? (y/n): ")

if choice.lower() == 'y':
    # 发送到队列
    redis_client.rpush("biliup:queue", json.dumps(task))
    print(f"\n✅ 任务已发送到 biliup:queue")
    print(f"\n查看日志: docker logs biliup-uploader --tail 30 --follow")
else:
    print("\n❌ 已取消")
