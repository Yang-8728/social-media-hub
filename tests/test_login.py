#!/usr/bin/env python3
"""
测试Instagram登录功能
检查Firefox cookies登录和session文件生成
"""
import os
import sys

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.platforms.instagram.downloader import InstagramDownloader
from src.core.models import Account
from src.utils.logger import Logger


def test_login(account_name: str):
    """测试指定账号的登录功能"""
    print(f"🔑 测试 {account_name} 账号登录...")
    print("=" * 50)
    
    # 创建下载器实例
    downloader = InstagramDownloader()
    
    # 创建账号对象
    account = Account(
        name=account_name,
        platform="instagram",
        username=account_name  # 假设账号名就是用户名
    )
    
    try:
        # 测试登录
        print("🔍 检查Firefox cookies...")
        cookiefile = downloader.get_cookiefile()
        if not cookiefile:
            print("❌ 未找到Firefox cookies文件")
            print("请确保：")
            print("1. 已安装Firefox浏览器")
            print("2. 在Firefox中登录了Instagram")
            print("3. Firefox配置文件存在cookies.sqlite")
            return False
        
        print(f"✅ 找到cookies文件: {cookiefile}")
        
        # 验证登录
        print(f"🔍 验证 {account_name} 账号登录状态...")
        if downloader.validate_login(cookiefile, account_name):
            print(f"✅ {account_name} 登录验证成功!")
            
            # 尝试完整登录流程
            print("🔄 执行完整登录流程...")
            login_success = downloader.login(account)
            
            if login_success:
                print(f"🎉 {account_name} 登录成功!")
                
                # 检查session文件
                session_file = downloader.get_session_file_path(account_name)
                if os.path.exists(session_file):
                    print(f"✅ Session文件已创建: {session_file}")
                else:
                    print("⚠️ Session文件未找到")
                
                return True
            else:
                print(f"❌ {account_name} 登录失败")
                return False
        else:
            print(f"❌ {account_name} 登录验证失败")
            print("可能的原因：")
            print("1. Firefox中当前登录的不是此账号")
            print("2. Instagram session已过期")
            print("3. 网络连接问题")
            return False
            
    except Exception as e:
        print(f"❌ 登录测试出错: {e}")
        return False


def main():
    """主函数"""
    print("🚀 Instagram登录功能测试")
    print("=" * 50)
    
    # 测试两个账号
    accounts = ["ai_vanvan", "aigf8728"]
    
    results = {}
    for account in accounts:
        print(f"\n📱 测试账号: {account}")
        results[account] = test_login(account)
        print("\n" + "-" * 30)
    
    # 总结结果
    print("\n📊 测试结果总结:")
    print("=" * 50)
    for account, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        print(f"{account}: {status}")
    
    success_count = sum(results.values())
    total_count = len(results)
    print(f"\n成功: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 所有账号登录测试通过!")
    elif success_count > 0:
        print("⚠️ 部分账号登录成功")
    else:
        print("❌ 所有账号登录失败")
        print("\n建议检查:")
        print("1. Firefox是否已安装并登录Instagram")
        print("2. 网络连接是否正常")
        print("3. Instagram账号是否正常")


if __name__ == "__main__":
    main()
