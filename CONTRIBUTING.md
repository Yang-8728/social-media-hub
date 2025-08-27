# Contributing to Social Media Hub

感谢您对 Social Media Hub 项目的贡献！本文档将指导您如何参与项目开发。

## 🚀 快速开始

### 开发环境设置

1. **克隆仓库**
```bash
git clone https://github.com/Yang-8728/social-media-hub.git
cd social-media-hub
```

2. **设置Python环境**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# 或 source venv/bin/activate  # Linux/Mac
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **运行环境设置脚本**
```bash
tools\setup\setup_env.bat
tools\setup\create_folders.bat
```

## 📁 项目结构

请先阅读各目录的 README.md 文件了解项目结构：
- `src/README.md` - 核心代码结构
- `tools/README.md` - 工具脚本说明  
- `config/README.md` - 配置文件管理
- `data/README.md` - 数据存储说明

## 🐛 报告问题

### Bug 报告
提交 Bug 时请包含：
- **环境信息**: 操作系统、Python版本
- **重现步骤**: 详细的操作步骤
- **预期行为**: 您期望发生什么
- **实际行为**: 实际发生了什么
- **错误日志**: 相关的错误信息或日志文件
- **Unicode路径**: 如果涉及文件路径问题，请注明是否使用了中文路径

### 功能请求
提交功能请求时请说明：
- **使用场景**: 这个功能解决什么问题
- **建议实现**: 您认为如何实现比较好
- **替代方案**: 目前如何解决这个问题

## 🔧 开发指南

### 代码规范

1. **Python代码风格**
   - 遵循 PEP 8 标准
   - 使用有意义的变量和函数名
   - 添加必要的注释，特别是中文注释用于说明复杂逻辑

2. **文件和路径处理**
   - 始终使用 `os.path.join()` 或 `pathlib` 处理路径
   - 注意Windows Unicode路径问题，测试中文文件名
   - 使用 `clean_unicode_path()` 函数处理路径标准化

3. **错误处理**
   - 使用适当的异常处理
   - 记录详细的错误日志
   - 为用户提供有用的错误信息

### 提交规范

使用清晰的提交信息格式：

```
类型(范围): 简短描述

详细描述（如果需要）

关闭 #问题号码（如果适用）
```

**提交类型**:
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构代码
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

**示例**:
```
fix(instagram): 修复Unicode路径下载问题

- 修复Windows下Unicode路径分隔符问题
- 添加自动路径迁移功能
- 改进错误日志记录

关闭 #123
```

### 测试

1. **运行测试**
```bash
python -m pytest tests/
```

2. **添加测试**
   - 为新功能添加单元测试
   - 确保测试覆盖边界情况
   - 测试Unicode路径和中文文件名

3. **手动测试**
   - 测试不同平台（Windows/Linux/Mac）
   - 验证Unicode路径处理
   - 检查大文件下载和处理

## 🔀 Pull Request 流程

1. **Fork 项目** 到您的GitHub账户

2. **创建功能分支**
```bash
git checkout -b feature/your-feature-name
```

3. **开发和测试**
   - 实现您的功能或修复
   - 添加或更新测试
   - 确保所有测试通过

4. **提交更改**
```bash
git add .
git commit -m "feat: 添加新功能描述"
```

5. **推送到您的Fork**
```bash
git push origin feature/your-feature-name
```

6. **创建 Pull Request**
   - 提供清晰的PR描述
   - 说明更改的内容和原因
   - 引用相关的Issue编号

### Pull Request 检查清单

- [ ] 代码遵循项目编码规范
- [ ] 添加了必要的测试
- [ ] 所有测试都通过
- [ ] 更新了相关文档
- [ ] 测试了Unicode路径兼容性
- [ ] 检查了与现有功能的兼容性

## 🛠️ 开发工具

### 推荐的开发工具
- **IDE**: VS Code 或 PyCharm
- **调试**: 使用内置调试器
- **代码格式化**: black, autopep8
- **静态分析**: flake8, pylint

### 项目工具脚本
- `tools/scripts/fix_unicode_paths.py` - Unicode路径修复
- `tools/setup/create_folders.bat` - 创建目录结构
- `tools/scripts/view-log.bat` - 查看日志

## 📚 资源和文档

- [项目README](README.md) - 项目概述
- [Unicode路径修复文档](BUGFIX_UNICODE_PATHS.md) - 路径问题解决方案
- [API文档](docs/) - 详细的API参考
- [工具使用说明](tools/README.md) - 开发工具指南

## 💬 获取帮助

如果您有任何问题：

1. **查看文档**: 先查看相关的README和文档
2. **搜索Issues**: 看看是否已有类似问题
3. **创建Issue**: 详细描述您的问题
4. **讨论功能**: 可以先创建Issue讨论新功能

## 🙏 致谢

感谢所有为项目做出贡献的开发者！每一个贡献都让项目变得更好。

---

**欢迎加入我们的开发团队！**
