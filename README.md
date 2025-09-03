# Social Media Hub

🎯 **企业级社交媒体内容管理系统** | **v2.3.0-ai_vanvan-final**

一个专业的Instagram内容下载、管理和处理工具，支持多账户管理、自动化下载、高级视频合并等功能。

## ✨ 主要特性

- 🔐 **安全登录**: 基于Firefox Session的无密码登录
- 📱 **多平台支持**: 目前支持Instagram，架构支持扩展
- 👥 **多账户管理**: 支持多个账户独立配置和管理
- 📁 **智能文件夹**: 按日期、博主等策略自动组织文件
- 🎬 **高级视频合并**: 支持标准合并和终极标准化合并
- 🔧 **视频修复**: 自动修复时间戳、音频质量等问题
- 📊 **下载记录**: 完整的下载历史和去重机制
- 🛡️ **路径保护**: 自动处理Unicode路径问题
- 🎨 **友好界面**: 清晰的进度显示和状态反馈

## 🚀 快速开始

### 1. 环境准备
```bash
# 激活虚拟环境
setup_green_venv.bat

# 设置UTF-8编码(Windows)
chcp 65001
```

### 2. 下载内容
```bash
# 下载搞笑内容
python main.py --download --ai_vanvan

# 下载女友内容
python main.py --download --aigf8728
```

### 3. 视频合并

#### 标准合并
```bash
# 合并最新8个视频
python main.py --merge ai_vanvan --limit 8
```

#### 终极标准化合并 ⭐
```bash
# 使用终极标准化合并（推荐）
python main.py --merge ai_vanvan --ultimate
```

## 🎬 视频处理功能

### 合并模式对比

| 模式 | 速度 | 质量 | 适用场景 |
|------|------|------|----------|
| 标准合并 | 快速 | 保持原始 | 高质量视频 |
| 终极合并 | 较慢 | 完全标准化 | 有问题的视频 ⭐ |

### 问题诊断工具
```bash
# 扫描视频质量
python scripts/analysis/complete_audio_scan.py

# 分析特定问题
python scripts/analysis/deep_analyze_problem_video.py
```

## 📁 项目结构

```
social-media-hub/
├── 📚 docs/                 # 文档目录
│   ├── VIDEO_MERGE_GUIDE.md # 视频合并完整指南
│   └── PROJECT_STRUCTURE.md # 项目结构说明
├── 🛠️ scripts/              # 工具脚本
│   ├── analysis/            # 视频分析工具
│   └── merge/               # 合并处理工具
├── 💻 src/                  # 源代码
│   └── utils/
│       └── video_merger.py  # 视频合并核心模块
├── 🗃️ temp/                 # 临时文件
└── 📄 main.py               # 主程序入口
│   ├── utils/              # 工具模块
│   ├── platforms/          # 平台实现
│   └── core/              # 核心接口
├── ⚙️ config/              # 配置文件
├── 📹 videos/              # 视频存储
└── 📝 logs/                # 日志文件
```

## 🔧 命令行参数

### 下载命令
- `--download` - 启动下载任务
- `--ai_vanvan` - 使用搞笑账户 (ai_vanvan)
- `--aigf8728` - 使用女友账户 (aigf8728)  
- `--limit N` - 限制下载数量

### 合并命令
- `--merge` - 启动视频合并
- `--merge-limit N` - 限制合并视频数量

### 示例
```bash
# 下载最多20个视频
python main.py --download --ai_vanvan --limit 20

# 合并最新5个视频
python main.py --merge --aigf8728 --merge-limit 5
```

## 🛠️ 工具脚本

| 工具 | 用途 | 命令 |
|-----|------|------|
| Unicode路径检查 | 修复路径问题 | `python tools/check_unicode_paths.py` |
| Bug记录助手 | 添加bug记录 | `python tools/add_bug_record.py` |
| 记录导入 | 迁移历史数据 | `python tools/import_old_records.py` |

## 📚 文档

- 📖 [项目文档索引](docs/项目文档索引.md) - 所有文档的导航
- 🐛 [Bug修复记录](docs/Bug修复记录.md) - 问题和解决方案
- 🔧 [Unicode路径问题解决指南](docs/Unicode路径问题解决指南.md) - 路径问题专题

## ⚙️ 配置说明

### 账户配置 (`config/accounts.json`)
```json
{
  "ai_vanvan": {
    "instagram": {"username": "ai_vanvan"},
    "download_dir": "videos/downloads/ai_vanvan",
    "folder_strategy": "daily",
    "download_safety": {
      "max_posts_per_session": 50,
      "request_delay": 2
    }
  }
}
```

### 文件夹策略
- `daily` - 按日期创建文件夹 (YYYY-MM-DD)
- `blogger_daily` - 按博主+日期创建文件夹

## 🔒 安全特性

- ✅ **请求限制**: 控制API调用频率，防止被封号
- ✅ **Session管理**: 安全的登录状态管理
- ✅ **路径验证**: 防止恶意路径攻击
- ✅ **Unicode处理**: 自动修复路径编码问题

## 🐛 问题排查

### 常见问题
1. **文件找不到** → 运行 `python tools/check_unicode_paths.py`
2. **登录失败** → 检查Firefox是否已登录Instagram
3. **下载慢** → 调整 `request_delay` 参数
4. **编码问题** → 确保运行 `chcp 65001`

### 获取帮助
- 查看 [Bug修复记录](docs/Bug修复记录.md) 寻找解决方案
- 检查日志文件 `logs/` 目录
- 使用工具脚本进行诊断

## 📊 功能状态

| 功能 | 状态 | 说明 |
|-----|------|------|
| Instagram下载 | ✅ 完成 | 支持保存的帖子下载 |
| 多账户管理 | ✅ 完成 | 支持独立配置 |
| 视频合并 | ✅ 完成 | 支持数量限制 |
| 路径处理 | ✅ 完成 | Unicode问题已修复 |
| 进度显示 | ✅ 完成 | 单行进度条 |
| Bilibili上传 | 🚧 计划 | 后续版本 |

## 🤝 贡献指南

1. **报告问题**: 使用 `python tools/add_bug_record.py` 记录bug
2. **提交修复**: 更新相应的文档和测试
3. **代码风格**: 遵循项目现有代码规范
4. **文档更新**: 修改功能时同步更新文档

## 📄 许可证

本项目为内部工具，请遵守相关平台的使用条款。

---

**📝 最后更新**: 2025-08-26  
**🔧 技术栈**: Python 3.11, instaloader, ffmpeg  
**💻 平台**: Windows (主要), Linux/Mac (兼容)
