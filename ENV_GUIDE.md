# 环境分离使用指南

## 🎯 概述
为了避免测试时影响生产环境，项目现在支持**开发环境**和**生产环境**的完全分离。

## 🌍 环境说明

### 🧪 开发环境 (Development)
- **用途**: 功能测试、调试、实验新功能
- **特点**: 
  - 独立的数据目录 (`videos_dev/`, `logs_dev/`, `temp_dev/`)
  - 安全限制更严格 (最多下载5个视频)
  - 支持模拟操作，不影响真实数据
  - 标题前缀带有 `[测试]` 标识

### 🏭 生产环境 (Production) 
- **用途**: 日常正式使用
- **特点**:
  - 使用标准数据目录 (`videos/`, `logs/`, `temp/`)
  - 正常的下载和上传限制
  - 真实操作，会影响实际数据

## 🔄 环境切换

### 方法1: 使用批处理脚本 (推荐)
```bash
# 交互式菜单
env.bat

# 直接切换
env.bat dev       # 切换到开发环境
env.bat prod      # 切换到生产环境
env.bat status    # 查看当前状态
env.bat clean     # 清理测试数据
```

### 方法2: 使用Python工具
```bash
# 查看状态
python tools/env_manager.py status

# 切换环境
python tools/env_manager.py switch dev
python tools/env_manager.py switch prod

# 创建测试数据
python tools/env_manager.py create-test

# 清理测试数据
python tools/env_manager.py clean-test
```

## 🎮 使用示例

### 安全测试流程
```bash
# 1. 切换到开发环境
env.bat dev

# 2. 测试下载功能 (只会下载少量内容)
python main.py --download --ai_vanvan

# 3. 测试合并功能 (使用测试数据)
python main.py --merge ai_vanvan_test --limit 3

# 4. 测试完成后切换回生产环境
env.bat prod
```

### 生产使用流程
```bash
# 1. 确保在生产环境
env.bat prod

# 2. 正常使用
python main.py --ai_vanvan     # 完整流程
python main.py --aigf8728      # 完整流程
```

## 📁 目录结构对比

### 生产环境目录
```
social-media-hub/
├── videos/           # 生产视频
├── logs/            # 生产日志
└── temp/            # 生产临时文件
```

### 开发环境目录
```
social-media-hub/
├── videos_dev/       # 测试视频
├── logs_dev/        # 测试日志
└── temp_dev/        # 测试临时文件
```

## ⚙️ 配置文件说明

### 环境配置: `config/environments.json`
定义开发和生产环境的基本设置

### 测试账户配置: `config/accounts_test.json`
开发环境专用的账户配置，包含安全限制

### 当前环境: `config/current_environment.json`
记录当前激活的环境 (自动生成)

## 🛡️ 安全特性

### 开发环境安全限制
- 最大下载量: 5个视频/次 (vs 生产环境50个)
- 请求延迟: 3-5秒 (vs 生产环境2秒)
- 自动跳过上传操作
- 标题加上 `[测试]` 前缀

### 防止误操作
- 环境状态实时显示
- 操作前显示当前环境
- 测试数据目录与生产完全隔离

## 🧹 清理和维护

### 定期清理测试数据
```bash
# 清理所有测试数据
env.bat clean

# 或手动删除
rmdir /s /q videos_dev logs_dev temp_dev
```

### 重置环境
```bash
# 删除环境配置文件
del config/current_environment.json

# 重新初始化 (默认生产环境)
python main.py --status
```

## 💡 最佳实践

1. **测试新功能时**: 始终切换到开发环境
2. **日常使用时**: 确保在生产环境
3. **遇到问题时**: 在开发环境复现和调试
4. **定期清理**: 清理测试环境的临时数据
5. **环境确认**: 每次操作前确认当前环境

## 🚨 注意事项

- 环境切换会立即生效，无需重启程序
- 测试环境的数据不会影响生产环境
- 在开发环境下载的内容会保存到独立目录
- 环境配置文件应该纳入版本控制，但当前环境文件不应该
