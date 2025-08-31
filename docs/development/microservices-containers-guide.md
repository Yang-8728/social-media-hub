# 🚀 微服务容器化详细方案

## 🏗️ 从单体到微服务的容器变化

### 阶段1：单体应用 (1个容器)
```dockerfile
# Dockerfile (单体版本)
FROM python:3.11-slim

WORKDIR /app

# 安装所有依赖
RUN apt-get update && apt-get install -y ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制整个项目
COPY . .

# 一个容器包含所有功能
CMD ["python", "main.py"]
```

### 阶段2：微服务架构 (5个容器)

#### 1. 📥 下载服务容器
```dockerfile
# services/download/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 只安装下载相关依赖
COPY services/download/requirements.txt .
RUN pip install -r requirements.txt

# 只复制下载服务代码
COPY services/download/ .
COPY src/platforms/instagram/ ./platforms/instagram/
COPY src/accounts/ ./accounts/

EXPOSE 8001
CMD ["python", "app.py"]
```

#### 2. 🎬 视频处理服务容器
```dockerfile
# services/video/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装FFmpeg (只有这个服务需要)
RUN apt-get update && apt-get install -y ffmpeg

# 安装视频处理依赖
COPY services/video/requirements.txt .
RUN pip install -r requirements.txt

# 只复制视频处理代码
COPY services/video/ .
COPY src/utils/video_merger.py ./utils/

EXPOSE 8002
CMD ["python", "app.py"]
```

#### 3. 👤 账户服务容器
```dockerfile
# services/account/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 账户服务依赖
COPY services/account/requirements.txt .
RUN pip install -r requirements.txt

# 只复制账户管理代码
COPY services/account/ .
COPY src/accounts/ ./accounts/

EXPOSE 8003
CMD ["python", "app.py"]
```

#### 4. 📁 文件服务容器
```dockerfile
# services/file/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 文件服务依赖
COPY services/file/requirements.txt .
RUN pip install -r requirements.txt

# 只复制文件管理代码
COPY services/file/ .
COPY src/utils/folder_manager.py ./utils/

EXPOSE 8004
CMD ["python", "app.py"]
```

#### 5. ⏰ 调度服务容器
```dockerfile
# services/scheduler/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 调度服务依赖
COPY services/scheduler/requirements.txt .
RUN pip install -r requirements.txt

# 只复制调度代码
COPY services/scheduler/ .

EXPOSE 8005
CMD ["python", "app.py"]
```

## 🐳 Docker Compose 配置

### 单体版本 (1个容器)
```yaml
# docker-compose-monolith.yml
version: '3.8'

services:
  social-media-hub:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
      - ./config:/app/config
      - ./logs:/app/logs
```

### 微服务版本 (5个容器)
```yaml
# docker-compose-microservices.yml
version: '3.8'

services:
  download-service:
    build: ./services/download
    ports:
      - "8001:8001"
    environment:
      - VIDEO_SERVICE_URL=http://video-service:8002
      - ACCOUNT_SERVICE_URL=http://account-service:8003
      - FILE_SERVICE_URL=http://file-service:8004
    volumes:
      - ./data/downloads:/app/data
    depends_on:
      - account-service

  video-service:
    build: ./services/video
    ports:
      - "8002:8002"
    environment:
      - FILE_SERVICE_URL=http://file-service:8004
    volumes:
      - ./data:/app/data
      
  account-service:
    build: ./services/account
    ports:
      - "8003:8003"
    volumes:
      - ./config:/app/config
      - ./temp:/app/temp

  file-service:
    build: ./services/file
    ports:
      - "8004:8004"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs

  scheduler-service:
    build: ./services/scheduler
    ports:
      - "8005:8005"
    environment:
      - DOWNLOAD_SERVICE_URL=http://download-service:8001
      - VIDEO_SERVICE_URL=http://video-service:8002
    depends_on:
      - download-service
      - video-service
      - account-service
      - file-service
```

## 🌐 Kubernetes 部署配置

### 单体版本 (1个Pod)
```yaml
# k8s-monolith.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: social-media-hub
spec:
  replicas: 1
  selector:
    matchLabels:
      app: social-media-hub
  template:
    metadata:
      labels:
        app: social-media-hub
    spec:
      containers:
      - name: app
        image: social-media-hub:latest
        ports:
        - containerPort: 8080
```

### 微服务版本 (5个Deployment)
```yaml
# k8s-microservices.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: download-service
spec:
  replicas: 2  # 可以独立扩缩容
  selector:
    matchLabels:
      app: download-service
  template:
    metadata:
      labels:
        app: download-service
    spec:
      containers:
      - name: download-service
        image: download-service:latest
        ports:
        - containerPort: 8001

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: video-service
spec:
  replicas: 1  # 视频处理需要更多资源
  selector:
    matchLabels:
      app: video-service
  template:
    metadata:
      labels:
        app: video-service
    spec:
      containers:
      - name: video-service
        image: video-service:latest
        ports:
        - containerPort: 8002
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: account-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: account-service
  template:
    metadata:
      labels:
        app: account-service
    spec:
      containers:
      - name: account-service
        image: account-service:latest
        ports:
        - containerPort: 8003

# ... 其他服务类似
```

## 📊 容器对比分析

### 单体架构：
| 特性 | 单体容器 |
|------|---------|
| 容器数量 | 1个 |
| 镜像大小 | 大 (包含所有依赖) |
| 启动时间 | 中等 |
| 资源使用 | 集中但可能浪费 |
| 扩展性 | 整体扩展 |
| 故障影响 | 全部功能失效 |
| 部署复杂度 | 简单 |

### 微服务架构：
| 特性 | 微服务容器 |
|------|----------|
| 容器数量 | 5个 |
| 镜像大小 | 小 (各自依赖) |
| 启动时间 | 快 (单个服务小) |
| 资源使用 | 精确分配 |
| 扩展性 | 独立扩展 |
| 故障影响 | 部分功能失效 |
| 部署复杂度 | 复杂但灵活 |

## 🎯 实际项目结构变化

### Before (单体)：
```
social-media-hub/
├── Dockerfile                 # 1个
├── docker-compose.yml         # 1个服务
├── main.py                    # 入口
├── src/                       # 所有代码在一起
│   ├── platforms/
│   ├── utils/
│   └── accounts/
└── requirements.txt           # 所有依赖
```

### After (微服务)：
```
social-media-hub/
├── docker-compose.yml         # 5个服务
├── services/
│   ├── download/
│   │   ├── Dockerfile         # 下载服务容器
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── video/
│   │   ├── Dockerfile         # 视频服务容器
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── account/
│   │   ├── Dockerfile         # 账户服务容器
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── file/
│   │   ├── Dockerfile         # 文件服务容器
│   │   ├── app.py
│   │   └── requirements.txt
│   └── scheduler/
│       ├── Dockerfile         # 调度服务容器
│       ├── app.py
│       └── requirements.txt
└── k8s/
    ├── namespace.yaml
    ├── download-service.yaml
    ├── video-service.yaml
    ├── account-service.yaml
    ├── file-service.yaml
    └── scheduler-service.yaml
```

## 💡 关键优势

### 容器隔离：
- ✅ **技术栈隔离**: 视频服务可以用不同的Python版本
- ✅ **依赖隔离**: 每个服务只安装需要的包
- ✅ **资源隔离**: 可以为视频处理分配更多CPU
- ✅ **故障隔离**: 一个服务挂掉不影响其他服务

### 独立部署：
- ✅ **独立更新**: 修改下载逻辑只需重建下载服务
- ✅ **独立扩缩容**: 下载量大时只扩展下载服务
- ✅ **独立监控**: 每个服务独立的健康检查
- ✅ **独立回滚**: 问题服务可以独立回滚

## 🚀 学习路径建议

### Week 1-2: 单体容器化
```bash
目标：掌握基础Docker技能
成果：整个项目在1个容器中运行
学习：Dockerfile、docker build、docker run
```

### Week 3-4: 微服务拆分  
```bash
目标：代码重构为微服务架构
成果：5个独立的服务代码
学习：API设计、服务间通信
```

### Week 5: 微服务容器化
```bash
目标：为每个微服务创建容器
成果：5个独立的Docker镜像
学习：docker-compose、服务编排
```

### Week 6: K8s部署
```bash
目标：在K8s中部署微服务
成果：完整的微服务系统在K8s运行
学习：Service发现、负载均衡
```

总结：微服务化后需要**多个容器**，每个服务一个容器，这样才能实现真正的服务隔离和独立部署！🎯
