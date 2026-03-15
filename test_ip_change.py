#!/usr/bin/env python3
"""
测试换 IP 后的下载效果
用于验证是否是 IP 封禁问题
"""

import requests
import time

def test_with_current_ip():
    """测试当前 IP 的情况"""
    print("=" * 60)
    print("🔍 测试当前 IP 访问 Instagram CDN")
    print("=" * 60)
    print()
    
    # 获取当前 IP
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text
        print(f"📍 当前公网 IP: {ip}")
    except:
        print("❌ 无法获取当前 IP")
        ip = "未知"
    print()
    
    # 测试多个 CDN 节点
    cdn_nodes = [
        "instagram.fbkk29-1.fna.fbcdn.net",
        "instagram.fbkk29-2.fna.fbcdn.net",
        "instagram.fbkk29-4.fna.fbcdn.net",
        "instagram.fbkk29-6.fna.fbcdn.net",
        "instagram.fbkk29-8.fna.fbcdn.net",
        "instagram.fbkk29-9.fna.fbcdn.net",
    ]
    
    print("📊 测试结果:")
    success_count = 0
    timeout_count = 0
    
    for node in cdn_nodes:
        try:
            start = time.time()
            r = requests.head(f"https://{node}/", timeout=5)
            elapsed = time.time() - start
            print(f"   ✅ {node}: {r.status_code} ({elapsed:.2f}s)")
            success_count += 1
        except requests.exceptions.ConnectTimeout:
            print(f"   ❌ {node}: 连接超时")
            timeout_count += 1
        except Exception as e:
            print(f"   ❌ {node}: {type(e).__name__}")
            timeout_count += 1
    
    print()
    print(f"成功: {success_count}/{len(cdn_nodes)} ({success_count/len(cdn_nodes)*100:.0f}%)")
    print(f"失败: {timeout_count}/{len(cdn_nodes)} ({timeout_count/len(cdn_nodes)*100:.0f}%)")
    print()
    
    return {
        'ip': ip,
        'success': success_count,
        'timeout': timeout_count,
        'total': len(cdn_nodes),
        'success_rate': success_count/len(cdn_nodes)
    }

if __name__ == "__main__":
    print()
    print("📝 使用说明:")
    print("1. 先运行此脚本记录当前结果")
    print("2. 连接 VPN 或更换网络")
    print("3. 再次运行脚本对比结果")
    print()
    print("如果换 IP 后成功率显著提升 → IP 封禁")
    print("如果换 IP 后成功率不变 → CDN 节点问题")
    print()
    
    result = test_with_current_ip()
    
    print("=" * 60)
    print("💾 保存此结果用于对比")
    print("=" * 60)
    print()
    print(f"IP: {result['ip']}")
    print(f"成功率: {result['success_rate']*100:.0f}%")
    print()
    
    # 保存结果
    import json
    from datetime import datetime
    
    result['timestamp'] = datetime.now().isoformat()
    
    with open('ip_test_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("✅ 结果已保存到 ip_test_result.json")
    print()
    print("下一步:")
    print("1. 连接 VPN 或更换网络")
    print("2. 再次运行: python test_ip_change.py")
    print("3. 对比两次结果")
