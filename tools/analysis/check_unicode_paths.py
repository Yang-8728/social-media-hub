#!/usr/bin/env python3
"""
Unicode路径问题快速检查工具
用于排查和修复路径中的Unicode字符问题

使用方法:
python tools/check_unicode_paths.py [目录路径]
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.path_utils import clean_unicode_path, ensure_valid_windows_path


def has_unicode_path_chars(path: str) -> bool:
    """检测路径是否包含Unicode分隔符"""
    unicode_chars = ['﹨', '∕', '⧵', '⁄', '／', '＼']
    return any(char in path for char in unicode_chars)


def scan_unicode_paths(base_dir: str):
    """扫描目录中的Unicode路径问题"""
    problems = []
    
    print(f"🔍 扫描目录: {base_dir}")
    print("-" * 50)
    
    if not os.path.exists(base_dir):
        print(f"❌ 目录不存在: {base_dir}")
        return
    
    for root, dirs, files in os.walk(base_dir):
        # 检查目录路径
        if has_unicode_path_chars(root):
            correct_path = clean_unicode_path(root)
            problems.append({
                'type': 'directory',
                'current': root,
                'correct': correct_path
            })
            print(f"📁 Unicode目录: {root}")
            print(f"   应修正为: {correct_path}")
            print()
        
        # 检查文件路径
        for file in files:
            file_path = os.path.join(root, file)
            if has_unicode_path_chars(file_path):
                correct_path = clean_unicode_path(file_path)
                problems.append({
                    'type': 'file',
                    'current': file_path,
                    'correct': correct_path
                })
                print(f"📄 Unicode文件: {file_path}")
                print(f"   应修正为: {correct_path}")
                print()
    
    if not problems:
        print("✅ 未发现Unicode路径问题！")
    else:
        print(f"⚠️  发现 {len(problems)} 个Unicode路径问题")
        
        # 询问是否修复
        if input("\n是否自动修复这些问题？(y/N): ").lower() == 'y':
            fix_unicode_paths(problems)
    
    return problems


def fix_unicode_paths(problems):
    """修复Unicode路径问题"""
    import shutil
    
    fixed_count = 0
    
    for problem in problems:
        try:
            current = problem['current']
            correct = problem['correct']
            
            if os.path.exists(current):
                # 确保目标目录存在
                target_dir = os.path.dirname(correct)
                os.makedirs(target_dir, exist_ok=True)
                
                # 移动文件或目录
                shutil.move(current, correct)
                print(f"✅ 已修复: {current} -> {correct}")
                fixed_count += 1
            else:
                print(f"⚠️  跳过不存在的路径: {current}")
                
        except Exception as e:
            print(f"❌ 修复失败 {current}: {e}")
    
    print(f"\n🎉 成功修复 {fixed_count} 个路径问题！")


def main():
    """主函数"""
    if len(sys.argv) > 1:
        scan_dir = sys.argv[1]
    else:
        # 默认扫描videos目录
        scan_dir = os.path.join(project_root, "videos")
    
    print("🔧 Unicode路径问题检查工具")
    print("=" * 50)
    
    scan_unicode_paths(scan_dir)


if __name__ == "__main__":
    main()
