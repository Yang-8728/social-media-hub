import os
import shutil

print("=== 整理根目录文件和清理异常目录 ===")

# 1. 创建tools子目录
setup_dir = os.path.join('tools', 'setup')
scripts_dir = os.path.join('tools', 'scripts')

os.makedirs(setup_dir, exist_ok=True)
os.makedirs(scripts_dir, exist_ok=True)
print(f"✅ 创建目录: {setup_dir}")
print(f"✅ 创建目录: {scripts_dir}")

# 2. 移动batch文件
batch_moves = {
    'setup_colors.bat': setup_dir,
    'setup_green_venv.bat': setup_dir,
    'setup_perfect_colors.bat': setup_dir,
    'view-log.bat': scripts_dir
}

print(f"\n📦 移动Batch文件:")
for bat_file, target_dir in batch_moves.items():
    if os.path.exists(bat_file):
        target_path = os.path.join(target_dir, bat_file)
        try:
            shutil.move(bat_file, target_path)
            print(f"✅ {bat_file} → {target_dir}/")
        except Exception as e:
            print(f"❌ 移动失败: {bat_file} - {e}")
    else:
        print(f"⚠️  文件不存在: {bat_file}")

# 3. 清理异常目录
print(f"\n🗑️  清理异常目录:")
weird_dirs = []
for item in os.listdir('.'):
    if os.path.isdir(item) and ('：' in item or '﹨' in item):
        weird_dirs.append(item)

for weird_dir in weird_dirs:
    print(f"发现异常目录: {repr(weird_dir)}")
    try:
        # 检查目录内容
        if os.path.exists(weird_dir):
            files_in_dir = os.listdir(weird_dir)
            if files_in_dir:
                print(f"  ⚠️  目录不为空，包含 {len(files_in_dir)} 个项目")
                print(f"  建议手动检查后删除")
            else:
                # 删除空目录
                os.rmdir(weird_dir)
                print(f"  ✅ 删除空目录: {weird_dir}")
    except Exception as e:
        print(f"  ❌ 处理失败: {e}")

# 4. 移动分析脚本到备份
backup_files = ['analyze_all_files.py']
backup_dir = 'cleanup_old_files'

print(f"\n📋 移动临时文件到备份:")
for file in backup_files:
    if os.path.exists(file):
        try:
            shutil.move(file, os.path.join(backup_dir, file))
            print(f"✅ {file} → {backup_dir}/")
        except Exception as e:
            print(f"❌ 移动失败: {file} - {e}")

# 5. 最终检查
print(f"\n📊 整理完成后的根目录:")
remaining_files = []
for item in os.listdir('.'):
    if os.path.isfile(item):
        remaining_files.append(item)

remaining_files.sort()
print(f"剩余文件 ({len(remaining_files)}个):")
for file in remaining_files:
    if file.endswith('.py'):
        print(f"  🐍 {file}")
    elif file.endswith('.md'):
        print(f"  📄 {file}")
    elif file.endswith('.txt'):
        print(f"  📝 {file}")
    else:
        print(f"  📁 {file}")

print(f"\n✅ 根目录现在应该非常干净!")
print(f"核心文件:")
print(f"  - main.py (程序入口)")
print(f"  - fix_unicode_paths.py (重要工具)")
print(f"  - README.md (项目文档)")
print(f"  - requirements.txt (依赖)")
print(f"  - .gitignore (Git配置)")
print(f"  - BUGFIX_UNICODE_PATHS.md (修复记录)")
