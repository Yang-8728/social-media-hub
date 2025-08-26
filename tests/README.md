# 测试文档

本目录包含Social Media Hub项目的所有测试文件。

## 目录结构

```
tests/
├── __init__.py                    # 测试模块初始化
├── run_tests.py                   # 主测试运行器
├── unit/                          # 单元测试
│   ├── __init__.py
│   ├── test_folder_manager.py     # 文件夹管理器测试
│   ├── test_logger.py             # 日志模块测试
│   └── test_models.py             # 数据模型测试
└── integration/                   # 集成测试
    ├── __init__.py
    └── test_system.py             # 系统集成测试
```

## 运行测试

### 运行所有测试
```bash
cd tests
python run_tests.py
```

### 只运行单元测试
```bash
cd tests
python run_tests.py --unit
```

### 只运行集成测试
```bash
cd tests
python run_tests.py --integration
```

### 运行特定测试文件
```bash
cd tests
python unit/test_logger.py
python unit/test_models.py
python unit/test_folder_manager.py
python integration/test_system.py
```

## 测试类型说明

### 单元测试 (unit/)
- 测试单个模块或函数的功能
- 不依赖外部服务（如网络、文件系统等）
- 快速执行，用于验证代码逻辑正确性

### 集成测试 (integration/)
- 测试多个模块协同工作
- 可能涉及文件系统、网络等外部依赖
- 验证完整的工作流程

## 添加新测试

1. **单元测试**: 在 `unit/` 目录创建 `test_模块名.py`
2. **集成测试**: 在 `integration/` 目录创建 `test_功能名.py`
3. 使用 `unittest` 框架编写测试类
4. 在测试运行器中添加新测试的导入和执行

## 测试覆盖的功能

- ✅ 文件夹管理器 (FolderManager)
- ✅ 日志系统 (Logger)  
- ✅ 数据模型 (Models)
- ✅ 系统集成测试
- ⏳ Instagram下载器 (计划中)
- ⏳ 视频合并器 (计划中)
- ⏳ Bilibili上传器 (计划中)
