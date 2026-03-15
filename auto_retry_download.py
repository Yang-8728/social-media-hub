#!/usr/bin/env python3
"""
智能重试下载脚本
利用 CDN 节点状态波动的特点，多次重试直到成功
"""

import subprocess
import time
import json
from datetime import datetime

def run_download(account_name, max_retries=5, wait_minutes=10):
    """
    智能重试下载
    
    Args:
        account_name: 账号名称 (ai_vanvan 或 aigf8728)
        max_retries: 最多重试次数
        wait_minutes: 每次重试之间等待分钟数
    """
    
    print("=" * 60)
    print(f"🚀 智能下载器启动")
    print(f"📱 账号: {account_name}")
    print(f"🔄 最多重试: {max_retries} 次")
    print(f"⏰ 重试间隔: {wait_minutes} 分钟")
    print("=" * 60)
    print()
    
    results = []
    
    for attempt in range(1, max_retries + 1):
        print(f"\n{'='*60}")
        print(f"📥 第 {attempt}/{max_retries} 次尝试")
        print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # 运行下载命令
        cmd = f"python main.py --{account_name} --download"
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        # 解析结果
        output = result.stdout + result.stderr
        
        # 提取统计信息
        success = 0
        failed = 0
        skipped = 0
        
        for line in output.split('\n'):
            if '成功下载:' in line:
                try:
                    success = int(line.split(':')[1].split('个')[0].strip())
                except:
                    pass
            if '下载失败:' in line:
                try:
                    failed = int(line.split(':')[1].split('个')[0].strip())
                except:
                    pass
            if '跳过已有:' in line:
                try:
                    skipped = int(line.split(':')[1].split('个')[0].strip())
                except:
                    pass
        
        results.append({
            'attempt': attempt,
            'success': success,
            'failed': failed,
            'skipped': skipped,
            'time': datetime.now().isoformat()
        })
        
        print(f"\n📊 本次结果:")
        print(f"   ✅ 成功: {success}")
        print(f"   ❌ 失败: {failed}")
        print(f"   ⏭️  跳过: {skipped}")
        
        # 如果没有失败的，说明全部完成
        if failed == 0:
            print(f"\n🎉 所有视频下载完成！")
            break
        
        # 如果还没到最后一次，等待后继续
        if attempt < max_retries:
            print(f"\n⏸️  等待 {wait_minutes} 分钟后重试...")
            print(f"   原因: CDN 节点状态会变化，稍后可能成功")
            time.sleep(wait_minutes * 60)
    
    # 总结
    print(f"\n\n{'='*60}")
    print("📊 下载总结")
    print(f"{'='*60}")
    
    total_success = sum(r['success'] for r in results)
    total_failed = results[-1]['failed'] if results else 0
    total_attempts = len(results)
    
    print(f"\n总共尝试: {total_attempts} 次")
    print(f"累计成功: {total_success} 个视频")
    print(f"剩余失败: {total_failed} 个视频")
    
    if total_failed == 0:
        print(f"\n✅ 完美！所有视频都下载成功了！")
    elif total_failed < 3:
        print(f"\n👍 不错！只剩 {total_failed} 个视频失败")
        print(f"   建议: 稍后再运行一次可能就全部成功了")
    else:
        print(f"\n⚠️  还有 {total_failed} 个视频失败")
        print(f"   建议: 等待更长时间后再试，或检查网络")
    
    # 保存结果
    with open(f'download_results_{account_name}.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 详细结果已保存到: download_results_{account_name}.json")
    print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python auto_retry_download.py ai_vanvan")
        print("  python auto_retry_download.py aigf8728")
        print()
        print("可选参数:")
        print("  python auto_retry_download.py ai_vanvan 5 15")
        print("  (账号名 最多重试次数 等待分钟数)")
        sys.exit(1)
    
    account = sys.argv[1]
    max_retries = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    wait_minutes = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    run_download(account, max_retries, wait_minutes)
