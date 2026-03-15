#!/usr/bin/env python3
"""
验证 Instagram CDN 问题是否是广泛存在的
通过多种方式检测
"""

import requests
import socket
import time
from datetime import datetime

def test_cdn_from_multiple_sources():
    """从多个角度测试 CDN"""
    
    print("=" * 60)
    print("🔍 Instagram CDN 问题验证")
    print("=" * 60)
    print()
    
    # 1. 测试 DNS 解析
    print("📋 测试1: DNS 解析（检查 CDN 节点是否存在）")
    test_nodes = [
        "instagram.fbkk29-1.fna.fbcdn.net",
        "instagram.fbkk29-4.fna.fbcdn.net",
        "instagram.fbkk29-8.fna.fbcdn.net",
    ]
    
    dns_results = {}
    for node in test_nodes:
        try:
            ip = socket.gethostbyname(node)
            dns_results[node] = ip
            print(f"   ✅ {node}: {ip}")
        except Exception as e:
            print(f"   ❌ {node}: DNS解析失败 - {e}")
    print()
    
    # 2. 测试 TCP 连接
    print("📋 测试2: TCP 443 端口连接")
    tcp_results = {}
    for node, ip in dns_results.items():
        try:
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((ip, 443))
            elapsed = time.time() - start
            sock.close()
            
            if result == 0:
                tcp_results[node] = True
                print(f"   ✅ {node}: TCP 连接成功 ({elapsed:.2f}s)")
            else:
                tcp_results[node] = False
                print(f"   ❌ {node}: TCP 连接失败 (错误码: {result})")
        except Exception as e:
            tcp_results[node] = False
            print(f"   ❌ {node}: {e}")
    print()
    
    # 3. 测试 HTTPS 请求
    print("📋 测试3: HTTPS HEAD 请求")
    https_results = {}
    for node in dns_results.keys():
        try:
            start = time.time()
            r = requests.head(f"https://{node}/", timeout=5)
            elapsed = time.time() - start
            https_results[node] = r.status_code
            print(f"   ✅ {node}: {r.status_code} ({elapsed:.2f}s)")
        except requests.exceptions.ConnectTimeout:
            https_results[node] = "TIMEOUT"
            print(f"   ❌ {node}: 连接超时 (这是我们遇到的问题！)")
        except requests.exceptions.ReadTimeout:
            https_results[node] = "READ_TIMEOUT"
            print(f"   ❌ {node}: 读取超时")
        except Exception as e:
            https_results[node] = str(type(e).__name__)
            print(f"   ❌ {node}: {type(e).__name__}")
    print()
    
    # 4. 对比其他地区的 CDN
    print("📋 测试4: 对比其他地区 CDN 节点")
    other_regions = [
        "instagram.fsin2-1.fna.fbcdn.net",  # 新加坡
        "instagram.fhkg2-1.fna.fbcdn.net",  # 香港
    ]
    
    for node in other_regions:
        try:
            start = time.time()
            r = requests.head(f"https://{node}/", timeout=5)
            elapsed = time.time() - start
            print(f"   ✅ {node}: {r.status_code} ({elapsed:.2f}s)")
        except Exception as e:
            print(f"   ❌ {node}: {type(e).__name__}")
    print()
    
    # 分析结果
    print("=" * 60)
    print("📊 分析结果")
    print("=" * 60)
    print()
    
    timeout_count = sum(1 for v in https_results.values() if v == "TIMEOUT")
    success_count = sum(1 for v in https_results.values() if isinstance(v, int) and v == 204)
    
    print(f"曼谷 CDN 节点测试:")
    print(f"  • DNS 解析成功: {len(dns_results)}/{len(test_nodes)}")
    print(f"  • TCP 连接成功: {sum(tcp_results.values())}/{len(tcp_results)}")
    print(f"  • HTTPS 请求成功: {success_count}/{len(https_results)}")
    print(f"  • HTTPS 请求超时: {timeout_count}/{len(https_results)}")
    print()
    
    if timeout_count > 0 and sum(tcp_results.values()) == len(tcp_results):
        print("🎯 结论:")
        print("  • DNS 解析正常 ✅")
        print("  • TCP 连接正常 ✅")
        print("  • HTTPS 请求超时 ❌")
        print()
        print("  这表明:")
        print("  1. CDN 节点存在且可达")
        print("  2. 网络层连接正常")
        print("  3. HTTPS/TLS 层有问题")
        print()
        print("  可能原因:")
        print("  • CDN 节点过载，拒绝新连接")
        print("  • TLS 握手失败或超时")
        print("  • CDN 正在维护/限流")
        print("  • 特定于 HTTPS 的防护机制")
    elif timeout_count == len(https_results):
        print("🎯 结论:")
        print("  所有曼谷 CDN 节点都超时！")
        print("  这很可能是 Instagram CDN 基础设施问题。")
    else:
        print("🎯 结论:")
        print("  CDN 节点部分正常，部分异常。")
        print("  这是不稳定的表现。")

if __name__ == "__main__":
    test_cdn_from_multiple_sources()
