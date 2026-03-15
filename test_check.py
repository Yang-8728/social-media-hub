#!/usr/bin/env python3
"""测试检查已下载视频的功能"""
import os
import lzma
import json

download_dir = "/app/downloads/ai_vanvan"

# 列出根目录的已下载shortcodes
print("=" * 50)
print("根目录已下载的shortcodes:")
print("=" * 50)

for filename in os.listdir(download_dir):
    if filename.endswith('.json.xz'):
        json_file_path = os.path.join(download_dir, filename)
        try:
            with open(json_file_path, 'rb') as f:
                content = lzma.decompress(f.read()).decode('utf-8')
                data = json.loads(content)
                node = data.get('node', {})
                shortcode = node.get('shortcode')
                print(f"  {shortcode} <- {filename}")
        except Exception as e:
            print(f"  ERROR: {filename} - {e}")

print("\n" + "=" * 50)
print("子目录统计:")
print("=" * 50)

# 统计子目录
total_files = 0
for item in os.listdir(download_dir):
    item_path = os.path.join(download_dir, item)
    if os.path.isdir(item_path):
        json_files = [f for f in os.listdir(item_path) if f.endswith('.json.xz')]
        if json_files:
            print(f"  {item}/: {len(json_files)} 个视频")
            total_files += len(json_files)

print(f"\n总计: {total_files} 个已下载视频在子目录中")
