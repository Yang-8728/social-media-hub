"""
测试完整容器化流程
ai_vanvan 账号：下载 → 标准化 → 合并
"""
import requests
import time
import json

API_BASE = "http://localhost:8080"
ACCOUNT = "ai_vanvan"

def test_download():
    """步骤1: 测试下载服务"""
    print("=" * 60)
    print("📥 步骤 1/3: 下载最新内容")
    print("=" * 60)
    
    url = f"{API_BASE}/download"
    payload = {
        "account": ACCOUNT,
        "limit": 5
    }
    
    print(f"🔗 请求: POST {url}")
    print(f"📦 参数: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=300)
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 下载响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 获取任务ID（如果是异步的话）
            task_id = result.get('task_id')
            if task_id:
                print(f"📋 任务ID: {task_id}")
                return task_id, True
            else:
                # 直接返回结果
                message = result.get('message', '')
                if '没有新视频' in message or '成功' in message:
                    print("✅ 下载完成（没有新视频或已完成）")
                    return None, True
                return None, True
        else:
            print(f"❌ 下载失败: {response.text}")
            return None, False
            
    except Exception as e:
        print(f"❌ 下载请求失败: {e}")
        return None, False


def test_standardize():
    """步骤2: 测试标准化服务"""
    print("\n" + "=" * 60)
    print("🔧 步骤 2/3: 标准化视频")
    print("=" * 60)
    
    # 注意：在当前架构中，标准化是在合并时自动完成的
    # 这里我们跳过独立的标准化步骤
    print("ℹ️  标准化会在合并步骤中自动完成")
    print("✅ 跳过独立标准化步骤")
    return True


def wait_for_standardize(task_id, max_wait=300):
    """等待标准化完成"""
    url = f"{API_BASE}/standardize/status/{task_id}"
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                result = response.json()
                status = result.get('status')
                progress = result.get('progress', {})
                
                print(f"📊 状态: {status}, 进度: {progress.get('completed', 0)}/{progress.get('total', 0)}")
                
                if status == 'completed':
                    print(f"✅ 标准化完成！")
                    return True
                elif status == 'failed':
                    print(f"❌ 标准化失败: {result.get('error')}")
                    return False
            
            time.sleep(5)
        except Exception as e:
            print(f"⚠️  查询状态失败: {e}")
            time.sleep(5)
    
    print(f"⏰ 等待超时")
    return False


def test_merge():
    """步骤3: 测试合并服务"""
    print("\n" + "=" * 60)
    print("🔗 步骤 3/3: 合并视频")
    print("=" * 60)
    
    # 先查询合并状态
    status_url = f"{API_BASE}/merge/status/{ACCOUNT}"
    
    print(f"🔗 查询合并状态: GET {status_url}")
    
    try:
        response = requests.get(status_url, timeout=30)
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            unmerged = result.get('unmerged_count', 0)
            
            print(f"📋 未合并视频数: {unmerged}")
            
            if unmerged == 0:
                print("ℹ️  没有需要合并的视频")
                return True
            
            # 开始合并
            print(f"\n🚀 开始合并处理...")
            merge_url = f"{API_BASE}/merge"
            merge_payload = {
                "account": ACCOUNT,
                "limit": None  # 合并所有未合并的视频
            }
            
            merge_response = requests.post(merge_url, json=merge_payload, timeout=600)
            print(f"📊 合并状态码: {merge_response.status_code}")
            
            if merge_response.status_code == 200:
                merge_result = merge_response.json()
                print(f"✅ 合并响应: {json.dumps(merge_result, indent=2, ensure_ascii=False)}")
                
                # 检查合并结果
                if merge_result.get('status') == 'success':
                    merged_count = merge_result.get('merged_count', 0)
                    output_file = merge_result.get('output_file', '')
                    print(f"✅ 成功合并 {merged_count} 个视频")
                    print(f"📁 输出文件: {output_file}")
                    return True
                else:
                    print(f"⚠️  合并未完成: {merge_result.get('message')}")
                    return merge_result.get('merged_count', 0) > 0
            else:
                print(f"❌ 合并失败: {merge_response.text}")
                return False
        else:
            print(f"❌ 查询状态失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 合并请求失败: {e}")
        return False


def main():
    """运行完整流程"""
    print("🚀 开始测试 ai_vanvan 完整容器化流程")
    print("="*60)
    print(f"📱 账号: {ACCOUNT}")
    print(f"🌐 API地址: {API_BASE}")
    print()
    
    # 检查服务是否在线
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API Gateway 在线")
        else:
            print("⚠️  API Gateway 状态异常")
    except Exception as e:
        print(f"❌ 无法连接到 API Gateway: {e}")
        print("💡 请确保服务已启动: docker-compose up -d")
        return
    
    print()
    
    # 步骤1: 下载
    task_id, success = test_download()
    if not success:
        print("\n❌ 下载步骤失败，停止流程")
        return
    
    # 如果下载是异步的，等待一下
    if task_id:
        print("⏳ 等待下载完成...")
        time.sleep(10)
    
    # 步骤2: 标准化
    success = test_standardize()
    if not success:
        print("\n❌ 标准化步骤失败，停止流程")
        return
    
    # 步骤3: 合并
    success = test_merge()
    if not success:
        print("\n⚠️  合并步骤未完全成功")
    
    print("\n" + "="*60)
    print("✅ 完整流程测试结束")
    print("="*60)


if __name__ == "__main__":
    main()
