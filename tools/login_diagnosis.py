#!/usr/bin/env python3
"""
Instagram登录诊断工具
"""
import os
import sys
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def get_cookiefile():
    """获取Firefox cookies文件路径"""
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite", 
        "Linux": "~/.mozilla/firefox/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")

    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        print("❌ 未找到Firefox cookies文件")
        return None
    return cookiefiles[0]

def check_firefox_login():
    """检查Firefox中的Instagram登录状态"""
    print("🔍 检查Firefox中的Instagram登录状态...")
    
    cookiefile = get_cookiefile()
    if not cookiefile:
        return None
        
    print(f"📁 Firefox cookies文件: {cookiefile}")
    
    try:
        conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
        try:
            cookie_data = conn.execute(
                "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
            ).fetchall()
        except OperationalError:
            cookie_data = conn.execute(
                "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
            ).fetchall()
        
        if not cookie_data:
            print("❌ Firefox中未找到Instagram cookies")
            return None
            
        print(f"✅ 找到 {len(cookie_data)} 个Instagram cookies")
        
        # 尝试获取当前登录的用户名
        from instaloader import Instaloader
        loader = Instaloader(max_connection_attempts=1)
        loader.context._session.cookies.update({name: value for name, value in cookie_data})
        
        try:
            current_user = loader.test_login()
            print(f"🔐 Firefox中当前登录用户: {current_user}")
            return current_user
        except Exception as e:
            print(f"❌ 无法验证Firefox登录状态: {e}")
            return None
            
    except Exception as e:
        print(f"❌ 读取Firefox cookies失败: {e}")
        return None

def check_session_files():
    """检查现有的session文件"""
    print("\n📁 检查session文件...")
    
    session_dir = expanduser("~/.config/instaloader")
    if not os.path.exists(session_dir):
        print("❌ session目录不存在")
        return {}
        
    session_files = glob(os.path.join(session_dir, "session-*"))
    if not session_files:
        print("❌ 未找到任何session文件")
        return {}
        
    sessions = {}
    for session_file in session_files:
        username = os.path.basename(session_file).replace("session-", "")
        sessions[username] = session_file
        print(f"📄 找到session: {username}")
        
    return sessions

def test_session_validity(username):
    """测试session文件的有效性"""
    print(f"\n🔐 测试 {username} 的session有效性...")
    
    try:
        from instaloader import Instaloader
        loader = Instaloader(max_connection_attempts=1)
        
        session_file = expanduser(f"~/.config/instaloader/session-{username}")
        if not os.path.exists(session_file):
            print(f"❌ session文件不存在: {session_file}")
            return False
            
        loader.load_session_from_file(username, session_file)
        test_result = loader.test_login()
        
        if test_result == username:
            print(f"✅ {username} session有效")
            return True
        else:
            print(f"❌ {username} session无效，当前登录用户: {test_result}")
            return False
            
    except Exception as e:
        print(f"❌ 测试session失败: {e}")
        return False

def create_session_from_firefox(username):
    """从Firefox cookies创建新的session"""
    print(f"\n🔄 为 {username} 创建新的session...")
    
    cookiefile = get_cookiefile()
    if not cookiefile:
        return False
        
    try:
        conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
        try:
            cookie_data = conn.execute(
                "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
            ).fetchall()
        except OperationalError:
            cookie_data = conn.execute(
                "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
            ).fetchall()
        
        from instaloader import Instaloader
        loader = Instaloader(max_connection_attempts=1)
        loader.context._session.cookies.update({name: value for name, value in cookie_data})
        
        # 验证登录用户
        current_user = loader.test_login()
        if current_user != username:
            print(f"❌ Firefox中登录的用户是 {current_user}，不是 {username}")
            return False
            
        # 保存session
        session_file = expanduser(f"~/.config/instaloader/session-{username}")
        os.makedirs(os.path.dirname(session_file), exist_ok=True)
        loader.save_session_to_file(session_file)
        
        print(f"✅ 成功为 {username} 创建session文件")
        return True
        
    except Exception as e:
        print(f"❌ 创建session失败: {e}")
        return False

def main():
    """主诊断流程"""
    print("🔧 Instagram登录诊断工具")
    print("=" * 50)
    
    # 1. 检查Firefox登录状态
    firefox_user = check_firefox_login()
    
    # 2. 检查现有session文件
    sessions = check_session_files()
    
    # 3. 测试目标账号
    target_accounts = ["ai_vanvan", "aigf8728"]
    
    print(f"\n🎯 目标账号: {target_accounts}")
    print("=" * 50)
    
    for account in target_accounts:
        print(f"\n📱 处理账号: {account}")
        print("-" * 30)
        
        # 检查session是否存在且有效
        if account in sessions:
            if test_session_validity(account):
                print(f"✅ {account} 已准备就绪")
                continue
        
        # 如果Firefox用户匹配，创建新session
        if firefox_user == account:
            if create_session_from_firefox(account):
                print(f"✅ {account} session已创建")
            else:
                print(f"❌ {account} session创建失败")
        else:
            print(f"⚠️  Firefox中登录的是 {firefox_user}，需要 {account}")
            print(f"   请在Firefox中切换到 {account} 账号")
    
    print("\n" + "=" * 50)
    print("📊 诊断完成")
    
    if firefox_user:
        print(f"🔐 Firefox当前登录: {firefox_user}")
        print("💡 建议: 确保Firefox中登录的是你要下载的账号")
    else:
        print("❌ Firefox未登录Instagram或cookies无效")
        print("💡 建议: 请先在Firefox中登录Instagram")

if __name__ == "__main__":
    main()
