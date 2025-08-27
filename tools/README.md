# tools/ - 工具脚本目录

这个目录包含各种辅助工具和脚本，用于项目维护、调试和开发支持。

## 📁 目录结构

```
tools/
├── setup/                   # 环境设置脚本
│   ├── create_folders.bat   # 创建必要的目录结构
│   ├── extract_ffmpeg.bat   # 解压FFmpeg工具
│   └── setup_env.bat        # 环境初始化脚本
└── scripts/                 # 维护和修复脚本
    ├── fix_unicode_paths.py # Unicode路径修复工具 ⭐
    └── view-log.bat         # 日志查看工具
```

## 🛠️ 主要工具

### 🔧 setup/ - 环境设置
- **create_folders.bat**: 自动创建项目所需的所有目录结构
- **extract_ffmpeg.bat**: 解压和配置FFmpeg视频处理工具
- **setup_env.bat**: 一键环境初始化，适合新环境部署

### 📜 scripts/ - 维护脚本
- **fix_unicode_paths.py**: 🌟 核心修复工具，解决Unicode路径问题
  - 自动检测和修复Unicode分隔符 (﹨ → \)
  - 批量迁移文件到标准路径
  - 生成详细的修复报告
- **view-log.bat**: 快速查看最新日志文件

## 🚀 使用指南

### 首次设置
```bash
# 1. 运行环境设置
tools\setup\setup_env.bat

# 2. 创建目录结构
tools\setup\create_folders.bat

# 3. 配置FFmpeg
tools\setup\extract_ffmpeg.bat
```

### 日常维护
```bash
# 修复Unicode路径问题
python tools\scripts\fix_unicode_paths.py

# 查看最新日志
tools\scripts\view-log.bat
```

## ⚠️ 重要说明

- **fix_unicode_paths.py** 是核心修复工具，解决了下载文件路径错乱的关键问题
- 所有bat脚本都经过Windows环境测试
- 建议定期运行fix_unicode_paths.py检查文件路径状态

## 🔍 工具开发

如需添加新工具：
1. 设置类脚本放入 `setup/`
2. 维护类脚本放入 `scripts/`
3. 确保工具有清晰的文档和用法说明
