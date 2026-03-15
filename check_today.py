#!/usr/bin/env python3
"""检查今天下载的视频shortcodes"""
import os
import lzma
import json

today_dir = "/app/downloads/ai_vanvan/2025-10-09"

if not os.path.exists(today_dir):
    print(f"目录不存在: {today_dir}")
    exit(1)

print("=" * 60)
print("今天(2025-10-09)下载的视频shortcodes:")
print("=" * 60)

shortcodes = []
for filename in os.listdir(today_dir):
    if filename.endswith('.json.xz'):
        json_file_path = os.path.join(today_dir, filename)
        try:
            with open(json_file_path, 'rb') as f:
                content = lzma.decompress(f.read()).decode('utf-8')
                data = json.loads(content)
                node = data.get('node', {})
                shortcode = node.get('shortcode')
                if shortcode:
                    shortcodes.append(shortcode)
                    print(f"  {shortcode}")
        except Exception as e:
            print(f"  ERROR: {filename} - {e}")

print(f"\n总计: {len(shortcodes)} 个视频")

# 保存到文件供测试
with open('/tmp/today_shortcodes.txt', 'w') as f:
    for sc in shortcodes:
        f.write(f"{sc}\n")

print(f"\n已保存shortcodes到: /tmp/today_shortcodes.txt")
