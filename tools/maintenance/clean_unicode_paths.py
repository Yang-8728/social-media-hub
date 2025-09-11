#!/usr/bin/env python3
"""
Unicode路径清理工具
清理由于instaloader库创建的Unicode分隔符异常文件夹

问题说明：
- instaloader在某些情况下会创建包含Unicode分隔符（﹨）的文件夹
- 这些文件夹会出现在项目根目录，影响项目结构
- 此工具可以安全地清理这些异常文件夹

使用方法：
    python scripts/clean_unicode_paths.py
"""
import os
import shutil
import sys


def find_unicode_paths(directory="."):
    """查找包含Unicode分隔符的异常路径"""
    unicode_paths = []
    unicode_separator = chr(65128)  # ﹨ (U+FE68)
    
    try:
        for item in os.listdir(directory):
            if unicode_separator in item:
                full_path = os.path.join(directory, item)
                if os.path.isdir(full_path):
                    unicode_paths.append(full_path)
                    print(f"🔍 发现Unicode路径: {item}")
    except Exception as e:
        print(f"❌ 扫描目录失败: {e}")
        return []
    
    return unicode_paths


def clean_unicode_paths(unicode_paths):
    """清理Unicode路径文件夹"""
    if not unicode_paths:
        print("✅ 没有发现Unicode路径异常文件夹")
        return
    
    print(f"🧹 准备清理 {len(unicode_paths)} 个Unicode路径文件夹")
    
    for unicode_path in unicode_paths:
        try:
            # 检查文件夹内容
            if os.path.exists(unicode_path):
                files = os.listdir(unicode_path)
                if files:
                    print(f"⚠️  {unicode_path} 不为空，包含 {len(files)} 个文件，跳过清理")
                    continue
                
                # 删除空文件夹
                shutil.rmtree(unicode_path)
                print(f"🗑️  已清理: {unicode_path}")
            else:
                print(f"ℹ️  路径不存在: {unicode_path}")
                
        except Exception as e:
            print(f"❌ 清理失败 {unicode_path}: {e}")


def main():
    """主函数"""
    print("🛠️  Unicode路径清理工具")
    print("=" * 50)
    
    # 查找Unicode路径
    unicode_paths = find_unicode_paths()
    
    if not unicode_paths:
        print("🎉 项目根目录干净，无需清理")
        return
    
    # 显示发现的路径
    print(f"\n📋 发现的Unicode路径异常文件夹:")
    for i, path in enumerate(unicode_paths, 1):
        print(f"  {i}. {path}")
    
    # 确认清理
    print(f"\n⚠️  即将清理 {len(unicode_paths)} 个异常文件夹")
    confirm = input("确认清理？(y/N): ").lower().strip()
    
    if confirm == 'y':
        clean_unicode_paths(unicode_paths)
        print("\n🎉 清理完成！")
    else:
        print("❌ 取消清理操作")


if __name__ == "__main__":
    main()