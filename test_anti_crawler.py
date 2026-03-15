#!/usr/bin/env python3
"""检测 Instagram 是否对 IP 进行了反爬虫限制"""

import requests
import time
from datetime import datetime

def test_instagram_access():
    """测试 Instagram 各种访问方式"""
    
    print("=" * 60)
    print("🔍 Instagram 反爬虫检测")
    print("=" * 60)
    print()
    
    # 测试1: 主站访问
    print("📋 测试1: Instagram 主站访问")
    try:
        r = requests.get('https://www.instagram.com/', timeout=10)
        print(f"   ✅ 主站状态: {r.status_code}")
        if r.status_code == 429:
            print(f"   ⚠️  检测到速率限制！")
        elif r.status_code == 403:
            print(f"   ⚠️  检测到访问被禁止！")
    except Exception as e:
        print(f"   ❌ 主站访问失败: {e}")
    print()
    
    # 测试2: API 访问
    print("📋 测试2: Instagram GraphQL API 访问")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        r = requests.get('https://www.instagram.com/graphql/query/', 
                        headers=headers, timeout=10)
        print(f"   状态: {r.status_code}")
        if r.status_code == 429:
            print(f"   ⚠️  API 被限速！这是反爬虫的明确信号！")
            return True
        elif r.status_code == 403:
            print(f"   ⚠️  API 访问被禁止！IP 可能被封！")
            return True
    except Exception as e:
        print(f"   ❌ API 访问失败: {e}")
    print()
    
    # 测试3: CDN 图片访问（公开资源）
    print("📋 测试3: Instagram CDN 公开资源访问")
    test_urls = [
        "https://instagram.fbkk29-1.fna.fbcdn.net/",
        "https://instagram.fbkk29-8.fna.fbcdn.net/",
    ]
    
    for url in test_urls:
        try:
            start = time.time()
            r = requests.head(url, timeout=8)
            elapsed = time.time() - start
            print(f"   ✅ {url.split('//')[1].split('/')[0]}: {r.status_code} ({elapsed:.2f}s)")
        except requests.exceptions.ConnectTimeout:
            print(f"   ❌ {url.split('//')[1].split('/')[0]}: 连接超时 (反爬虫可能性)")
        except requests.exceptions.ReadTimeout:
            print(f"   ❌ {url.split('//')[1].split('/')[0]}: 读取超时 (反爬虫可能性)")
        except Exception as e:
            print(f"   ❌ {url.split('//')[1].split('/')[0]}: {type(e).__name__}")
    print()
    
    # 测试4: 带 Session 的访问（模拟登录后）
    print("📋 测试4: 模拟已登录用户访问")
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        r = session.get('https://www.instagram.com/', timeout=10)
        print(f"   状态: {r.status_code}")
        
        # 检查是否有限速相关的响应头
        if 'X-Ratelimit-Remaining' in r.headers:
            print(f"   速率限制剩余: {r.headers['X-Ratelimit-Remaining']}")
        if 'Retry-After' in r.headers:
            print(f"   ⚠️  要求延迟: {r.headers['Retry-After']} 秒")
    except Exception as e:
        print(f"   ❌ 模拟登录访问失败: {e}")
    print()
    
    # 测试5: 检查是否能访问公开账号
    print("📋 测试5: 访问公开 Instagram 账号")
    try:
        r = requests.get('https://www.instagram.com/instagram/', timeout=10)
        print(f"   状态: {r.status_code}")
        if r.status_code == 200:
            print(f"   ✅ 可以访问公开账号页面")
        elif r.status_code == 429:
            print(f"   ⚠️  账号页面也被限速！")
            return True
        elif r.status_code == 403:
            print(f"   ⚠️  账号页面访问被禁！")
            return True
    except Exception as e:
        print(f"   ❌ 访问失败: {e}")
    print()
    
    print("=" * 60)
    print("📊 诊断结果")
    print("=" * 60)
    print()
    print("如果看到以下情况，说明是反爬虫：")
    print("  • 429 状态码 (Too Many Requests)")
    print("  • 403 状态码 (Forbidden)")  
    print("  • Retry-After 响应头")
    print("  • 主站可访问，但 API/CDN 超时")
    print()
    print("如果看到以下情况，说明是网络问题：")
    print("  • 所有请求都超时")
    print("  • 没有特定的 HTTP 错误码")
    print("  • 连接层面就失败")
    print()
    
    return False

if __name__ == "__main__":
    test_instagram_access()
