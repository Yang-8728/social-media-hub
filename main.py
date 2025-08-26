"""
Social Media Hub - 主程序
企业级社交媒体内容管理系统
"""
import argparse
import os
import json

from src.core.models import Account
from src.platforms.instagram.downloader import InstagramDownloader
from src.utils.logger import Logger
from src.utils.video_merger import VideoMerger
from src.utils.folder_manager import FolderManager


def load_account_config() -> dict:
    """加载账号配置"""
    config_file = "config/accounts.json"
    
    if not os.path.exists(config_file):
        print(f"❌ 配置文件不存在: {config_file}")
        return {}
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
        # 支持新旧格式的配置文件
        if "accounts" in config_data:
            return config_data["accounts"]
        return config_data


def create_account_from_config(account_name: str, config: dict) -> Account:
    """从配置创建账号对象"""
    account_config = config.get(account_name, {})
    
    # 支持新旧格式
    if "instagram" in account_config:
        username = account_config["instagram"].get("username", "")
    else:
        username = account_config.get("username", "")
    
    account = Account(
        name=account_name,
        platform="instagram",
        username=username
    )
    
    # 添加完整配置到账号对象
    account.config = account_config
    
    return account


def run_download(account_name: str, limit: int):
    """运行下载任务"""
    # 不在这里显示开始信息，让下载器自己处理
    
    # 加载配置
    config = load_account_config()
    if not config:
        return
    
    # 创建账号
    account = create_account_from_config(account_name, config)
    if not account.username:
        print(f"❌ 账号配置不完整: {account_name}")
        return
    
    # 初始化下载器
    downloader = InstagramDownloader()
    
    # 登录
    if not downloader.login(account):
        print(f"❌ 登录失败: {account.username}")
        return
    
    # 下载内容
    results = downloader.download_posts(account, limit)
    
    for result in results:
        if result.success:
            print(f"✅ 下载成功: {result.message}")
        else:
            print(f"❌ 下载失败: {result.error}")


def run_merge(account_name: str, limit: int = None):
    """运行视频合并任务"""
    if limit:
        print(f"🔄 开始合并任务: {account_name} (限制: {limit} 个)")
    else:
        print(f"🔄 开始合并任务: {account_name}")
    
    # 初始化合并器
    merger = VideoMerger(account_name)
    
    # 合并指定数量的未合并视频
    result = merger.merge_unmerged_videos(limit=limit)
    
    print(f"✅ 合并完成 - 成功: {result['merged']}, 跳过: {result['skipped']}, 失败: {result['failed']}")


def show_folders(account_name: str = None):
    """显示文件夹信息"""
    if account_name:
        accounts = [account_name]
    else:
        config = load_account_config()
        accounts = list(config.keys())
    
    print("📁 文件夹信息:")
    print("-" * 60)
    
    for acc in accounts:
        config = load_account_config()
        account_config = config.get(acc, {})
        
        folder_manager = FolderManager(acc, account_config)
        folder_info = folder_manager.get_folder_info()
        
        print(f"\n📱 账号: {acc}")
        print(f"   策略: {folder_info['strategy']}")
        print(f"   下载基础目录: {folder_info['base_download_dir']}")
        print(f"   合并基础目录: {folder_info['base_merged_dir']}")
        print(f"   下载文件夹数量: {folder_info['total_download_folders']}")
        print(f"   合并文件夹数量: {folder_info['total_merged_folders']}")
        
        # 显示最近的文件夹
        if folder_info['download_folders']:
            print(f"   最近的下载文件夹:")
            for folder in folder_info['download_folders'][:3]:
                print(f"     - {folder['name']} ({folder['files_count']} 文件)")
        
        if folder_info['merged_folders']:
            print(f"   最近的合并文件夹:")
            for folder in folder_info['merged_folders'][:3]:
                print(f"     - {folder['name']} ({folder['files_count']} 文件)")


def search_blogger(account_name: str, blogger_name: str):
    """搜索博主文件夹"""
    print(f"🔍 搜索博主: {blogger_name} (账号: {account_name})")
    print("-" * 50)
    
    config = load_account_config()
    account_config = config.get(account_name, {})
    
    folder_manager = FolderManager(account_name, account_config)
    matches = folder_manager.search_blogger_folders(blogger_name)
    
    if not matches:
        print(f"❌ 未找到包含 '{blogger_name}' 的文件夹")
        return
    
    print(f"✅ 找到 {len(matches)} 个匹配的文件夹:")
    
    for match in matches:
        print(f"📁 {match['name']} ({match['type']})")
        print(f"   路径: {match['path']}")
        print(f"   文件数: {match['files_count']}")
        print(f"   创建时间: {match['created']}")
        print()


def show_status(account_name: str = None):
    """显示状态信息"""
    if account_name:
        accounts = [account_name]
    else:
        config = load_account_config()
        accounts = list(config.keys())
    
    print("📊 系统状态:")
    print("-" * 50)
    
    for acc in accounts:
        logger = Logger(acc)
        summary = logger.get_download_summary()
        unmerged = logger.get_unmerged_downloads()
        
        print(f"\n📱 账号: {acc}")
        print(f"   总下载: {summary.get('total', 0)} 个")
        print(f"   成功: {summary.get('success', 0)} 个")
        print(f"   失败: {summary.get('failed', 0)} 个")
        print(f"   跳过: {summary.get('skipped', 0)} 个")
        print(f"   待合并: {len(unmerged)} 个")
        
        if unmerged:
            print(f"   未合并列表: {', '.join([u['shortcode'] for u in unmerged[:5]])}")
            if len(unmerged) > 5:
                print(f"                及其他 {len(unmerged) - 5} 个...")
        
        # 显示文件夹信息
        config = load_account_config()
        account_config = config.get(acc, {})
        folder_manager = FolderManager(acc, account_config)
        folder_info = folder_manager.get_folder_info()
        print(f"   下载文件夹: {folder_info['total_download_folders']} 个")
        print(f"   合并文件夹: {folder_info['total_merged_folders']} 个")


def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(description="Social Media Hub - 企业级社交媒体内容管理")
    
    # 命令参数
    parser.add_argument("--download", action="store_true", help="下载内容")
    parser.add_argument("--merge", action="store_true", help="合并视频")
    parser.add_argument("--status", action="store_true", help="显示状态")
    parser.add_argument("--folders", action="store_true", help="显示文件夹信息")
    parser.add_argument("--search", type=str, help="搜索博主文件夹")
    parser.add_argument("--stats", action="store_true", help="显示详细统计")
    parser.add_argument("--clean", action="store_true", help="清理空文件夹")
    parser.add_argument("--backup", action="store_true", help="备份日志文件")
    
    # 账号参数
    parser.add_argument("--ai_vanvan", action="store_true", help="使用 ai_vanvan 账号 (搞笑)")
    parser.add_argument("--aigf8728", action="store_true", help="使用 aigf8728 账号")
    parser.add_argument("--account", type=str, help="指定账号名称")
    
    # 其他参数
    parser.add_argument("--limit", type=int, default=50, help="下载数量限制")
    parser.add_argument("--merge-limit", type=int, help="合并视频数量限制")
    parser.add_argument("--all", action="store_true", help="处理所有账号")
    
    args = parser.parse_args()
    
    # 确定账号
    account_name = None
    if args.ai_vanvan:
        account_name = "ai_vanvan"
    elif args.aigf8728:
        account_name = "aigf8728"
    elif args.account:
        account_name = args.account
    
    # 执行命令
    if args.download:
        if account_name:
            run_download(account_name, args.limit)
        elif args.all:
            config = load_account_config()
            for acc in config.keys():
                run_download(acc, args.limit)
        else:
            print("❌ 请指定账号 (--ai_vanvan, --aigf8728, --account <name>, 或 --all)")
    
    elif args.merge:
        if account_name:
            run_merge(account_name, limit=args.merge_limit)
        elif args.all:
            config = load_account_config()
            for acc in config.keys():
                run_merge(acc, limit=args.merge_limit)
        else:
            print("❌ 请指定账号 (--ai_vanvan, --aigf8728, --account <name>, 或 --all)")
    
    elif args.status:
        show_status(account_name)
    
    elif args.folders:
        show_folders(account_name)
    
    elif args.search:
        if account_name:
            search_blogger(account_name, args.search)
        else:
            print("❌ 搜索博主时请指定账号 (--ai_vanvan, --aigf8728, 或 --account <name>)")
    
    else:
        # 默认显示帮助
        parser.print_help()
        print("\n💡 常用命令示例:")
        print("   python main.py --download --ai_vanvan --limit 5     # 下载 ai_vanvan 的 5 个内容")
        print("   python main.py --merge --ai_vanvan                  # 合并 ai_vanvan 的视频")
        print("   python main.py --status                          # 查看所有账号状态")
        print("   python main.py --folders --ai_vanvan                # 查看 ai_vanvan 文件夹")
        print("   python main.py --search 博主名 --aigf8728            # 搜索 aigf8728 中的博主文件夹")
        print("   python main.py --download --all --limit 3        # 下载所有账号各 3 个内容")


if __name__ == "__main__":
    main()
