#!/usr/bin/env python3
"""测试 Instagram CDN 访问"""

import requests
import time

# 测试 URL
cdn_nodes = [
    "instagram.fbkk29-1.fna.fbcdn.net",
    "instagram.fbkk29-4.fna.fbcdn.net", 
    "instagram.fbkk29-7.fna.fbcdn.net",
    "instagram.fbkk29-8.fna.fbcdn.net",
]

print("🔍 测试 Instagram CDN 节点访问\n")

for node in cdn_nodes:
    url = f"https://{node}/"
    
    # 测试1: 不带 Headers
    print(f"📡 测试节点: {node}")
    try:
        start = time.time()
        r = requests.head(url, timeout=5)
        elapsed = time.time() - start
        print(f"   ✅ 无Headers: {r.status_code} ({elapsed:.2f}s)")
    except Exception as e:
        print(f"   ❌ 无Headers: {type(e).__name__}: {str(e)[:50]}")
    
    # 测试2: 带浏览器 Headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.instagram.com/'
    }
    try:
        start = time.time()
        r = requests.head(url, headers=headers, timeout=5)
        elapsed = time.time() - start
        print(f"   ✅ 带Headers: {r.status_code} ({elapsed:.2f}s)")
    except Exception as e:
        print(f"   ❌ 带Headers: {type(e).__name__}: {str(e)[:50]}")
    
    print()
