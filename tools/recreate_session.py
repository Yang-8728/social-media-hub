#!/usr/bin/env python3
"""
从Firefox重新创建Instagram session
"""
import os
import sys
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect

def get_cookiefile():
    """获取Firefox cookies文件路径"""
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite", 
        "Linux": "~/.mozilla/firefox/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")

    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit("❌ 未找到Firefox cookies文件")
    return cookiefiles[0]

def recreate_session():
    """重新创建session"""
    print("🔄 从Firefox重新创建Instagram session...")
    
    # 获取Firefox cookies
    cookiefile = get_cookiefile()
    print(f"📁 使用cookies文件: {cookiefile}")
    
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
        print("❌ 未找到Instagram cookies")
        return False
    
    print(f"✅ 找到 {len(cookie_data)} 个Instagram cookies")
    
    # 创建Instaloader实例
    from instaloader import Instaloader
    loader = Instaloader(max_connection_attempts=3)
    loader.context._session.cookies.update({name: value for name, value in cookie_data})
    
    # 获取当前登录用户
    try:
        current_user = loader.test_login()
        if not current_user:
            print("❌ 无法确定当前登录用户")
            return False
            
        print(f"🔐 当前登录用户: {current_user}")
        
        # 删除旧的session文件
        session_file = expanduser(f"~/.config/instaloader/session-{current_user}")
        if os.path.exists(session_file):
            os.remove(session_file)
            print(f"🗑️  删除旧session文件")
        
        # 保存新的session
        os.makedirs(os.path.dirname(session_file), exist_ok=True)
        loader.save_session_to_file(session_file)
        print(f"✅ 成功创建新session: {session_file}")
        
        # 验证新session
        test_loader = Instaloader(max_connection_attempts=1)
        test_loader.load_session_from_file(current_user, session_file)
        test_result = test_loader.test_login()
        
        if test_result == current_user:
            print(f"✅ session验证成功: {current_user}")
            return current_user
        else:
            print(f"❌ session验证失败")
            return False
            
    except Exception as e:
        print(f"❌ 创建session过程出错: {e}")
        return False

if __name__ == "__main__":
    result = recreate_session()
    if result:
        print(f"\n🎉 session创建成功！现在可以使用 {result} 账号进行下载了。")
    else:
        print("\n❌ session创建失败，请检查Firefox登录状态。")
