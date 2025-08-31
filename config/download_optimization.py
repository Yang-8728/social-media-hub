"""
Instagram下载性能优化配置
"""

# ai_vanvan账户优化建议
AI_VANVAN_OPTIMIZED_CONFIG = {
    "download_safety": {
        "max_posts_per_session": 30,  # 降低到30，更安全
        "request_delay": 3,          # 增加到3秒，避免被限制
        "max_retries": 5,            # 增加重试次数
        "session_timeout": 1800,     # 30分钟session超时
        "daily_limit": 100           # 每日下载限制
    },
    "download_optimization": {
        "batch_size": 5,             # 每批处理5个视频
        "batch_delay": 10,           # 批次间延迟10秒
        "smart_skip": True,          # 智能跳过已下载
        "metadata_check": True,      # 启用元数据检查
        "progress_report": True      # 详细进度报告
    },
    "file_management": {
        "auto_cleanup": True,        # 自动清理临时文件
        "duplicate_check": True,     # 重复文件检查
        "path_validation": True,     # 路径验证
        "unicode_fix": True          # Unicode路径修复
    },
    "quality_settings": {
        "prefer_video": True,        # 优先下载视频
        "save_metadata": True,       # 保存元数据
        "save_comments": False,      # 不保存评论（节省空间）
        "compress_json": True        # 压缩JSON文件
    }
}

# 下载策略优化
DOWNLOAD_STRATEGIES = {
    "conservative": {
        "max_posts": 10,
        "delay": 5,
        "description": "保守策略，适合首次使用或担心被限制"
    },
    "balanced": {
        "max_posts": 30,
        "delay": 3,
        "description": "平衡策略，推荐日常使用"
    },
    "aggressive": {
        "max_posts": 50,
        "delay": 2,
        "description": "激进策略，适合稳定网络和信任的账号"
    }
}
