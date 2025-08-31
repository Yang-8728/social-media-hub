# 🔄 双账户系统架构设计

## 🎯 账户差异化管理

### 账户配置差异：
```json
{
  "accounts": {
    "ai_vanvan": {
      "instagram": {
        "username": "ai_vanvan",
        "session_file": "ai_vanvan_session"
      },
      "bilibili": {
        "chrome_profile": "chrome_profile_ai_vanvan",
        "title_prefix": "海外离大谱#",
        "serial_file": "serial_number_ai_vanvan.txt",
        "tags": ["Instagram", "海外", "日常"],
        "category": "生活"
      },
      "storage": {
        "download_folder": "ai_vanvan",
        "merged_folder": "ai_vanvan"
      }
    },
    "aigf8728": {
      "instagram": {
        "username": "aigf8728", 
        "session_file": "aigf8728_session"
      },
      "bilibili": {
        "chrome_profile": "chrome_profile_aigf8728",
        "title_prefix": "ins你的海外女友#",
        "serial_file": "serial_number_aigf8728.txt",
        "tags": ["Instagram", "美女", "海外"],
        "category": "生活"
      },
      "storage": {
        "download_folder": "aigf8728",
        "merged_folder": "aigf8728"
      }
    }
  }
}
```

## 📁 项目结构规划

### 工具目录：
```
tools/
├── chrome/                     # Chrome浏览器和驱动
│   ├── chrome-win64/
│   │   └── chrome.exe
│   └── chromedriver-win64/
│       └── chromedriver.exe
├── ffmpeg/                     # 视频处理工具
│   └── bin/
│       ├── ffmpeg.exe
│       └── ffprobe.exe
└── profiles/                   # 浏览器配置文件
    ├── chrome_profile_ai_vanvan/
    └── chrome_profile_aigf8728/
```

### 代码架构：
```
src/
├── accounts/
│   ├── __init__.py
│   ├── account_manager.py      # 账户管理器
│   └── configs/
│       ├── ai_vanvan.py        # ai_vanvan特定配置
│       └── aigf8728.py         # aigf8728特定配置
├── platforms/
│   ├── instagram/
│   │   └── downloader.py
│   └── bilibili/
│       ├── __init__.py
│       ├── uploader.py         # B站上传器
│       ├── title_generator.py  # 标题生成器
│       └── browser_manager.py  # 浏览器管理
└── utils/
    ├── folder_manager.py
    ├── video_merger.py
    └── logger.py
```

## 🚀 实现步骤

### Step 1: 复制Chrome工具
```bash
从 insDownloader 复制：
- tools/chrome-win64/ -> social-media-hub/tools/chrome/
- tools/chromedriver-win64/ -> social-media-hub/tools/chrome/
- chrome_profile_ai_vanvan/ -> social-media-hub/tools/profiles/
```

### Step 2: 创建账户特定配置
```python
# src/accounts/configs/ai_vanvan.py
class AiVanvanConfig:
    # Instagram配置
    INSTAGRAM_USERNAME = "ai_vanvan"
    SESSION_FILE = "ai_vanvan_session"
    
    # B站上传配置
    CHROME_PROFILE = "chrome_profile_ai_vanvan"
    TITLE_PREFIX = "海外离大谱#"
    SERIAL_FILE = "serial_number_ai_vanvan.txt"
    TAGS = ["Instagram", "海外", "日常"]
    CATEGORY = "生活"
    
    # 存储配置
    DOWNLOAD_FOLDER = "ai_vanvan"
    MERGED_FOLDER = "ai_vanvan"

# src/accounts/configs/aigf8728.py  
class Aigf8728Config:
    # Instagram配置
    INSTAGRAM_USERNAME = "aigf8728"
    SESSION_FILE = "aigf8728_session"
    
    # B站上传配置
    CHROME_PROFILE = "chrome_profile_aigf8728"
    TITLE_PREFIX = "ins你的海外女友#"
    SERIAL_FILE = "serial_number_aigf8728.txt"
    TAGS = ["Instagram", "美女", "海外"]
    CATEGORY = "生活"
    
    # 存储配置
    DOWNLOAD_FOLDER = "aigf8728"
    MERGED_FOLDER = "aigf8728"
```

### Step 3: 账户管理器
```python
# src/accounts/account_manager.py
class AccountManager:
    def __init__(self):
        self.configs = {
            'ai_vanvan': AiVanvanConfig(),
            'aigf8728': Aigf8728Config()
        }
    
    def get_config(self, account_name):
        return self.configs.get(account_name)
    
    def get_all_accounts(self):
        return list(self.configs.keys())
```

### Step 4: B站上传器
```python
# src/platforms/bilibili/uploader.py
class BilibiliUploader:
    def __init__(self, account_config):
        self.config = account_config
        self.browser_manager = BrowserManager(account_config)
    
    def upload_video(self, video_path):
        # 使用账户特定配置上传视频
        pass
    
    def generate_title(self):
        # 使用账户特定的标题生成逻辑
        pass
```

## 💡 命令行界面

### 账户特定命令：
```bash
# ai_vanvan账户操作
python main.py --upload --account ai_vanvan
python main.py --download --account ai_vanvan  
python main.py --merge --account ai_vanvan

# aigf8728账户操作
python main.py --upload --account aigf8728
python main.py --download --account aigf8728
python main.py --merge --account aigf8728

# 批量操作
python main.py --upload --all
python main.py --auto --account ai_vanvan
```

## 🎯 差异化特性

### ai_vanvan特色：
- 标题：海外离大谱#XX
- 标签：海外、日常、Instagram
- Chrome配置：独立的ai_vanvan配置文件
- 序列号：独立的序列号文件

### aigf8728特色：  
- 标题：ins你的海外女友#XX
- 标签：美女、海外、Instagram
- Chrome配置：独立的aigf8728配置文件
- 序列号：独立的序列号文件

这样设计的优势：
1. ✅ **完全隔离** - 两个账户完全独立
2. ✅ **易于扩展** - 可以轻松添加新账户
3. ✅ **配置清晰** - 每个账户的配置一目了然
4. ✅ **代码复用** - 共享核心逻辑，差异化配置
5. ✅ **维护简单** - 修改一个账户不影响另一个
