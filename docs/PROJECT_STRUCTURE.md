# 项目结构说明

## 目录结构

```
social-media-hub/
├── 📁 src/                       # 核心源代码
│   ├── 📁 utils/
│   │   ├── 📄 video_merger.py    # 视频合并核心模块 ⭐
│   │   ├── 📄 logger.py          # 日志系统
│   │   ├── 📄 folder_manager.py  # 文件管理
│   │   └── 📄 ...
│   └── 📁 ...
├── 📁 scripts/                   # 工具脚本
│   ├── 📁 analysis/              # 视频分析工具 🔍
│   │   ├── 📄 complete_audio_scan.py         # 完整音频扫描
│   │   ├── 📄 check_today_videos.py          # 视频质量检查
│   │   ├── 📄 analyze_audio_strategy.py      # 策略分析
│   │   ├── 📄 deep_analyze_problem_video.py  # 深度问题分析
│   │   ├── 📄 verify_ultimate_result.py      # 结果验证
│   │   └── 📄 ...
│   └── 📁 merge/                 # 合并工具 🔧
│       ├── 📄 ultimate_merge_script.py       # 终极合并脚本 ⭐
│       ├── 📄 strategy2_smart_fix.py         # 智能修复
│       ├── 📄 merge_fixed_proper.py          # 基础合并
│       ├── 📄 fix_negative_timestamp.py      # 时间戳修复
│       └── 📄 ...
├── 📁 docs/                      # 文档 📚
│   ├── 📄 VIDEO_MERGE_GUIDE.md   # 视频合并指南
│   ├── 📄 PROJECT_STRUCTURE.md   # 项目结构说明
│   └── 📄 ...
├── 📁 temp/                      # 临时文件 🗃️
├── 📁 tools/                     # 外部工具
│   └── 📁 ffmpeg/                # FFmpeg工具包
├── 📁 videos/                    # 视频存储
│   └── 📁 downloads/             # 下载视频
│       └── 📁 ai_vanvan/         # 账号目录
│           └── 📁 2025-09-01/    # 日期目录
├── 📄 main.py                    # 主程序入口 🚀
├── 📄 requirements.txt           # 依赖包
└── 📄 README.md                  # 项目说明
```

## 文件说明

### 核心模块
- **video_merger.py**: 视频合并的核心实现，包含所有合并逻辑
- **main.py**: 程序主入口，命令行界面

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

### 文档 (docs/)
- **VIDEO_MERGE_GUIDE.md**: 完整的视频合并使用指南
- **PROJECT_STRUCTURE.md**: 项目结构说明文档

## 清理说明

### 已移动的文件
从根目录移动到对应的scripts子目录中的文件：

**分析类脚本** → `scripts/analysis/`
- complete_audio_scan.py
- check_*.py (6个文件)
- analyze_*.py (3个文件)
- *problem*.py (4个文件)
- verify_*.py (1个文件)

**合并类脚本** → `scripts/merge/`
- merge_*.py (2个文件)
- strategy2_*.py (2个文件)
- ultimate_merge_script.py
- fix_*.py (2个文件)

### 保留在根目录的文件
- main.py (主程序)
- requirements.txt (依赖)
- README.md (说明)
- 配置文件
- 核心业务模块

## 使用建议

### 日常使用
1. 分析视频: 使用 `scripts/analysis/` 中的工具
2. 合并视频: 优先使用 `main.py --merge --ultimate`
3. 问题排查: 使用对应的分析工具

### 开发维护
1. 核心逻辑在 `src/utils/video_merger.py`
2. 独立工具在 `scripts/` 目录
3. 文档在 `docs/` 目录

### 临时文件
- 所有临时文件统一放在 `temp/` 目录
- 脚本会自动清理临时文件
- 可以手动删除整个 `temp/` 目录
