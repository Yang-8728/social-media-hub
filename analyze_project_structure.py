import os

def analyze_directory_structure(path, prefix="", max_depth=3, current_depth=0):
    """递归分析目录结构"""
    if current_depth > max_depth:
        return
    
    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        print(f"{prefix}❌ 权限拒绝")
        return
    
    dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
    files = [item for item in items if os.path.isfile(os.path.join(path, item))]
    
    # 显示目录
    for dir_name in dirs:
        dir_path = os.path.join(path, dir_name)
        
        # 特殊标记
        markers = []
        if dir_name.startswith('.'):
            markers.append("🔧")
        elif dir_name in ['__pycache__', 'node_modules', 'venv']:
            markers.append("🗂️")
        elif dir_name in ['src', 'tests', 'docs']:
            markers.append("📁")
        elif dir_name in ['tools', 'scripts']:
            markers.append("🔨")
        else:
            markers.append("📂")
            
        marker = "".join(markers)
        print(f"{prefix}{marker} {dir_name}/")
        
        if current_depth < max_depth:
            analyze_directory_structure(dir_path, prefix + "  ", max_depth, current_depth + 1)
    
    # 显示文件
    for file_name in files:
        file_path = os.path.join(path, file_name)
        file_size = os.path.getsize(file_path)
        
        # 文件类型标记
        if file_name.endswith('.py'):
            marker = "🐍"
        elif file_name.endswith('.md'):
            marker = "📄"
        elif file_name.endswith(('.txt', '.json', '.yaml', '.yml')):
            marker = "📝"
        elif file_name.endswith(('.bat', '.sh')):
            marker = "⚡"
        elif file_name.startswith('.'):
            marker = "⚙️"
        else:
            marker = "📄"
            
        size_str = f"({file_size/1024:.1f}KB)" if file_size < 1024*1024 else f"({file_size/(1024*1024):.1f}MB)"
        print(f"{prefix}{marker} {file_name} {size_str}")

print("=== Social-Media-Hub 项目结构全面分析 ===")
print()

# 分析根目录
print("📊 根目录结构:")
analyze_directory_structure(".", max_depth=2)

print("\n" + "="*60)
print("🔍 项目结构优化建议分析")
print("="*60)

# 检查各个重要目录
important_dirs = {
    'src': '核心源代码',
    'tests': '测试文件',
    'docs': '文档',
    'tools': '工具脚本',
    'config': '配置文件',
    'data': '数据文件',
    'logs': '日志文件',
    'videos': '视频文件'
}

print("\n📁 重要目录状态检查:")
for dir_name, description in important_dirs.items():
    if os.path.exists(dir_name):
        items = os.listdir(dir_name)
        files_count = len([f for f in items if os.path.isfile(os.path.join(dir_name, f))])
        dirs_count = len([f for f in items if os.path.isdir(os.path.join(dir_name, f))])
        
        print(f"✅ {dir_name}/ - {description}")
        print(f"   📊 包含: {dirs_count}个子目录, {files_count}个文件")
        
        # 检查是否有README
        if not os.path.exists(os.path.join(dir_name, 'README.md')):
            print(f"   💡 建议: 添加 {dir_name}/README.md 说明")
    else:
        print(f"❌ {dir_name}/ - {description} (不存在)")

# 检查项目标准文件
print("\n📋 项目标准文件检查:")
standard_files = {
    'README.md': '项目主文档',
    'requirements.txt': 'Python依赖',
    '.gitignore': 'Git忽略规则',
    'LICENSE': '开源许可证',
    'CHANGELOG.md': '变更日志',
    'CONTRIBUTING.md': '贡献指南',
    'setup.py': 'Python包安装脚本',
    'pyproject.toml': '现代Python项目配置',
    'Dockerfile': 'Docker容器化',
    '.github/workflows/': 'GitHub Actions CI/CD'
}

for file_name, description in standard_files.items():
    if os.path.exists(file_name):
        if os.path.isfile(file_name):
            size = os.path.getsize(file_name)
            print(f"✅ {file_name} - {description} ({size/1024:.1f}KB)")
        else:
            print(f"✅ {file_name} - {description} (目录)")
    else:
        if file_name in ['LICENSE', 'CHANGELOG.md', 'CONTRIBUTING.md']:
            print(f"💡 {file_name} - {description} (建议添加)")
        else:
            print(f"❌ {file_name} - {description} (缺失)")

# 代码结构分析
print("\n🏗️  代码架构分析:")
if os.path.exists('src'):
    src_structure = {}
    for root, dirs, files in os.walk('src'):
        level = root.replace('src', '').count(os.sep)
        if level <= 2:  # 只分析前2层
            py_files = [f for f in files if f.endswith('.py')]
            if py_files:
                relative_path = os.path.relpath(root, 'src')
                src_structure[relative_path] = len(py_files)
    
    for path, count in sorted(src_structure.items()):
        print(f"  📦 src/{path}: {count}个Python文件")

# 文件大小分析
print("\n📏 大文件检查 (>1MB):")
large_files = []
for root, dirs, files in os.walk('.'):
    # 跳过特定目录
    dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', 'node_modules']]
    
    for file in files:
        file_path = os.path.join(root, file)
        try:
            size = os.path.getsize(file_path)
            if size > 1024 * 1024:  # >1MB
                large_files.append((file_path, size))
        except:
            pass

large_files.sort(key=lambda x: x[1], reverse=True)
for file_path, size in large_files[:10]:  # 显示前10个大文件
    size_mb = size / (1024 * 1024)
    print(f"  📊 {file_path}: {size_mb:.1f}MB")

if not large_files:
    print("  ✅ 没有发现大文件")

print("\n🎯 优化建议总结将在下方输出...")
