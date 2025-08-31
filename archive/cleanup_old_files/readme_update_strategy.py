"""
README文件未来更新策略说明
什么时候会更新根目录README.md和docs/README.md
"""

print("📋 === README文件更新策略 ===")
print()

print("✅ 我会在以下情况更新README文件:")
print()

# 根目录README.md更新场景
print("🏠 根目录README.md更新时机:")
root_readme_updates = [
    {
        "场景": "添加新功能",
        "示例": "支持新的社交媒体平台(如TikTok、微博)",
        "更新内容": "在'主要特性'部分添加新平台支持"
    },
    {
        "场景": "改进安装流程",
        "示例": "简化环境配置步骤或添加Docker支持",
        "更新内容": "更新'快速开始'和'环境准备'部分"
    },
    {
        "场景": "修复重要问题",
        "示例": "解决关键Bug或兼容性问题",
        "更新内容": "在故障排除部分添加解决方案"
    },
    {
        "场景": "API或使用方式变更",
        "示例": "命令行参数改变或配置文件格式更新",
        "更新内容": "更新使用示例和命令说明"
    },
    {
        "场景": "项目重大里程碑",
        "示例": "发布1.0版本、获得重要认证",
        "更新内容": "更新项目介绍和成就展示"
    }
]

for update in root_readme_updates:
    print(f"  📝 {update['场景']}")
    print(f"     例子: {update['示例']}")
    print(f"     更新: {update['更新内容']}")
    print()

# docs/README.md更新场景
print("📚 docs/README.md更新时机:")
docs_readme_updates = [
    {
        "场景": "添加新文档",
        "示例": "创建API文档、架构设计文档",
        "更新内容": "在文档列表中添加新文档说明"
    },
    {
        "场景": "重组文档结构",
        "示例": "按功能重新分类文档",
        "更新内容": "更新目录结构和导航链接"
    },
    {
        "场景": "文档标准变更",
        "示例": "采用新的文档格式或风格",
        "更新内容": "更新文档格式规范说明"
    },
    {
        "场景": "移动重要文档",
        "示例": "像今天移动BUGFIX文档一样",
        "更新内容": "更新文档位置引用和说明"
    }
]

for update in docs_readme_updates:
    print(f"  📝 {update['场景']}")
    print(f"     例子: {update['示例']}")
    print(f"     更新: {update['更新内容']}")
    print()

print("="*60)
print("🎯 更新原则")
print("="*60)

principles = [
    "📱 根目录README保持简洁，突出核心价值",
    "📚 docs/README详细完整，便于深入了解",
    "🔄 及时更新，保持信息准确性",
    "👥 考虑用户体验，使用清晰的语言",
    "🎯 重点突出，避免信息过载",
    "🔗 保持内部链接的有效性"
]

for principle in principles:
    print(f"  {principle}")

print()
print("⚠️ 什么时候不会更新:")
no_update_scenarios = [
    "小的代码修改或Bug修复(除非影响使用方式)",
    "内部重构或性能优化(用户无感知)",
    "测试代码的变更",
    "注释或文档字符串的小改动",
    "临时功能或实验性功能"
]

for scenario in no_update_scenarios:
    print(f"  ❌ {scenario}")

print()
print("🤝 协作建议:")
collaboration_tips = [
    "如果您添加新功能，请提醒我更新README",
    "如果您发现README信息过时，可以指出来",
    "重要功能变更时，我们一起讨论如何更新文档",
    "保持README的专业性和用户友好性"
]

for tip in collaboration_tips:
    print(f"  💡 {tip}")

print()
print("🎯 总结:")
print("  - 我会根据项目发展适时更新README")
print("  - 重点关注用户体验和信息准确性")
print("  - 保持两个README的不同定位和作用")
print("  - 欢迎您提出更新建议和反馈")
