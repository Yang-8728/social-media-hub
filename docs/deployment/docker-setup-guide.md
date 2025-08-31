# 🐳 Social Media Hub Docker化指南

## 第一阶段：容器化现有单体应用

### 1. 主应用 Dockerfile
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装FFmpeg (如果需要)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p data/downloads data/merged logs temp config

# 设置权限
RUN chmod +x main.py

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# 暴露端口（如果将来添加web界面）
EXPOSE 8000

# 启动命令
CMD ["python", "main.py", "--help"]
```

### 2. Docker Compose 配置
```yaml
# docker-compose.yml
version: '3.8'

services:
  social-media-hub:
    build: .
    container_name: social-media-hub
    volumes:
      # 挂载数据目录到宿主机，避免数据丢失
      - ./data:/app/data
      - ./logs:/app/logs
      - ./config:/app/config
      - ./temp:/app/temp
      # 如果有Firefox session文件
      - ./temp:/app/temp
    environment:
      # 环境变量配置
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=INFO
    # 如果需要网络访问Instagram
    network_mode: "host"
    # 或者使用自定义网络
    # networks:
    #   - social-media-network
    
  # Redis (用于将来的任务队列)
  redis:
    image: redis:7-alpine
    container_name: social-media-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  # PostgreSQL (用于将来的数据存储)
  postgres:
    image: postgres:15
    container_name: social-media-postgres
    environment:
      POSTGRES_DB: social_media_hub
      POSTGRES_USER: smhub
      POSTGRES_PASSWORD: your_password_here
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  # 文件浏览器 (可选，方便查看下载的文件)
  filebrowser:
    image: filebrowser/filebrowser:latest
    container_name: social-media-filebrowser
    ports:
      - "8080:80"
    volumes:
      - ./data:/srv
    environment:
      - FB_BASEURL=/files

volumes:
  redis_data:
  postgres_data:

# networks:
#   social-media-network:
#     driver: bridge
```

### 3. 开发环境配置
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  social-media-hub:
    build: 
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      # 开发时挂载源代码，支持热重载
      - .:/app
      - /app/__pycache__
    environment:
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    command: python main.py --help

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

# 其他服务同docker-compose.yml
```

### 4. 开发用 Dockerfile
```dockerfile
# Dockerfile.dev
FROM python:3.11-slim

WORKDIR /app

# 安装开发工具
RUN apt-get update && apt-get install -y \
    firefox-esr \
    ffmpeg \
    git \
    vim \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装Python开发依赖
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# 开发模式不复制代码，通过volume挂载
COPY . .

CMD ["bash"]
```

### 5. 环境变量文件
```bash
# .env
# 数据库配置
POSTGRES_DB=social_media_hub
POSTGRES_USER=smhub
POSTGRES_PASSWORD=your_password_here

# Redis配置
REDIS_URL=redis://redis:6379

# 应用配置
DEBUG=false
LOG_LEVEL=INFO

# Instagram配置
MAX_POSTS_PER_SESSION=50
REQUEST_DELAY=2
MAX_RETRIES=3
```

### 6. .dockerignore 文件
```
# .dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.git
.gitignore
README.md
.env
.venv
.pytest_cache
.coverage
.DS_Store
Thumbs.db

# 避免复制大文件到镜像
data/downloads/
data/merged/
logs/
temp/
```

### 7. Makefile 自动化命令
```makefile
# Makefile
.PHONY: build up down logs shell clean test

# 构建镜像
build:
	docker-compose build

# 启动服务
up:
	docker-compose up -d

# 停止服务
down:
	docker-compose down

# 查看日志
logs:
	docker-compose logs -f social-media-hub

# 进入容器
shell:
	docker-compose exec social-media-hub bash

# 清理
clean:
	docker-compose down -v
	docker system prune -f

# 运行测试
test:
	docker-compose exec social-media-hub python -m pytest

# 开发模式
dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# 生产模式构建
prod-build:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# 下载命令
download:
	docker-compose exec social-media-hub python main.py --download --ai_vanvan

# 合并命令
merge:
	docker-compose exec social-media-hub python main.py --merge

# 自动模式
auto:
	docker-compose exec social-media-hub python main.py --auto --all
```

## 🎯 使用步骤

### 1. 准备文件
```bash
# 创建必要的配置文件
echo "POSTGRES_PASSWORD=your_password_here" > .env

# 创建requirements.txt（如果还没有）
pip freeze > requirements.txt
```

### 2. 构建和启动
```bash
# 构建镜像
make build

# 启动所有服务
make up

# 查看运行状态
docker-compose ps
```

### 3. 运行你的应用
```bash
# 进入容器执行命令
make download  # 下载
make merge     # 合并
make auto      # 自动模式

# 或者进入shell操作
make shell
```

### 4. 监控和调试
```bash
# 查看日志
make logs

# 查看特定服务日志
docker-compose logs -f redis
docker-compose logs -f postgres
```

## 🔧 优势

### 容器化的好处：
1. **环境一致性** - 开发、测试、生产环境完全一致
2. **依赖隔离** - 不会污染宿主机环境
3. **快速部署** - 一键启动整个技术栈
4. **版本管理** - 通过镜像标签管理不同版本
5. **扩展准备** - 为后续微服务化打基础

### 下一步计划：
- ✅ 第1周：完成Docker化
- 🔄 第2-3周：学习服务拆分
- 🔄 第4周：微服务改造
- 🔄 第5周：Kubernetes部署

这样循序渐进，既能学到技术，又不会一下子把项目搞复杂！
