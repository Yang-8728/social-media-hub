#!/usr/bin/env python3
"""
Firefox Profile 管理工具
"""
import os
import subprocess
import sys

def list_firefox_profiles():
    """列出所有 Firefox profiles"""
    if os.name == 'nt':  # Windows
        firefox_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
    else:  # Linux/Mac
        firefox_dir = os.path.join(os.path.expanduser("~"), ".mozilla", "firefox")
    
    print(f"📁 Firefox Profiles 目录: {firefox_dir}")
    print()
    
    if not os.path.exists(firefox_dir):
        print("❌ Firefox Profiles 目录不存在")
        return
    
    profiles = []
    for item in os.listdir(firefox_dir):
        profile_path = os.path.join(firefox_dir, item)
        if os.path.isdir(profile_path):
            profiles.append(item)
            cookies_path = os.path.join(profile_path, "cookies.sqlite")
            has_cookies = "✅" if os.path.exists(cookies_path) else "❌"
            print(f"{has_cookies} {item}")
            if os.path.exists(cookies_path):
                # 简单检查 cookies 文件大小
                size = os.path.getsize(cookies_path)
                print(f"    Cookies 文件大小: {size:,} bytes")
    
    return profiles

def create_firefox_profile(profile_name):
    """创建新的 Firefox profile"""
    print(f"🔧 创建新的 Firefox profile: {profile_name}")
    
    try:
        # 尝试找到 Firefox 可执行文件
        firefox_paths = [
            "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
            "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe",
            "/usr/bin/firefox",
            "/Applications/Firefox.app/Contents/MacOS/firefox"
        ]
        
        firefox_exe = None
        for path in firefox_paths:
            if os.path.exists(path):
                firefox_exe = path
                break
        
        if not firefox_exe:
            print("❌ 无法找到 Firefox 可执行文件")
            print("请确保 Firefox 已安装，或手动指定路径")
            return False
        
        # 创建新 profile
        cmd = [firefox_exe, "-CreateProfile", profile_name]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Profile '{profile_name}' 创建成功")
            print("ℹ️ 现在可以使用以下命令启动该 profile:")
            print(f"firefox -P {profile_name}")
            return True
        else:
            print(f"❌ 创建 profile 失败: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ 创建 profile 时出错: {e}")
        return False

def main():
    print("🦊 Firefox Profile 管理工具")
    print("=" * 40)
    
    print("\n📋 当前 Firefox Profiles:")
    profiles = list_firefox_profiles()
    
    print("\n" + "=" * 40)
    print("💡 使用建议:")
    print("1. 为 ai_vanvan 使用: 370tsjzy.default-release (已有 cookies)")
    print("2. 为 aigf8728 创建新 profile 或使用现有的 tmz7wi5o.default")
    print()
    print("如果要创建新 profile，可以运行:")
    print("python tools_firefox_profile.py create aigf8728_profile")
    
    # 处理命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "create" and len(sys.argv) > 2:
            profile_name = sys.argv[2]
            create_firefox_profile(profile_name)
        elif sys.argv[1] == "list":
            pass  # 已经列出了
        else:
            print("用法:")
            print("  python tools_firefox_profile.py list")
            print("  python tools_firefox_profile.py create <profile_name>")

if __name__ == "__main__":
    main()
