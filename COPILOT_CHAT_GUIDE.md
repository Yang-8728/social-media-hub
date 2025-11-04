# Quick Start - 新 Chat 使用指南

## 🚀 开始新的 Copilot Chat 会话

### 第一句话模板
```
@workspace 继续开发 social-media-hub，请先阅读：
- DEVELOPMENT_LOG.md (了解当前状态)
- .github/copilot-instructions.md (了解项目架构)

当前任务：[你要做的事情]
```

### 常用上下文引用
- `@workspace` - 整个工作区
- `#file:DEVELOPMENT_LOG.md` - 引用特定文件
- `#terminalLastCommand` - 上一条终端命令
- `#terminalSelection` - 选中的终端输出

### 示例对话

#### 场景1: 调试问题
```
@workspace 容器 social-media-hub-merger-1 报错，
查看 DEVELOPMENT_LOG.md 中的已知问题，
帮我排查和修复。
```

#### 场景2: 添加新功能
```
@workspace 我要添加自动重试功能，
参考 .github/copilot-instructions.md 中的架构，
应该在哪个服务中实现？
```

#### 场景3: 继续上次工作
```
@workspace 上次修复了 merger 的 type 字段问题，
现在需要测试是否工作正常。
参考 DEVELOPMENT_LOG.md 中的修复记录。
```

## 📝 每次结束前要做的

更新 `DEVELOPMENT_LOG.md`：
```markdown
### [日期] - [完成的任务]
- 修改了：XXX
- 解决了：XXX  
- 发现问题：XXX
- 下一步：XXX
```

## 🔄 Chat 生命周期建议

| 情况 | 建议 | 原因 |
|------|------|------|
| 对话 > 50 轮 | 新开 chat | Token 限制 |
| 出现工具失效 | 新开 chat | 可能触发限制 |
| 每天开始工作 | 新开 chat | 保持上下文清晰 |
| 切换功能模块 | 新开 chat | 避免上下文混淆 |
| 解决一个 bug | 可继续 | 保持连贯性 |

