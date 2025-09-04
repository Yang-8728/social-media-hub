#!/usr/bin/env python3
"""
Firefox Profile 创建工具
为不同的 Instagram 账户创建独立的 Firefox profile
"""

import subprocess
import os
import sys
import time
from pathlib import Path

def find_firefox_executable():
    """查找 Firefox 可执行文件"""
    common_paths = [
        r"C:\Program Files\Mozilla Firefox\firefox.exe",
        r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
        os.path.join(os.path.expanduser("~"), "AppData", "Local", "Mozilla Firefox", "firefox.exe")
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    print("❌ 未找到 Firefox 可执行文件")
    return None

def list_existing_profiles():
    """列出现有的 Firefox profiles"""
    profiles_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
    
    if not os.path.exists(profiles_dir):
        print("❌ Firefox Profiles 目录不存在")
        return []
    
    profiles = []
    for item in os.listdir(profiles_dir):
        profile_path = os.path.join(profiles_dir, item)
        if os.path.isdir(profile_path):
            profiles.append(item)
    
    return profiles

def create_firefox_profile(profile_name):
    """创建新的 Firefox profile"""
    firefox_exe = find_firefox_executable()
    if not firefox_exe:
        return False
    
    print(f"🔧 正在创建 Firefox profile: {profile_name}")
    
    try:
        # 使用 -CreateProfile 参数创建新 profile
        cmd = [firefox_exe, "-CreateProfile", profile_name]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ Profile 创建成功: {profile_name}")
            return True
        else:
            print(f"❌ Profile 创建失败: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 创建 profile 超时")
        return False
    except Exception as e:
        print(f"❌ 创建 profile 出错: {e}")
        return False

def launch_firefox_with_profile(profile_name):
    """使用指定 profile 启动 Firefox"""
    firefox_exe = find_firefox_executable()
    if not firefox_exe:
        return False
    
    print(f"🚀 正在启动 Firefox (Profile: {profile_name})")
    print("请在新打开的 Firefox 窗口中登录 Instagram 账户")
    print("登录完成后关闭 Firefox 窗口，然后按任意键继续...")
    
    try:
        # 使用 -P 参数启动指定 profile
        cmd = [firefox_exe, "-P", profile_name, "--no-remote"]
        subprocess.Popen(cmd)
        
        # 等待用户确认
        input("\n按回车键继续...")
        return True
        
    except Exception as e:
        print(f"❌ 启动 Firefox 出错: {e}")
        return False

def main():
    print("🦊 Firefox Profile 管理工具")
    print("=" * 50)
    
    # 显示现有 profiles
    print("\n📋 现有 Firefox Profiles:")
    existing_profiles = list_existing_profiles()
    if existing_profiles:
        for i, profile in enumerate(existing_profiles, 1):
            print(f"  {i}. {profile}")
    else:
        print("  (无)")
    
    print("\n🎯 建议为每个 Instagram 账户创建独立的 profile:")
    print("  • ai_vanvan -> 使用现有 profile (370tsjzy.default-release)")
    print("  • aigf8728 -> 创建新 profile")
    
    # 为 aigf8728 创建新 profile
    profile_name = "aigf8728_instagram"
    
    print(f"\n🔧 将为 aigf8728 账户创建新 profile: {profile_name}")
    
    if input("继续? (y/N): ").lower() == 'y':
        # 创建 profile
        if create_firefox_profile(profile_name):
            # 启动 Firefox 让用户登录
            if launch_firefox_with_profile(profile_name):
                print(f"\n✅ Profile 设置完成！")
                print(f"现在可以在 accounts.json 中使用: \"{profile_name}\"")
            
        # 再次显示所有 profiles
        print("\n📋 更新后的 Profiles:")
        updated_profiles = list_existing_profiles()
        for i, profile in enumerate(updated_profiles, 1):
            print(f"  {i}. {profile}")

if __name__ == "__main__":
    main()
