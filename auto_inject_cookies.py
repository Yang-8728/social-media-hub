"""
无需关闭 Chrome 即可提取 B站 Cookies 并注入到 Docker
"""
import sqlite3
import shutil
import os
import time
from pathlib import Path

def get_chrome_cookies_db():
    """获取 Chrome Cookies 数据库路径"""
    local_appdata = os.environ.get('LOCALAPPDATA')
    profiles = ['Default', 'Profile 1', 'Profile 2']
    
    for profile in profiles:
        cookies_path = Path(local_appdata) / 'Google' / 'Chrome' / 'User Data' / profile / 'Network' / 'Cookies'
        if cookies_path.exists():
            print(f"✅ 找到 Chrome Profile: {profile}")
            return str(cookies_path)
    return None

def extract_bilibili_cookies_safe(chrome_cookies_db):
    """安全提取 B站 Cookies（Chrome 运行时也可以）"""
    temp_db = 'temp_chrome_cookies.db'
    
    # 尝试多次复制（Chrome 可能正在使用）
    for attempt in range(3):
        try:
            # 使用 Windows 的 copy 命令（可以复制正在使用的文件）
            os.system(f'copy /Y "{chrome_cookies_db}" "{temp_db}" >nul 2>&1')
            
            if os.path.exists(temp_db):
                break
        except:
            time.sleep(0.5)
    
    if not os.path.exists(temp_db):
        print("❌ 无法复制 Cookies 文件")
        return None
    
    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # 提取 B站 Cookies
        cursor.execute("""
            SELECT name, value, host_key, path, expires_utc, is_secure, is_httponly, 
                   COALESCE(samesite, 0) as samesite
            FROM cookies 
            WHERE host_key LIKE '%bilibili%'
        """)
        
        cookies = cursor.fetchall()
        conn.close()
        
        # 删除临时文件
        try:
            os.remove(temp_db)
        except:
            pass
        
        print(f"\n✅ 找到 {len(cookies)} 个 B站 Cookie")
        
        # 检查关键 Cookie
        cookie_names = [c[0] for c in cookies]
        if 'SESSDATA' in cookie_names:
            print("  🔑 SESSDATA - 已找到")
        if 'bili_jct' in cookie_names:
            print("  🔑 bili_jct - 已找到")
        if 'DedeUserID' in cookie_names:
            print("  🔑 DedeUserID - 已找到")
        
        if 'SESSDATA' not in cookie_names:
            print("\n❌ 未找到 SESSDATA！请先在 Chrome 登录 B站")
            return None
        
        return cookies
        
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        try:
            os.remove(temp_db)
        except:
            pass
        return None

def inject_to_docker_profile(cookies):
    """注入到临时文件，然后复制到 Docker"""
    # 先创建临时 Profile
    temp_profile = Path('temp_docker_profile/Default/Network')
    temp_profile.mkdir(parents=True, exist_ok=True)
    
    temp_cookies_db = temp_profile / 'Cookies'
    
    # 从容器复制原始 Cookies 数据库
    print("  📥 从容器复制原始 Cookies 数据库...")
    os.system(f'docker cp social-media-hub-uploader-1:/app/chrome/profiles/chrome_profile_ai_vanvan/Default/Network/Cookies {temp_cookies_db} >nul 2>&1')
    
    if not temp_cookies_db.exists():
        print(f"❌ 无法从容器复制 Cookies 数据库")
        return False
    
    try:
        conn = sqlite3.connect(str(temp_cookies_db))
        cursor = conn.cursor()
        
        # 删除旧的 B站 Cookie
        cursor.execute("DELETE FROM cookies WHERE host_key LIKE '%bilibili%'")
        print(f"  🗑️  清理旧 Cookie...")
        
        # 注入新 Cookie
        success = 0
        for cookie in cookies:
            try:
                # 计算 top_frame_site_key (从 host_key 派生)
                host_key = cookie[2]
                if host_key.startswith('.'):
                    top_frame_site_key = 'https://' + host_key[1:]
                else:
                    top_frame_site_key = 'https://' + host_key
                
                current_time = int(time.time() * 1000000)
                
                cursor.execute("""
                    INSERT INTO cookies (
                        creation_utc, host_key, top_frame_site_key, name, value,
                        encrypted_value, path, expires_utc, is_secure, is_httponly,
                        last_access_utc, has_expires, is_persistent, priority, samesite,
                        source_scheme, source_port, last_update_utc, source_type,
                        has_cross_site_ancestor
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    current_time,      # creation_utc
                    cookie[2],         # host_key
                    top_frame_site_key, # top_frame_site_key [新增]
                    cookie[0],         # name
                    cookie[1],         # value
                    b'',               # encrypted_value
                    cookie[3],         # path
                    cookie[4],         # expires_utc
                    cookie[5],         # is_secure
                    cookie[6],         # is_httponly
                    current_time,      # last_access_utc
                    1,                 # has_expires
                    1,                 # is_persistent
                    1,                 # priority
                    cookie[7],         # samesite
                    2,                 # source_scheme (HTTPS)
                    443,               # source_port
                    current_time,      # last_update_utc [新增]
                    0,                 # source_type [新增]
                    0,                 # has_cross_site_ancestor [新增]
                ))
                success += 1
                
                # 显示关键 Cookie
                if cookie[0] in ['SESSDATA', 'bili_jct', 'DedeUserID']:
                    print(f"  ✅ {cookie[0]} @ {cookie[2]}")
                    
            except Exception as e:
                print(f"  ⚠️  跳过 {cookie[0]}: {e}")
        
        conn.commit()
        conn.close()
        
        print(f"  ✅ 成功注入 {success}/{len(cookies)} 个 Cookie")
        
        # 复制回容器
        print("  📤 复制更新后的 Cookies 到容器...")
        os.system(f'docker cp {temp_cookies_db} social-media-hub-uploader-1:/app/chrome/profiles/chrome_profile_ai_vanvan/Default/Network/Cookies >nul 2>&1')
        
        # 清理临时文件
        import shutil
        shutil.rmtree('temp_docker_profile', ignore_errors=True)
        
        return True
        
    except Exception as e:
        print(f"❌ 注入失败: {e}")
        return False

def main():
    print("=" * 70)
    print("📋 自动提取 Chrome B站 Cookies 并注入到 Docker")
    print("=" * 70)
    
    # 1. 找到 Chrome Cookies
    print("\n🔍 步骤 1: 查找 Chrome Cookies...")
    chrome_db = get_chrome_cookies_db()
    
    if not chrome_db:
        print("❌ 找不到 Chrome Profile")
        return False
    
    # 2. 提取 B站 Cookies
    print("\n📦 步骤 2: 提取 B站 Cookies...")
    cookies = extract_bilibili_cookies_safe(chrome_db)
    
    if not cookies:
        return False
    
    # 3. 注入到 Docker Profile
    print("\n💉 步骤 3: 注入到 Docker Profile...")
    if not inject_to_docker_profile(cookies):
        return False
    
    # 4. 删除 Docker 中的锁文件
    print("\n🔓 步骤 4: 删除 Docker Profile 锁文件...")
    os.system('docker exec social-media-hub-uploader-1 rm -f /app/chrome/profiles/chrome_profile_ai_vanvan/SingletonLock 2>nul')
    os.system('docker exec social-media-hub-uploader-1 rm -f /app/chrome/profiles/chrome_profile_ai_vanvan/SingletonSocket 2>nul')
    print("  ✅ 锁文件已清理")
    
    # 5. 重启 uploader
    print("\n🔄 步骤 5: 重启 Uploader 容器...")
    os.system('docker-compose restart uploader >nul 2>&1')
    print("  ✅ 容器已重启")
    
    print("\n" + "=" * 70)
    print("🎉 所有步骤完成！现在可以测试上传了")
    print("=" * 70)
    print("\n测试命令:")
    print("  powershell -File test_upload_simple.ps1")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        if not success:
            print("\n❌ 操作失败")
            input("\n按 Enter 退出...")
    except KeyboardInterrupt:
        print("\n\n⚠️  已取消")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按 Enter 退出...")
