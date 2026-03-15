#!/usr/bin/env python3
"""
完整流程执行脚本 (Docker版本)
通过API Gateway调用容器服务
扫描  下载  合并  上传
失败立即停止
"""
import requests
import time
import argparse
import json
import sys


API_BASE = "http://localhost:8080/api"


def print_banner(text):
    """打印横幅"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def print_step(step_num, total_steps, message):
    """打印步骤信息"""
    print(f"\n{''*70}")
    print(f"【步骤 {step_num}/{total_steps}】{message}")
    print(f"{''*70}\n")


def call_api(endpoint, data):
    """调用API"""
    try:
        url = f"{API_BASE}{endpoint}"
        print(f" 调用API: {url}")
        print(f" 参数: {json.dumps(data, ensure_ascii=False)}")
        
        response = requests.post(url, json=data, timeout=10)
        
        # 检查HTTP状态码
        if response.status_code != 200:
            print(f" HTTP错误: {response.status_code}")
            print(f"   响应内容: {response.text[:200]}")
            return None
        
        result = response.json()
        print(f" 响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return result
    except requests.exceptions.ConnectionError:
        print(f" 连接失败: 无法连接到 {API_BASE}")
        print(f"   请确保Docker容器正在运行: docker-compose up -d")
        return None
    except Exception as e:
        print(f" API调用失败: {e}")
        return None


def run_full_workflow(account: str, 
                     download_limit: int = 20,
                     merge_count: int = 15,
                     resolution: str = "1080x1920",
                     skip_upload: bool = False):
    """执行完整工作流程"""
    
    print_banner(" 开始执行完整工作流程 (Docker版本)")
    print(f"\n 配置:")
    print(f"   账户: {account}")
    print(f"   下载限制: {download_limit} 个")
    print(f"   合并数量: {merge_count} 个")
    print(f"   分辨率: {resolution}")
    print(f"   API地址: {API_BASE}")
    print(f"   跳过上传: {'是' if skip_upload else '否'}")
    
    start_time = time.time()
    task_ids = []
    
    try:
        # 步骤1: 扫描新内容
        print_step(1, 5, " 扫描新内容")
        print("  扫描会在遇到已下载视频时自动停止，避免封号风险\n")
        
        result = call_api("/scanner/scan", {
            "account": account,
            "limit": 50
        })
        
        if not result or result.get("status") != "success":
            error = result.get("error") if result else "API调用失败"
            print(f"\n 步骤1失败: {error}")
            print(" 流程终止")
            return False
        
        task_id = result.get("task_id")
        task_ids.append(("扫描", task_id))
        print(f" 扫描任务已提交: {task_id}")
        
        print("\n 等待 3 秒...")
        time.sleep(3)
        
        # 步骤2: 下载视频
        print_step(2, 5, f"  下载视频 (限制 {download_limit} 个)")
        print("开始下载新视频，智能去重...\n")
        
        result = call_api("/downloader/download", {
            "account": account,
            "max_downloads": download_limit
        })
        
        if not result or result.get("status") != "success":
            error = result.get("error") if result else "API调用失败"
            print(f"\n 步骤2失败: {error}")
            print(" 流程终止")
            return False
        
        task_id = result.get("task_id")
        task_ids.append(("下载", task_id))
        print(f" 下载任务已提交: {task_id}")
        
        print("\n 等待 5 秒...")
        time.sleep(5)
        
        # 步骤3: 标准化处理
        print_step(3, 5, f" 标准化处理 (分辨率: {resolution})")
        print("转换视频分辨率...\n")
        
        result = call_api("/standardizer/process", {
            "account": account,
            "resolution": resolution
        })
        
        if not result or result.get("status") != "success":
            error = result.get("error") if result else "API调用失败"
            print(f"\n 步骤3失败: {error}")
            print(" 流程终止")
            return False
        
        task_id = result.get("task_id")
        task_ids.append(("标准化", task_id))
        print(f" 标准化任务已提交: {task_id}")
        
        print("\n 等待 5 秒...")
        time.sleep(5)
        
        # 步骤4: 合并视频
        print_step(4, 5, f" 合并视频 (数量: {merge_count})")
        print("合并多个视频...\n")
        
        result = call_api("/merger/merge", {
            "account": account,
            "limit": merge_count
        })
        
        if not result or result.get("status") != "success":
            error = result.get("error") if result else "API调用失败"
            print(f"\n 步骤4失败: {error}")
            print(" 流程终止")
            return False
        
        task_id = result.get("task_id")
        task_ids.append(("合并", task_id))
        print(f" 合并任务已提交: {task_id}")
        
        print("\n 等待 5 秒...")
        time.sleep(5)
        
        # 步骤5: 上传B站
        if not skip_upload:
            print_step(5, 5, "  上传到B站")
            
            confirm = input("  确定要上传视频到B站吗？(y/N): ").strip().lower()
            if confirm == 'y':
                result = call_api("/uploader/upload", {
                    "account": account,
                    "video_path": None
                })
                
                if not result or result.get("status") != "success":
                    error = result.get("error") if result else "API调用失败"
                    print(f"\n 步骤5失败: {error}")
                    print(" 流程终止")
                    return False
                
                task_id = result.get("task_id")
                task_ids.append(("上传", task_id))
                print(f" 上传任务已提交: {task_id}")
            else:
                print("  跳过上传步骤")
        else:
            print_step(5, 5, "  跳过上传步骤")
        
        # 完成
        elapsed = time.time() - start_time
        print_banner(f" 完整流程执行完成！耗时: {elapsed:.1f} 秒")
        
        # 显示所有任务ID
        if task_ids:
            print("\n 已提交的任务:")
            for name, task_id in task_ids:
                print(f"   {name}: {task_id}")
        
        print("\n 提示: 任务正在后台处理中，可以通过以下命令查看日志:")
        print(f"   docker logs social-media-hub-scanner-1 -f")
        print(f"   docker logs social-media-hub-downloader-1 -f")
        print(f"   docker logs social-media-hub-merger-1 -f")
        print(f"   docker logs social-media-hub-uploader-1 -f")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n  用户中断执行")
        return False
    except Exception as e:
        print(f"\n 流程执行出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="执行完整的视频处理流程 (Docker版本 - 调用API Gateway)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run_full_workflow.py ai_vanvan                    # 使用默认参数
  python run_full_workflow.py ai_vanvan -d 20 -m 15        # 下载20个，合并15个
  python run_full_workflow.py aigf8728 -r 720x1280         # 使用720p分辨率
  python run_full_workflow.py ai_vanvan --skip-upload      # 跳过上传

注意: 需要确保Docker容器正在运行 (docker-compose up -d)
        """
    )
    parser.add_argument("account", help="账户名称 (ai_vanvan 或 aigf8728)")
    parser.add_argument("-d", "--download", type=int, default=20, 
                       help="下载视频数量 (默认: 20)")
    parser.add_argument("-m", "--merge", type=int, default=15, 
                       help="合并视频数量 (默认: 15)")
    parser.add_argument("-r", "--resolution", default="1080x1920",
                       choices=["720x1280", "1080x1920"],
                       help="目标分辨率 (默认: 1080x1920)")
    parser.add_argument("--skip-upload", action="store_true",
                       help="跳过上传步骤")
    
    args = parser.parse_args()
    
    success = run_full_workflow(
        account=args.account,
        download_limit=args.download,
        merge_count=args.merge,
        resolution=args.resolution,
        skip_upload=args.skip_upload
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
