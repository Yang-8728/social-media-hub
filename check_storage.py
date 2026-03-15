"""检查Chrome Profile中的LocalStorage"""
import sqlite3
import os

# Chrome的LocalStorage存储在 Local Storage/leveldb 中
profile_path = '/app/chrome/profiles/chrome_profile_ai_vanvan/Default'

print("🔍 检查Chrome Profile结构...")
print("=" * 80)

# 列出Default目录下的文件
for item in os.listdir(profile_path):
    item_path = os.path.join(profile_path, item)
    if os.path.isdir(item_path):
        print(f"📁 {item}/")
        # 如果是LocalStorage相关目录，列出内容
        if 'Storage' in item or 'storage' in item:
            try:
                for sub_item in os.listdir(item_path):
                    print(f"   └─ {sub_item}")
            except:
                pass

print("\n" + "=" * 80)
print("📋 查找Storage相关文件...")

# 查找所有Storage相关的数据库文件
for root, dirs, files in os.walk(profile_path):
    for file in files:
        if any(x in file.lower() for x in ['storage', 'localstorage', 'sessionstorage', 'leveldb']):
            rel_path = os.path.relpath(os.path.join(root, file), profile_path)
            print(f"  📄 {rel_path}")
