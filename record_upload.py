"""
记录上传成功的视频
用法: python record_upload.py <编号> <BV号>
示例: python record_upload.py 124 BV1sq1rBME77
"""
import sys
from upload_tracker import record_upload

if len(sys.argv) < 3:
    print("用法: python record_upload.py <编号> <BV号>")
    print("示例: python record_upload.py 124 BV1sq1rBME77")
    exit(1)

number = int(sys.argv[1])
bv_id = sys.argv[2]
account = "ai_vanvan"

title = f"ins海外离大谱#{number}"
record = record_upload(account, number, bv_id, title)

print("=" * 70)
print("✅ 上传记录已保存")
print("=" * 70)
print(f"编号: #{number}")
print(f"标题: {title}")
print(f"BV号: {bv_id}")
print(f"链接: https://www.bilibili.com/video/{bv_id}")
print(f"时间: {record['upload_time']}")
