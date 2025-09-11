#!/usr/bin/env python3
"""
环境管理工具 - 在测试环境和生产环境之间切换
"""

import os
import sys
import json
import shutil
from pathlib import Path

class EnvironmentManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config_dir = self.project_root / "config"
        self.env_config_file = self.config_dir / "environments.json"
        self.current_env_file = self.config_dir / "current_environment.json"
        
    def load_environments(self):
        """加载环境配置"""
        if not self.env_config_file.exists():
            print("❌ 环境配置文件不存在")
            return None
            
        with open(self.env_config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_current_environment(self):
        """获取当前环境"""
        if not self.current_env_file.exists():
            return "production"  # 默认生产环境
            
        with open(self.current_env_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("current_environment", "production")
    
    def switch_environment(self, env_name):
        """切换环境"""
        environments = self.load_environments()
        if not environments or env_name not in environments:
            print(f"❌ 环境 '{env_name}' 不存在")
            return False
            
        # 保存当前环境设置
        current_env_data = {
            "current_environment": env_name,
            "switch_time": __import__('datetime').datetime.now().isoformat(),
            "previous_environment": self.get_current_environment()
        }
        
        with open(self.current_env_file, 'w', encoding='utf-8') as f:
            json.dump(current_env_data, f, ensure_ascii=False, indent=2)
        
        # 创建环境特定的目录
        env_config = environments[env_name]
        base_paths = env_config["base_paths"]
        
        for path_name, path_value in base_paths.items():
            path_dir = self.project_root / path_value
            path_dir.mkdir(exist_ok=True)
            print(f"✅ 创建目录: {path_dir}")
        
        print(f"🔄 已切换到 {env_name} 环境: {env_config['name']}")
        print(f"📝 描述: {env_config['description']}")
        
        return True
    
    def show_status(self):
        """显示当前环境状态"""
        current_env = self.get_current_environment()
        environments = self.load_environments()
        
        if not environments:
            print("❌ 无法加载环境配置")
            return
            
        print("🌍 环境状态")
        print("=" * 50)
        
        for env_name, env_config in environments.items():
            marker = "👉" if env_name == current_env else "  "
            print(f"{marker} {env_name}: {env_config['name']}")
            if env_name == current_env:
                print(f"     📝 {env_config['description']}")
                print(f"     📁 视频目录: {env_config['base_paths']['videos']}")
                print(f"     📋 日志目录: {env_config['base_paths']['logs']}")
                
                # 显示特性
                features = env_config['features']
                print(f"     🎯 特性:")
                for feature, enabled in features.items():
                    status = "✅" if enabled else "❌"
                    print(f"        {status} {feature}")
    
    def create_test_data(self):
        """创建测试数据"""
        current_env = self.get_current_environment()
        if current_env != "development":
            print("⚠️ 只能在开发环境创建测试数据")
            return False
            
        # 创建一些测试视频文件（空文件）
        test_videos_dir = self.project_root / "videos_dev" / "downloads" / "ai_vanvan_test"
        test_videos_dir.mkdir(parents=True, exist_ok=True)
        
        test_files = [
            "test_video_1.mp4",
            "test_video_2.mp4", 
            "test_video_3.mp4"
        ]
        
        for filename in test_files:
            test_file = test_videos_dir / filename
            if not test_file.exists():
                test_file.write_text("# 测试视频文件")
                print(f"✅ 创建测试文件: {test_file}")
        
        print(f"🎯 测试数据创建完成: {test_videos_dir}")
        return True
    
    def clean_test_data(self):
        """清理测试数据"""
        test_dirs = ["videos_dev", "logs_dev", "temp_dev"]
        
        for dir_name in test_dirs:
            test_dir = self.project_root / dir_name
            if test_dir.exists():
                try:
                    shutil.rmtree(test_dir)
                    print(f"🗑️ 已删除: {test_dir}")
                except Exception as e:
                    print(f"❌ 删除失败 {test_dir}: {e}")
        
        print("🧹 测试数据清理完成")

def main():
    env_manager = EnvironmentManager()
    
    if len(sys.argv) < 2:
        print("🌍 环境管理工具")
        print("=" * 40)
        print("用法:")
        print("  python tools/env_manager.py status          # 查看环境状态")
        print("  python tools/env_manager.py switch dev      # 切换到开发环境")
        print("  python tools/env_manager.py switch prod     # 切换到生产环境")
        print("  python tools/env_manager.py create-test     # 创建测试数据")
        print("  python tools/env_manager.py clean-test      # 清理测试数据")
        print()
        env_manager.show_status()
        return
    
    command = sys.argv[1]
    
    if command == "status":
        env_manager.show_status()
    elif command == "switch":
        if len(sys.argv) < 3:
            print("❌ 请指定环境名称: dev 或 prod")
            return
        
        env_name = sys.argv[2]
        if env_name == "dev":
            env_name = "development"
        elif env_name == "prod":
            env_name = "production"
            
        env_manager.switch_environment(env_name)
    elif command == "create-test":
        env_manager.create_test_data()
    elif command == "clean-test":
        env_manager.clean_test_data()
    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    main()
