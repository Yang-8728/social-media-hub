# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.1] - 2025-09-02

### 修复 🔧
- � 修复视频合并器中 Logger debug 方法错误
- 📊 修复工作流处理错误视频数量问题（168→11个视频）
- 🎯 优化合并逻辑，只处理今天的视频
- 🧹 移除冗余的智能模式选择逻辑

### 删除 ❌
- 🗑️ 智能合并模式（统一使用终极模式）
- 📂 过时的兼容性包装方法
- 🧽 清理 `smart_merge_test.py` 和 `strategy2_smart_fix.py`

### 更改 🔄
- 🎯 简化合并方法命名（移除"ultimate"前缀）
- 📝 更新Chrome日志设置，输出更清洁
- 🔄 改进上传失败时的序列号回滚机制
- 📋 增强工作流中的合并模式描述
- 🧰 更新 .gitignore 规则，忽略临时调试文件

### 技术细节 ⚙️
- **合并逻辑**: 现在只处理今天的视频，具备完善的重复检测
- **标准化**: 统一终极模式确保100%兼容B站上传要求
- **代码质量**: 删除584行冗余代码，新增75行改进
- **文件管理**: 更好的日志和记录文件组织结构

## [2.0.0] - 2025-08-31

### Added
- 🎉 Complete automation system: download → merge → upload workflow
- One-command execution: `python main.py --ai_vanvan`
- Enterprise-level code architecture
- Comprehensive project cleanup (140+ files archived)

### Changed
- Project structure completely reorganized
- Root directory cleaned and standardized

## [1.5.0] - 2025-08-31

### Added
- 🏷️ Smart title generation with "ins海外离大谱#序号" format
- Automatic episode number management

## [1.4.0] - 2025-08-31

### Fixed
- 🎯 Bilibili category selection optimization
- Prevent accidental clicks on "分区合集" option
- Improved upload success rate

## [1.3.0] - 2025-08-31

### Added
- 🚀 Complete Bilibili upload automation
- Upload success detection
- Automatic browser closure after completion

## [1.2.1] - 2025-08-31

### Fixed
- 🔧 "立即投稿" button click functionality
- Restored complete upload and submission workflow
- ActionChains method implementation

## [1.2.0] - 2025-08-31

### Added
- 📤 Auto-submit functionality
- Smart "立即投稿" button detection
- Multiple text fallback options
- Success signal detection

## [1.1.0] - 2025-08-31

### Added
- 🔗 Bilibili upload integration
- Unified architecture
- Chrome driver fixes
- Unified CLI interface

## [1.0.0] - 2025-08-31

### Added
- 📁 Project standardization and restructuring
- Complete open-source project structure
- Standardized code organization
- Documentation system

## [0.4.0] - 2025-08-31

### Improved
- ⚡ Instagram detection optimization
- Smart sync detection
- Performance improvements

## [0.3.0] - 2025-08-31

### Fixed
- 🔧 Unicode path issues
- Instagram download path problems
- Detection logic optimization

## [0.2.0] - 2025-08-31

### Added
- 🎬 Video merging functionality
- Complete VideoMerger implementation
- FFmpeg integration
- Time-based video ordering

## [0.1.0] - 2025-08-31

### Added
- 🌱 Initial project version
- Instagram downloader migration
- Basic project architecture
- Account configuration system

If upgrading from earlier versions:
1. Run `tools/scripts/fix_unicode_paths.py` to migrate any files in Unicode paths
2. Update any custom scripts to use the new directory structure
3. Check that FFmpeg tools are properly extracted in `tools/ffmpeg/`

## Contributors

- Yang-8728 - Initial development and maintenance

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
