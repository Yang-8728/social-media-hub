"""
回退最后一次合并记录
"""
import json
import os

# 读取合并记录
merge_record_file = "logs/merges/ai_vanvan_merged_record.json"

with open(merge_record_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"当前合并记录数: {len(data['merged_videos'])}")

# 显示最后一条记录
if data['merged_videos']:
    last_record = data['merged_videos'][-1]
    print(f"\n最后一条记录:")
    print(f"  时间: {last_record['timestamp']}")
    print(f"  输出文件: {last_record['output_file']}")
    print(f"  输入视频数: {last_record['input_count']}")
    
    # 删除最后一条记录
    data['merged_videos'].pop()
    
    # 保存
    with open(merge_record_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已删除最后一条记录")
    print(f"剩余合并记录数: {len(data['merged_videos'])}")
else:
    print("没有合并记录")
