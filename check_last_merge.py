"""
查看最后一个合并记录
"""
import json

with open('logs/merges/ai_vanvan_merged_record.json', encoding='utf-8') as f:
    data = json.load(f)

last = data['merged_videos'][-1]

print('最后合并记录 (#109):')
print(f"时间: {last['timestamp']}")
print(f"输出: {last['output_file']}")
print(f"视频数: {last['input_count']}")
print(f'\n前5个输入视频:')
for i, v in enumerate(last['input_videos'][:5], 1):
    print(f"  {i}. {v}")
