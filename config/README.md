# config/ - 配置文件目录

这个目录包含项目的所有配置文件，用于管理账户、设置和环境参数。

## 📁 目录结构

```
config/
└── accounts.json           # 账户配置文件
```

## 🔧 配置文件说明

### accounts.json - 账户管理
存储各社交媒体平台的账户信息和配置：

```json
{
  "accounts": {
    "instagram": {
      "username": "your_username",
      "settings": {
        "download_path": "data/downloads",
        "max_retries": 3,
        "delay_seconds": 2
      }
    }
  }
}
```

## 🛡️ 安全注意事项

- **⚠️ 敏感信息**: 不要在配置文件中直接存储密码
- **🔐 凭据管理**: 建议使用环境变量或安全的凭据存储
- **📋 版本控制**: 确保敏感配置不被提交到Git仓库

## 🚀 配置最佳实践

1. **环境分离**: 为不同环境（开发/生产）创建不同配置
2. **默认值**: 为所有配置项提供合理的默认值
3. **验证**: 在应用启动时验证配置的完整性
4. **文档**: 为每个配置项添加清晰的注释

## 📝 配置模板

如需添加新的配置文件，请参考以下结构：

```json
{
  "platform_name": {
    "account_info": {
      "username": "required",
      "email": "optional"
    },
    "download_settings": {
      "quality": "high",
      "format": "mp4",
      "max_size_mb": 100
    },
    "behavior_settings": {
      "delay_between_downloads": 2,
      "retry_count": 3,
      "timeout_seconds": 30
    }
  }
}
```

## 🔍 使用说明

- 修改配置后需要重启应用程序
- 支持热重载的配置项会在代码中特别标注
- 配置错误会在应用启动时显示详细错误信息
