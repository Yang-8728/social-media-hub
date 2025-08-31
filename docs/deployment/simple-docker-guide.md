# 🐳 Social Media Hub 简单Docker化

## 基于现有项目的Docker配置

### 1. 简单的 Dockerfile
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖 (Firefox用于session，FFmpeg用于视频处理)
RUN apt-get update && apt-get install -y \
    firefox-esr \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目
COPY . .

# 创建必要的目录 (基于你现有的结构)
RUN mkdir -p data/downloads data/merged logs temp config

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import os; exit(0 if os.path.exists('main.py') else 1)"

# 默认命令
CMD ["python", "main.py", "--help"]
```

### 2. 超简单的 docker-compose.yml
```yaml
# docker-compose.yml
version: '3.8'

services:
  social-media-hub:
    build: .
    container_name: social-media-hub
    volumes:
      # 挂载数据目录，保持数据持久化
      - ./data:/app/data
      - ./logs:/app/logs  
      - ./config:/app/config
      - ./temp:/app/temp
      # 如果你有videos目录，也挂载上
      - ./videos:/app/videos
    environment:
      - PYTHONUNBUFFERED=1
    # 使用host网络，方便访问Instagram
    network_mode: "host"
    # 交互模式，方便调试
    stdin_open: true
    tty: true
```

### 3. requirements.txt 示例
```txt
# requirements.txt
instaloader>=4.9
requests>=2.28.0
urllib3>=1.26.0
```

### 4. .dockerignore
```
# .dockerignore
__pycache__
*.pyc
*.pyo
.git
.gitignore
README.md
.env
.venv
.pytest_cache
.DS_Store
Thumbs.db

# 不要把大文件复制到镜像里
data/downloads/
data/merged/
videos/downloads/
videos/merged/
logs/
temp/
```

### 5. 简化的 Makefile
```makefile
# Makefile
.PHONY: build up down shell logs clean

# 构建镜像
build:
	docker-compose build

# 启动容器 (后台运行)
up:
	docker-compose up -d

# 停止容器
down:
	docker-compose down

# 进入容器shell
shell:
	docker-compose exec social-media-hub bash

# 查看日志
logs:
	docker-compose logs -f

# 清理
clean:
	docker-compose down
	docker system prune -f

# 运行你的命令
download-ai:
	docker-compose exec social-media-hub python main.py --download --ai_vanvan

download-all:
	docker-compose exec social-media-hub python main.py --download --all

merge:
	docker-compose exec social-media-hub python main.py --merge

auto:
	docker-compose exec social-media-hub python main.py --auto --all

status:
	docker-compose exec social-media-hub python main.py --status

# 交互模式 (方便调试)
run:
	docker-compose run --rm social-media-hub bash
```

## 🚀 使用步骤

### 1. 准备文件
```bash
# 在你的项目根目录创建这些文件
# 已经存在的不用动：main.py, config/, logs/ 等

# 创建requirements.txt (如果没有)
pip freeze > requirements.txt

# 创建Dockerfile
# 创建docker-compose.yml
# 创建.dockerignore
```

### 2. 构建和运行
```bash
# 构建Docker镜像
make build

# 启动容器
make up

# 查看是否启动成功
docker ps
```

### 3. 运行你的程序
```bash
# 进入容器
make shell

# 在容器内运行你的命令
python main.py --download --ai_vanvan
python main.py --merge
python main.py --auto --all

# 或者直接从外部执行
make download-ai
make merge  
make auto
```

### 4. 数据持久化
所有重要数据都会保存在宿主机上：
- `./data/` -> 下载的数据
- `./logs/` -> 日志文件
- `./config/` -> 配置文件
- `./temp/` -> 临时文件

## 🎯 这个版本的优势

### ✅ 适合你当前项目：
1. **不添加额外依赖** - 只Docker化现有代码
2. **数据不丢失** - 所有文件都映射到宿主机
3. **使用简单** - 和之前一样的命令
4. **环境隔离** - 不污染宿主机Python环境

### 🔄 渐进式改进：
- **现在**: 基础Docker化
- **以后**: 需要时再加Redis/PostgreSQL
- **最后**: 微服务化

## 💡 试试看！

1. 创建这几个文件
2. 运行 `make build`
3. 运行 `make up`
4. 运行 `make shell` 进入容器
5. 在容器里执行你熟悉的命令

这样你就能体验Docker的好处，但不会改变你现有的工作流程！
