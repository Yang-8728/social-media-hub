import os

print("=== Social-Media-Hub 根目录文件分析 ===")

# 获取所有文件（排除目录）
all_files = []
for item in os.listdir('.'):
    if os.path.isfile(item):
        all_files.append(item)

print(f"根目录总文件数: {len(all_files)}")
print()

# 按文件类型分类
file_types = {
    'Python文件': [],
    'Batch文件': [],
    'Markdown文档': [],
    '配置文件': [],
    '其他文件': []
}

for file in sorted(all_files):
    if file.endswith('.py'):
        file_types['Python文件'].append(file)
    elif file.endswith('.bat'):
        file_types['Batch文件'].append(file)
    elif file.endswith('.md'):
        file_types['Markdown文档'].append(file)
    elif file.endswith(('.txt', '.json', '.ini', '.cfg')):
        file_types['配置文件'].append(file)
    else:
        file_types['其他文件'].append(file)

# 显示分类结果
for category, files in file_types.items():
    if files:
        print(f"📁 {category} ({len(files)}个):")
        for file in files:
            size_kb = os.path.getsize(file) / 1024
            print(f"  - {file} ({size_kb:.1f}KB)")
        print()

# 具体分析bat文件
print("🔍 Batch文件详细分析:")
bat_files = file_types['Batch文件']
for bat_file in bat_files:
    print(f"\n📄 {bat_file}:")
    try:
        with open(bat_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()[:200]  # 读取前200字符
            lines = content.split('\n')[:3]  # 前3行
            for line in lines:
                if line.strip():
                    print(f"    {line.strip()}")
    except Exception as e:
        print(f"    无法读取: {e}")

# 整理建议
print("\n🧹 整理建议:")

# 分析每个bat文件的作用
bat_analysis = {
    'setup_colors.bat': '终端颜色设置 - 可移动到tools/setup/',
    'setup_green_venv.bat': 'Python环境设置 - 可移动到tools/setup/',
    'setup_perfect_colors.bat': '终端美化设置 - 可移动到tools/setup/',
    'view-log.bat': '日志查看工具 - 可移动到tools/scripts/'
}

print("\n📦 建议重新组织:")
for bat_file in bat_files:
    suggestion = bat_analysis.get(bat_file, '需要检查用途')
    print(f"  - {bat_file} → {suggestion}")

print(f"\n📋 其他文件处理建议:")
print(f"  - requirements.txt → 保留（Python依赖）") 
print(f"  - README.md → 保留（项目说明）")
print(f"  - .gitignore → 保留（Git配置）")

# 检查是否有奇怪的目录
weird_dirs = []
for item in os.listdir('.'):
    if os.path.isdir(item) and ('：' in item or '﹨' in item):
        weird_dirs.append(item)

if weird_dirs:
    print(f"\n⚠️  发现异常目录:")
    for dir_name in weird_dirs:
        print(f"  - {repr(dir_name)} (包含特殊字符)")
        print(f"    建议清理或重命名")
