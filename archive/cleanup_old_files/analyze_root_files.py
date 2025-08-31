import os
import re

# 分析根目录下的Python文件
root_files = []
for item in os.listdir('.'):
    if item.endswith('.py'):
        root_files.append(item)

print("=== 根目录Python文件分析 ===")
print(f"总共发现 {len(root_files)} 个Python文件")
print()

# 按功能分类
categories = {
    '核心功能': ['main.py'],
    '测试文件': [],
    '调试工具': [],
    '分析工具': [],
    '检查工具': [],
    '修复工具': [],
    '临时文件': []
}

for file in sorted(root_files):
    if file.startswith('test_'):
        categories['测试文件'].append(file)
    elif file.startswith('debug_'):
        categories['调试工具'].append(file)
    elif file.startswith('analyze_'):
        categories['分析工具'].append(file)
    elif file.startswith('check_'):
        categories['检查工具'].append(file)
    elif file.startswith('fix_') or 'fix' in file.lower():
        categories['修复工具'].append(file)
    elif file in ['main.py']:
        pass  # 已经在核心功能中
    else:
        categories['临时文件'].append(file)

for category, files in categories.items():
    if files:
        print(f"📁 {category} ({len(files)}个):")
        for file in files:
            print(f"  - {file}")
        print()

# 建议清理的文件
cleanup_candidates = []
cleanup_candidates.extend(categories['临时文件'])
cleanup_candidates.extend(categories['调试工具'])
cleanup_candidates.extend([f for f in categories['分析工具'] if 'failure' in f.lower()])

print("🗑️  建议清理的文件:")
for file in cleanup_candidates:
    print(f"  - {file}")

print()
print("✅ 建议保留的文件:")
keep_files = ['main.py', 'fix_unicode_paths.py']
for file in keep_files:
    if file in root_files:
        print(f"  - {file} (重要)")

print()
print("📦 应该移动到适当目录的文件:")
move_candidates = [f for f in categories['测试文件'] if f not in keep_files]
for file in move_candidates:
    print(f"  - {file} → tests/")
