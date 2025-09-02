# 视频合并系统文档

## 概述

本项目提供了完整的Instagram视频下载和合并解决方案，包含高级的视频标准化和修复功能。

## 项目结构

```
social-media-hub/
├── src/                          # 核心源代码
│   ├── utils/
│   │   └── video_merger.py       # 视频合并核心模块
│   └── ...
├── scripts/                      # 工具脚本
│   ├── analysis/                 # 视频分析脚本
│   │   ├── complete_audio_scan.py           # 完整音频质量扫描
│   │   ├── check_today_videos.py            # 今日视频检查
│   │   ├── analyze_audio_strategy.py        # 音频处理策略分析
│   │   └── ...
│   └── merge/                    # 合并相关脚本
│       ├── ultimate_merge_script.py         # 终极合并脚本
│       ├── strategy2_smart_fix.py           # 智能修复合并
│       └── ...
├── docs/                         # 文档目录
├── temp/                         # 临时文件目录
├── tools/                        # 外部工具
│   └── ffmpeg/                   # FFmpeg工具
├── videos/                       # 视频存储
│   └── downloads/                # 下载的视频
└── main.py                       # 主程序入口
```

## 核心功能

### 1. 视频合并功能

#### 标准合并
```bash
python main.py --merge account_name --limit 10
```

#### 终极标准化合并
```bash
python main.py --merge account_name --ultimate
```

### 2. 视频标准化功能

#### 功能特性
- **时间戳修复**: 自动修复负数时间戳问题
- **音频标准化**: 统一转换为AAC 128kbps
- **视频标准化**: 统一分辨率、帧率和编码参数
- **质量保证**: 使用高质量编码设置

#### 技术参数
- **视频编码**: H.264 (libx264)
- **音频编码**: AAC
- **分辨率**: 自动检测主要分辨率
- **帧率**: 统一30fps
- **音频比特率**: 128kbps
- **采样率**: 44100Hz

### 3. 问题诊断工具

#### 音频质量扫描
```bash
python scripts/analysis/complete_audio_scan.py
```

#### 问题视频分析
```bash
python scripts/analysis/deep_analyze_problem_video.py
```

## 使用指南

### 基本合并流程

1. **扫描视频质量**
   ```bash
   python scripts/analysis/complete_audio_scan.py
   ```

2. **选择合并策略**
   - 普通合并: 适用于质量良好的视频
   - 终极合并: 适用于有问题的视频

3. **执行合并**
   ```bash
   # 普通合并
   python main.py --merge ai_vanvan --limit 5
   
   # 终极合并
   python main.py --merge ai_vanvan --ultimate
   ```

### 问题排查流程

1. **识别问题视频**
   - 音频比特率 < 50kbps
   - 负数时间戳
   - 非标准编码参数

2. **选择修复策略**
   - 方案1: 统一处理所有视频
   - 方案2: 只修复问题视频
   - 终极方案: 完全标准化

3. **验证修复效果**
   ```bash
   python scripts/analysis/verify_ultimate_result.py
   ```

## 技术细节

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

## 常见问题

### Q: 合并后的视频在某个时间点卡住？
A: 通常是因为负数时间戳问题，使用终极合并模式可以解决。

### Q: 音频质量差？
A: 检查原视频的音频比特率，使用音频标准化功能提升到128kbps。

### Q: 视频大小差异很大？
A: 使用完全标准化模式可以统一所有参数，但会增加文件大小。

## 性能优化

### 处理速度
- 普通合并: 几秒钟
- 智能修复: 1-3分钟
- 终极标准化: 10-20分钟

### 文件大小
- 原始合并: 保持原始大小
- 标准化合并: 可能增加20-50%
- 终极合并: 统一质量，大小可控

## 更新日志

### v2.0 (2025-09-02)
- 添加终极标准化功能
- 修复负数时间戳问题
- 重构项目文件结构
- 完善文档和工具脚本

### v1.0
- 基础视频合并功能
- 简单的分辨率标准化
- 基本的错误处理
