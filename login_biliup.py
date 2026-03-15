"""
B站登录工具 - 获取Cookie用于云端上传
"""
import subprocess
import sys
from pathlib import Path

def check_biliup():
    try:
        result = subprocess.run(["biliup", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f" biliup: {result.stdout.strip()}")
            return True
    except:
        pass
    
    print(" 未找到biliup")
    print("\n 下载地址:")
    print("   https://github.com/biliup/biliup-rs/releases/latest")
    print("   文件: biliup-x86_64-pc-windows-msvc.zip")
    return False

def login(account="ai_vanvan"):
    if not check_biliup():
        return
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    cookie_file = config_dir / f"{account}.json"
    
    print("\n" + "="*60)
    print(f" B站登录 - {account}")
    print("="*60)
    print(f"Cookie保存至: {cookie_file}\n")
    
    cmd = ["biliup", "-u", str(cookie_file), "login"]
    
    try:
        result = subprocess.run(cmd)
        if result.returncode == 0:
            print(f"\n 登录成功!")
            print(f" Cookie: {cookie_file}")
            print("\n 同步到容器:")
            print(f"   docker cp {cookie_file} <container>:/app/cookies/")
    except KeyboardInterrupt:
        print("\n 已取消")

if __name__ == "__main__":
    account = sys.argv[1] if len(sys.argv) > 1 else "ai_vanvan"
    login(account)
