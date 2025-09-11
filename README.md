# Social Media Hub

🎯 **企业级社交媒体内容管理系统** | **v2.7.0-stable**

一个专业的Instagram内容下载、管理和处理工具，支持多账户管理、自动化下载、高级视频合并和B站自动上传等功能。

## 🚀 v2.7.0 重大更新

### ✨ 项目结构重构
- **tools目录整合**: 将原`scripts/`目录完全整合到`tools/`，实现统一工具管理
- **功能分类组织**: 按功能将工具分类到`analysis/`、`merge/`、`maintenance/`、`setup/`等目录
- **Unicode路径修复**: 修复Instagram下载器中的Unicode路径问题，添加自动清理机制
- **配置简化**: 移除测试环境配置，统一使用生产环境配置

### 🗂️ 新的工具目录结构
```
tools/
├── analysis/     # 视频分析工具
├── merge/        # 视频合并工具  
├── maintenance/  # 维护和清理工具
├── setup/        # 环境设置工具
├── diagnosis/    # 问题诊断工具
├── login/        # 登录管理工具
└── recovery/     # 恢复工具
```

## ✨ 主要特性

- 🔐 **安全登录**: 基于Firefox Session的无密码登录
- 📱 **多平台支持**: Instagram下载 + B站上传的完整工作流
- 👥 **多账户管理**: 支持多个账户独立配置和管理
- 📁 **智能文件夹**: 按日期、博主等策略自动组织文件
- 🎬 **高级视频合并**: 支持标准合并和终极标准化合并
- 📺 **自动上传**: 支持B站自动上传，账户专用标题格式
- 🎯 **智能命名**: 基于上传标题的文件命名系统
- 🔧 **视频修复**: 自动修复时间戳、音频质量等问题
- 📊 **下载记录**: 完整的下载历史和去重机制
- 🛡️ **路径保护**: 自动处理Unicode路径问题
- 🎨 **友好界面**: 清晰的进度显示和状态反馈

## � 项目结构

```
social-media-hub/
├── 📁 src/                       # 核心源代码
│   ├── 📁 utils/
│   │   ├── 📄 video_merger.py    # 视频合并核心模块 ⭐
│   │   ├── 📄 logger.py          # 日志系统
│   │   └── 📄 folder_manager.py  # 文件管理
│   ├── 📁 platforms/             # 平台集成
│   │   ├── 📁 instagram/         # Instagram相关
│   │   └── 📁 bilibili/          # B站相关
│   └── 📁 core/                  # 核心接口和模型
├── 📁 scripts/                   # 工具脚本
│   ├── 📁 analysis/              # 视频分析工具 🔍
│   │   ├── 📄 complete_audio_scan.py     # 完整音频扫描
│   │   ├── 📄 check_today_videos.py      # 视频质量检查
│   │   └── 📄 deep_analyze_problem_video.py # 深度问题分析
│   └── 📁 merge/                 # 合并工具 🔧
│       ├── 📄 ultimate_merge_script.py   # 终极合并脚本 ⭐
│       ├── 📄 strategy2_smart_fix.py     # 智能修复
│       └── 📄 fix_negative_timestamp.py  # 时间戳修复
├── 📁 config/                    # 配置文件
├── 📁 logs/                      # 日志系统
├── 📁 tools/                     # 外部工具
│   └── 📁 ffmpeg/                # FFmpeg工具包
├── 📁 videos/                    # 视频存储
│   ├── 📁 downloads/             # 下载视频
│   └── 📁 merged/                # 合并后视频
├── 📄 main.py                    # 主程序入口 🚀
├── 📄 requirements.txt           # 依赖包
└── 📄 README.md                  # 项目说明
```

## �🚀 快速开始

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

# 合并aigf8728账户视频（使用智能文件命名）
python main.py --merge aigf8728 --limit 5
```

### 5. 问题诊断工具

#### 音频质量扫描
```bash
python scripts/analysis/complete_audio_scan.py
```

#### 问题视频分析
```bash
python scripts/analysis/deep_analyze_problem_video.py
```

### 6. 视频合并问题排查

#### 识别问题视频
- 音频比特率 < 50kbps
- 负数时间戳
- 非标准编码参数

#### 选择修复策略
- **普通合并**: 适用于质量良好的视频
- **终极合并**: 适用于有问题的视频，包含完全标准化

#### 验证修复效果
```bash
python scripts/analysis/verify_ultimate_result.py
```

## 🎬 视频处理技术细节

### 时间戳问题修复
使用FFmpeg参数修复负数时间戳：
```bash
-avoid_negative_ts make_zero
-fflags +genpts
```

### 音频标准化
统一音频参数：
```bash
-c:a aac
-b:a 128k
-ar 44100
-ac 2
-sample_fmt fltp
```

### 视频标准化
统一视频参数：
```bash
-c:v libx264
-crf 23
-preset medium
-profile:v high
-level 4.0
-pix_fmt yuv420p
-r 30
```

## 🔧 工具脚本说明

### 分析工具 (scripts/analysis/)
- **complete_audio_scan.py**: 扫描所有视频的音频质量
- **check_today_videos.py**: 检查特定日期的视频
- **analyze_audio_strategy.py**: 分析音频处理策略
- **deep_analyze_problem_video.py**: 深度分析问题视频
- **verify_ultimate_result.py**: 验证最终合并结果

### 合并工具 (scripts/merge/)
- **ultimate_merge_script.py**: 终极合并脚本，包含所有修复功能
- **strategy2_smart_fix.py**: 智能修复策略
- **fix_negative_timestamp.py**: 专门修复时间戳问题

### 使用建议
- **日常使用**: 优先使用 `main.py --merge --ultimate`
- **问题排查**: 使用对应的分析工具
- **开发维护**: 核心逻辑在 `src/utils/video_merger.py`

#### 终极标准化合并 ⭐
```bash
# 使用终极标准化合并（推荐）
python main.py --merge ai_vanvan --ultimate

# aigf8728终极合并（生成title格式文件名）
python main.py --merge aigf8728 --ultimate
```

### 4. B站自动上传 🆕
```bash
# 上传aigf8728账户视频（自定义标题格式）
python main.py --upload --aigf8728

# 设置Chrome登录配置（首次使用）
python tools/upload_aigf8728.py
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
- `--ultimate` - 使用终极标准化合并

### 上传命令 🆕
- `--upload` - 启动B站上传任务
- `--aigf8728` - 使用aigf8728账户（支持自定义标题）

### 示例
```bash
# 下载最多20个视频
python main.py --download --ai_vanvan --limit 20

# 合并最新5个视频
python main.py --merge --aigf8728 --merge-limit 5

# 上传aigf8728视频到B站
python main.py --upload --aigf8728

# 完整工作流：下载→合并→上传
python main.py --download --aigf8728 --limit 10
python main.py --merge aigf8728 --ultimate
python main.py --upload --aigf8728
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
  },
  "aigf8728": {
    "instagram": {"username": "aigf8728"},
    "download_dir": "videos/downloads/aigf8728", 
    "folder_strategy": "date_blogger",
    "upload_settings": {
      "title_pattern": "ins你的海外第{序号}个女友:{博主ID}",
      "next_number": 6
    }
  }
}
```

### 文件夹策略
- `daily` - 按日期创建文件夹 (YYYY-MM-DD)
- `date_blogger` - 按日期+博主创建文件夹 🆕
- `blogger_daily` - 按博主+日期创建文件夹

### 上传配置 🆕
- `title_pattern` - 自定义标题格式，支持 {序号} 和 {博主ID} 变量
- `next_number` - 当前集数编号，上传成功后自动递增

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
| 智能文件命名 | ✅ 完成 | 基于标题格式的文件名 🆕 |
| 路径处理 | ✅ 完成 | Unicode问题已修复 |
| 进度显示 | ✅ 完成 | 单行进度条 |
| B站自动上传 | ✅ 完成 | 支持自定义标题格式 🆕 |
| Chrome配置管理 | ✅ 完成 | 持久化登录状态 🆕 |

## 🎯 aigf8728专属功能 🆕

### 自定义标题系统
- **格式**: `ins你的海外第{序号}个女友:{博主ID}`
- **自动编号**: 上传成功后序号自动递增
- **博主识别**: 智能提取视频中的博主ID

### 智能文件命名
- **合并文件**: 自动使用标题格式命名
- **示例**: `ins你的海外第6个女友_natasha_noel.mp4`
- **便于管理**: 文件名直接显示上传标题信息

### 首次设置
```bash
# 设置Chrome登录状态（仅需一次）
python tools/upload_aigf8728.py
```
按提示完成B站登录，程序会保存登录状态。

### 完整工作流
```bash
# 方法一：分步执行
python main.py --download --aigf8728 --limit 10
python main.py --merge aigf8728 --ultimate
python main.py --upload --aigf8728

# 方法二：批量处理
for /L %i in (1,1,3) do (
    python main.py --download --aigf8728 --limit 5
    python main.py --merge aigf8728 --ultimate  
    python main.py --upload --aigf8728
)
```

### 文件组织结构
```
videos/downloads/aigf8728/
├── 2025-09-04_natasha_noel/        # 按日期+博主分组
│   ├── natasha_noel_video1.mp4
│   └── natasha_noel_video2.mp4
└── videos/merged/aigf8728/
    └── ins你的海外第6个女友_natasha_noel.mp4  # 智能命名
```

### 标题效果示例
- **第6集**: `ins你的海外第6个女友:natasha_noel`
- **第7集**: `ins你的海外第7个女友:fitness_girl`
- **第8集**: `ins你的海外第8个女友:yoga_teacher`

---

# 📚 详细技术文档

## 🎬 视频合并系统详解

### 视频合并模式对比

| 模式 | 速度 | 质量 | 适用场景 | 处理时间 |
|------|------|------|----------|----------|
| 标准合并 | ⚡ 快速 | 保持原始 | 高质量视频 | 几秒钟 |
| 智能修复 | 🔧 中等 | 修复问题 | 有音频问题 | 1-3分钟 |
| 终极合并 | 🎯 较慢 | 完全标准化 | 严重问题视频 | 10-20分钟 |

### 技术参数详解

#### 视频标准化参数
```bash
# 视频编码参数
-c:v libx264          # H.264编码
-crf 23              # 恒定质量因子
-preset medium       # 编码速度
-profile:v high      # 编码配置
-level 4.0          # 编码级别  
-pix_fmt yuv420p    # 像素格式
-r 30               # 统一30fps
```

#### 音频标准化参数
```bash
# 音频编码参数
-c:a aac            # AAC编码
-b:a 128k          # 128kbps比特率
-ar 44100          # 44.1kHz采样率
-ac 2              # 双声道
-sample_fmt fltp   # 浮点采样
```

#### 时间戳修复参数
```bash
# 修复负数时间戳
-avoid_negative_ts make_zero
-fflags +genpts
```

### 视频质量诊断工具

#### 音频质量扫描
```bash
# 扫描所有视频音频质量
python scripts/analysis/complete_audio_scan.py

# 检查今日下载视频
python scripts/analysis/check_today_videos.py

# 深度分析问题视频
python scripts/analysis/deep_analyze_problem_video.py
```

#### 问题识别标准
- **音频比特率** < 50kbps - 需要修复
- **负数时间戳** - 导致播放卡顿
- **非标准编码** - 兼容性问题
- **分辨率不一致** - 需要标准化

### 合并策略选择指南

#### 何时使用标准合并？
- ✅ 所有视频质量良好
- ✅ 音频比特率 > 100kbps
- ✅ 无时间戳问题
- ✅ 分辨率基本一致

#### 何时使用终极合并？
- ⚠️ 存在音频质量问题
- ⚠️ 发现负数时间戳
- ⚠️ 分辨率差异很大
- ⚠️ 编码参数不一致

## 🏗️ 项目架构详解

### 核心目录结构
```
social-media-hub/
├── 📁 src/                       # 核心源代码
│   ├── 📁 platforms/             # 平台适配
│   │   ├── 📁 instagram/         # Instagram下载
│   │   └── 📁 bilibili/          # B站上传
│   ├── 📁 utils/                 # 工具模块
│   │   ├── 📄 video_merger.py    # 视频合并核心 ⭐
│   │   ├── 📄 folder_manager.py  # 文件管理
│   │   ├── 📄 logger.py          # 日志系统
│   │   └── 📄 path_utils.py      # 路径处理
│   └── 📁 accounts/              # 账户管理
├── 📁 scripts/                   # 独立工具脚本
│   ├── 📁 analysis/              # 视频分析工具 🔍
│   └── 📁 merge/                 # 合并处理工具 🔧
├── 📁 config/                    # 配置文件
├── 📁 logs/                      # 日志文件
├── 📁 videos/                    # 视频存储
│   ├── 📁 downloads/             # 原始下载
│   ├── 📁 merged/                # 合并输出
│   └── 📁 temp/                  # 临时文件
└── 📁 tools/                     # 外部工具
    └── 📁 profiles/              # 浏览器配置
```

### 核心模块说明

#### video_merger.py - 视频合并核心
- **功能**: 所有视频合并逻辑的核心实现
- **特性**: 支持标准合并和终极标准化
- **优化**: 智能检测视频质量并选择最佳策略

#### folder_manager.py - 文件管理系统
- **策略**: 支持多种文件夹组织策略
  - `daily`: 按日期分组 (YYYY-MM-DD)
  - `date_blogger`: 按日期+博主分组 (YYYY-MM-DD_博主名)
- **Unicode处理**: 自动修复Windows路径分隔符问题

#### logger.py - 日志记录系统
- **下载记录**: 详细记录每次下载的文件信息
- **错误跟踪**: 完整的错误堆栈和上下文信息
- **性能监控**: 下载速度和处理时间统计

## 🛠️ 高级配置指南

### 账户配置详解 (config/accounts.json)

#### ai_vanvan账户配置
```json
{
  "ai_vanvan": {
    "name": "ai_vanvan",
    "platform": "instagram",
    "username": "ai_vanvan", 
    "folder_strategy": "daily",
    "title_prefix": "海外离大谱#",
    "firefox_profile": "370tsjzy.default-release",
    "download_safety": {
      "max_posts_per_session": 50,    # 单次最大下载数
      "request_delay": 2               # 请求间延迟(秒)
    }
  }
}
```

#### aigf8728账户配置
```json
{
  "aigf8728": {
    "name": "aigf8728",
    "platform": "instagram",
    "username": "aigf8728",
    "folder_strategy": "date_blogger",   # 按日期+博主分组
    "firefox_profile": "y34y4ur5.aigf8728_instagram",
    "bilibili": {
      "profile_name": "aigf8728_profile",
      "chrome_profile_path": "c:\\...\\chrome_profile_aigf8728"
    },
    "upload_settings": {
      "title_pattern": "ins你的海外第{序号}个女友:{博主ID}",
      "next_number": 6               # 当前集数
    },
    "download_safety": {
      "max_posts_per_session": 50,
      "request_delay": 2
    }
  }
}
```

### 文件夹策略对比

| 策略 | 格式 | 适用场景 | 示例 |
|------|------|----------|------|
| `daily` | `YYYY-MM-DD/` | 按日期管理 | `2025-09-04/` |
| `date_blogger` | `YYYY-MM-DD_博主名/` | 精细管理 | `2025-09-04_natasha_noel/` |

## 🔧 故障排查指南

### 常见问题及解决方案

#### 1. Unicode路径问题
**现象**: 文件保存到错误路径，包含 `﹨` 字符
```
videos﹨downloads﹨aigf8728﹨...  # 错误路径
```

**解决方案**:
- ✅ 已在所有文件创建前应用Unicode清理
- ✅ 自动检测并修复历史错误路径
- ✅ 使用 `clean_unicode_path()` 函数标准化

#### 2. 下载检测失败
**现象**: 下载完成但程序显示失败

**排查步骤**:
```bash
# 1. 检查文件权限
ls -la videos/downloads/

# 2. 验证时间戳检查逻辑
python -c "import time; print(time.time())"

# 3. 清理浏览器缓存
rm -rf temp/*/
```

#### 3. B站上传失败
**现象**: Chrome启动失败或上传中断

**解决方案**:
```bash
# 1. 重新设置Chrome配置
python tools/upload_aigf8728.py

# 2. 检查视频格式
ffprobe video.mp4

# 3. 验证网络连接
ping bilibili.com
```

#### 4. 视频合并问题
**现象**: 合并后播放卡顿或无声音

**诊断命令**:
```bash
# 扫描视频质量
python scripts/analysis/complete_audio_scan.py

# 深度分析问题
python scripts/analysis/deep_analyze_problem_video.py

# 使用终极合并修复
python main.py --merge account_name --ultimate
```

### 调试模式

#### 启用详细日志
```bash
# 设置调试级别
export LOG_LEVEL=DEBUG

# 运行时显示详细信息
python main.py --download --aigf8728 --verbose
```

#### 检查系统状态
```bash
# 验证环境配置
python main.py --check-config

# 测试文件权限
python main.py --check-permissions

# 验证外部工具
ffmpeg -version
```

## 🚀 性能优化建议

### 下载优化
- **批量大小**: 建议每批5-10个视频
- **请求延迟**: 2-3秒避免被限制
- **并发控制**: 单账户单线程避免冲突

### 合并优化
- **磁盘空间**: 确保有足够临时空间
- **CPU使用**: 终极合并会占用较多CPU
- **内存管理**: 大文件合并注意内存使用

### 上传优化
- **网络稳定**: 确保稳定的网络连接
- **文件格式**: MP4格式兼容性最好
- **分辨率**: 720p或1080p为最佳选择

## 📖 开发指南

### 添加新功能
1. **在src/中添加核心逻辑**
2. **在scripts/中添加独立工具**
3. **更新配置文件格式**
4. **添加相应的测试用例**

### 代码规范
- **函数命名**: 使用描述性的英文命名
- **注释**: 关键逻辑必须有中文注释
- **错误处理**: 所有外部调用必须有异常处理
- **日志记录**: 重要操作必须记录日志

### 测试建议
- **单元测试**: 核心函数要有测试覆盖
- **集成测试**: 端到端流程验证
- **性能测试**: 大文件处理性能验证

## 🤝 贡献指南

1. **报告问题**: 使用 `python tools/add_bug_record.py` 记录bug
2. **提交修复**: 更新相应的文档和测试
3. **代码风格**: 遵循项目现有代码规范
4. **文档更新**: 修改功能时同步更新文档

## 📄 许可证

本项目为内部工具，请遵守相关平台的使用条款。

---

**📝 最后更新**: 2025-01-15  
**🔧 技术栈**: Python 3.11, instaloader, ffmpeg, selenium  
**💻 平台**: Windows (主要), Linux/Mac (兼容)  
**🆕 新增**: aigf8728自定义标题上传、智能文件命名、B站自动化工作流
