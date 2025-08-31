# Features Documentation

## 🚀 Core Features

### 1. 全流程自动化
- **命令**: `python main.py --ai_vanvan`
- **功能**: 下载 → 合并 → 上传一键完成
- **支持**: 多账号管理

### 2. 智能标题生成
- **格式**: "ins海外离大谱#序号"
- **功能**: 自动递增序号管理
- **特性**: 标题规范化

### 3. B站分区选择优化
- **问题**: 避免误点击"分区合集"选项
- **解决**: 智能分区选择逻辑
- **结果**: 提升上传成功率

### 4. 上传功能完整自动化
- **检测**: 稿件投递成功检测
- **流程**: 自动关闭浏览器
- **兜底**: 多种文案识别

## 🎯 Usage Examples

```bash
# 一键全流程
python main.py --ai_vanvan

# 分步执行
python main.py --download --ai_vanvan
python main.py --merge --ai_vanvan  
python main.py --upload path/to/video.mp4
```

## 📊 System Requirements

- Python 3.11+
- FFmpeg (video processing)
- Chrome/Chromium (upload automation)
- Windows 10+ (path handling optimized)
