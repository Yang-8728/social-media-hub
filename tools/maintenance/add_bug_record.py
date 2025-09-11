#!/usr/bin/env python3
"""
Bug记录助手
快速添加新的bug记录到文档中

使用方法:
python tools/add_bug_record.py
"""
import os
import re
from datetime import datetime


def get_next_bug_number():
    """获取下一个bug编号"""
    bug_file = "docs/Bug修复记录.md"
    
    if not os.path.exists(bug_file):
        return 1
    
    with open(bug_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有bug编号
    bug_numbers = re.findall(r'### #(\d+) -', content)
    
    if not bug_numbers:
        return 1
    
    return max(int(num) for num in bug_numbers) + 1


def create_bug_template(bug_number, title, severity, discovery_method):
    """创建bug记录模板"""
    date = datetime.now().strftime("%Y-%m-%d")
    
    severity_emoji = {
        "高危": "🔴",
        "中等": "🟡", 
        "低危": "🟢"
    }
    
    template = f"""
### #{bug_number:03d} - {title}
**日期**: {date}  
**严重程度**: {severity_emoji.get(severity, "🟡")} {severity}  
**发现方式**: {discovery_method}

#### 问题描述
[详细描述问题现象和影响]

#### 问题症状
- [ ] 症状1
- [ ] 症状2

#### 根本原因
[分析问题的根本原因]

#### 解决方案
[详细的解决步骤]

#### 修复文件
- `文件路径` (新建/修改)

#### 预防措施
- [ ] 预防措施1
- [ ] 预防措施2

#### 相关资料
[链接到相关文档或代码]

---
"""
    return template


def add_bug_record():
    """交互式添加bug记录"""
    print("🐛 Bug记录助手")
    print("=" * 30)
    
    # 获取基本信息
    title = input("Bug标题: ").strip()
    if not title:
        print("❌ 标题不能为空")
        return
    
    print("\n严重程度:")
    print("1. 🔴 高危")
    print("2. 🟡 中等") 
    print("3. 🟢 低危")
    
    severity_choice = input("选择严重程度 (1-3): ").strip()
    severity_map = {"1": "高危", "2": "中等", "3": "低危"}
    severity = severity_map.get(severity_choice, "中等")
    
    discovery_method = input("发现方式: ").strip()
    if not discovery_method:
        discovery_method = "开发过程中发现"
    
    # 生成bug编号和模板
    bug_number = get_next_bug_number()
    template = create_bug_template(bug_number, title, severity, discovery_method)
    
    # 读取现有文档
    bug_file = "docs/Bug修复记录.md"
    with open(bug_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 在模板部分之前插入新记录
    template_marker = "## 📝 修复模板"
    if template_marker in content:
        parts = content.split(template_marker)
        new_content = parts[0] + template + "\n" + template_marker + parts[1]
    else:
        # 如果没有找到标记，就添加到文档末尾
        new_content = content + template
    
    # 写回文档
    with open(bug_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\n✅ 已添加Bug记录 #{bug_number:03d}")
    print(f"📝 请编辑 {bug_file} 完善详细信息")
    
    # 更新统计信息
    update_statistics(new_content)


def update_statistics(content):
    """更新统计信息"""
    # 统计不同类型的bug数量
    total_bugs = len(re.findall(r'### #\d+ -', content))
    high_severity = len(re.findall(r'🔴 高危', content))
    medium_severity = len(re.findall(r'🟡 中等', content))
    low_severity = len(re.findall(r'🟢 低危', content))
    
    # 查找统计信息部分并更新
    stats_pattern = r'(## 📊 统计信息.*?\*\*总bug数\*\*: )\d+(.*?\*\*高危bug\*\*: )\d+(.*?\*\*中等bug\*\*: )\d+(.*?\*\*低危bug\*\*: )\d+'
    
    new_stats = f'\\g<1>{total_bugs}\\g<2>{high_severity}\\g<3>{medium_severity}\\g<4>{low_severity}'
    
    updated_content = re.sub(stats_pattern, new_stats, content, flags=re.DOTALL)
    
    # 写回文档
    with open("docs/Bug修复记录.md", 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"📊 统计信息已更新: 总计{total_bugs}个bug")


if __name__ == "__main__":
    if not os.path.exists("docs/Bug修复记录.md"):
        print("❌ 找不到Bug修复记录文档")
        print("请确保在项目根目录运行此脚本")
    else:
        add_bug_record()
