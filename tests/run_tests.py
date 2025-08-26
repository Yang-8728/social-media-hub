#!/usr/bin/env python3
"""
测试运行器 - 运行所有测试
"""
import sys
import os
import unittest

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def run_unit_tests():
    """运行单元测试"""
    print("=== 运行单元测试 ===")
    
    # 导入并运行文件夹管理器测试
    from tests.unit.test_folder_manager import test_folder_strategies, check_created_folders
    test_folder_strategies()
    check_created_folders()
    print("✅ 单元测试完成\n")

def run_integration_tests():
    """运行集成测试"""
    print("=== 运行集成测试 ===")
    
    # 导入并运行系统测试
    from tests.integration.test_system import main as test_system_main
    test_system_main()
    print("✅ 集成测试完成\n")

def run_all_tests():
    """运行所有测试"""
    print("🧪 Social Media Hub 测试套件")
    print("=" * 50)
    
    try:
        run_unit_tests()
        run_integration_tests()
        print("🎉 所有测试通过！")
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="测试运行器")
    parser.add_argument("--unit", action="store_true", help="只运行单元测试")
    parser.add_argument("--integration", action="store_true", help="只运行集成测试")
    
    args = parser.parse_args()
    
    if args.unit:
        run_unit_tests()
    elif args.integration:
        run_integration_tests()
    else:
        success = run_all_tests()
        sys.exit(0 if success else 1)
