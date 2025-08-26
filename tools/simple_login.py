#!/usr/bin/env python3
"""
简化版Instagram登录工具 - 基于原项目的方法
"""
import os
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect
from instaloader import Instaloader

def get_cookiefile():
    """获取Firefox cookies文件路径"""
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
        "Linux": "~/.mozilla/firefox/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")

    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit("❌ No Firefox cookies.sqlite file found.")
    return cookiefiles[0]

def get_session_file_path(username: str) -> str:
    """获取session文件路径"""
    config_dir = expanduser("~/.config/instaloader")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, f"session-{username}")

def import_session(cookiefile, username):
    """从Firefox cookies导入session - 使用原项目的方法"""
    print(f"🔄 为 {username} 导入session...")
    print(f"📁 使用cookies文件: {cookiefile}")

    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )

    # 使用原项目的参数设置
    loader = Instaloader(max_connection_attempts=1)
    loader.context._session.cookies.update(cookie_data)
    loader.context.username = username  # 这是关键！

    print(f"🔐 正在验证账号: {username}")
    login_result = loader.test_login()
    
    if not login_result:
        print("❌ 登录验证失败")
        print("💡 可能原因:")
        print("   1. Firefox中未登录Instagram")
        print("   2. Firefox中登录的不是指定账号") 
        print("   3. Instagram cookies已过期")
        return False

    print(f"✅ 登录验证成功: {login_result}")
    
    # 保存session文件
    session_path = get_session_file_path(username)
    
    # 删除旧的session文件
    if os.path.exists(session_path):
        os.remove(session_path)
        print("🗑️  删除旧session文件")
    
    loader.save_session_to_file(session_path)
    print(f"💾 Session文件已保存: {session_path}")
    
    return True

def main():
    """主函数"""
    print("🎯 Instagram Session导入工具")
    print("=" * 50)
    
    try:
        cookiefile = get_cookiefile()
        
        # 为ai_vanvan账号创建session
        username = "ai_vanvan"
        success = import_session(cookiefile, username)
        
        if success:
            print(f"\n🎉 {username} session创建成功！")
            print("现在可以开始下载了！")
        else:
            print(f"\n❌ {username} session创建失败")
            print("请确认Firefox中已登录正确的Instagram账号")
            
    except Exception as e:
        print(f"❌ 处理过程出错: {e}")

if __name__ == "__main__":
    main()
