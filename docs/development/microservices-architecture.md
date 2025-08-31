# 🚀 Social Media Hub 微服务架构设计

## 📁 项目目录结构
```
social-media-hub/
├── services/                           # 微服务目录
│   ├── api-gateway/                    # API网关
│   │   ├── Dockerfile
│   │   ├── nginx.conf
│   │   ├── requirements.txt
│   │   └── app.py
│   │
│   ├── download-service/               # 下载服务
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app.py
│   │   ├── models/
│   │   │   └── download.py
│   │   ├── routes/
│   │   │   └── download_routes.py
│   │   └── utils/
│   │       └── instagram_client.py
│   │
│   ├── video-service/                  # 视频处理服务
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app.py
│   │   ├── models/
│   │   │   └── video.py
│   │   ├── routes/
│   │   │   └── video_routes.py
│   │   └── utils/
│   │       └── ffmpeg_processor.py
│   │
│   ├── account-service/                # 账户服务
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app.py
│   │   ├── models/
│   │   │   └── account.py
│   │   └── routes/
│   │       └── account_routes.py
│   │
│   ├── file-service/                   # 文件服务
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app.py
│   │   └── routes/
│   │       └── file_routes.py
│   │
│   └── scheduler-service/              # 任务调度服务
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── app.py
│       └── tasks/
│           └── scheduler.py
│
├── infrastructure/                     # 基础设施
│   ├── docker-compose.yml             # 本地开发环境
│   ├── docker-compose.prod.yml        # 生产环境
│   ├── kubernetes/                     # K8s部署文件
│   │   ├── namespace.yaml
│   │   ├── secrets.yaml
│   │   ├── configmaps.yaml
│   │   ├── services/
│   │   │   ├── download-service.yaml
│   │   │   ├── video-service.yaml
│   │   │   ├── account-service.yaml
│   │   │   ├── file-service.yaml
│   │   │   └── scheduler-service.yaml
│   │   ├── ingress.yaml
│   │   └── monitoring/
│   │       ├── prometheus.yaml
│   │       └── grafana.yaml
│   │
│   ├── terraform/                      # 云基础设施即代码
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   └── helm/                          # Helm Charts
│       └── social-media-hub/
│           ├── Chart.yaml
│           ├── values.yaml
│           └── templates/
│
├── shared/                            # 共享库
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── events.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── config.py
│   │   └── database.py
│   └── middleware/
│       ├── __init__.py
│       ├── auth.py
│       └── rate_limit.py
│
├── frontend/                          # 前端应用
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.js
│   ├── Dockerfile
│   └── package.json
│
├── scripts/                           # 自动化脚本
│   ├── build.sh                      # 构建脚本
│   ├── deploy.sh                     # 部署脚本
│   ├── test.sh                       # 测试脚本
│   └── cleanup.sh                    # 清理脚本
│
├── monitoring/                        # 监控配置
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   └── dashboards/
│   └── jaeger/
│       └── jaeger.yml
│
├── docs/                             # 文档
│   ├── api/                          # API文档
│   ├── architecture/                 # 架构文档
│   └── deployment/                   # 部署文档
│
├── tests/                            # 测试
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── .github/                          # CI/CD
│   └── workflows/
│       ├── build.yml
│       ├── test.yml
│       └── deploy.yml
│
├── docker-compose.yml                # 开发环境
├── Makefile                          # 自动化命令
└── README.md
```

## 🐳 各服务的Dockerfile示例

### 下载服务 (Download Service)
```dockerfile
# services/download-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

EXPOSE 8001

CMD ["python", "app.py"]
```

### 视频服务 (Video Service)
```dockerfile
# services/video-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

EXPOSE 8002

CMD ["python", "app.py"]
```

## 🔧 Docker Compose配置

### 开发环境 (docker-compose.yml)
```yaml
version: '3.8'

services:
  # API网关
  api-gateway:
    build: ./services/api-gateway
    ports:
      - "8080:80"
    depends_on:
      - download-service
      - video-service
      - account-service
    environment:
      - DOWNLOAD_SERVICE_URL=http://download-service:8001
      - VIDEO_SERVICE_URL=http://video-service:8002
      - ACCOUNT_SERVICE_URL=http://account-service:8003
    networks:
      - social-media-network

  # 下载服务
  download-service:
    build: ./services/download-service
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/downloads
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    volumes:
      - ./data/downloads:/app/downloads
    networks:
      - social-media-network

  # 视频处理服务
  video-service:
    build: ./services/video-service
    ports:
      - "8002:8002"
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    volumes:
      - ./data/downloads:/app/downloads
      - ./data/merged:/app/merged
    networks:
      - social-media-network

  # 账户服务
  account-service:
    build: ./services/account-service
    ports:
      - "8003:8003"
    environment:
      - MONGODB_URL=mongodb://mongo:27017/accounts
    depends_on:
      - mongo
    networks:
      - social-media-network

  # 文件服务
  file-service:
    build: ./services/file-service
    ports:
      - "8004:8004"
    volumes:
      - ./data:/app/data
    networks:
      - social-media-network

  # 任务调度服务
  scheduler-service:
    build: ./services/scheduler-service
    ports:
      - "8005:8005"
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    networks:
      - social-media-network

  # 数据库
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: downloads
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - social-media-network

  mongo:
    image: mongo:6
    volumes:
      - mongo_data:/data/db
    networks:
      - social-media-network

  redis:
    image: redis:7-alpine
    networks:
      - social-media-network

  # 监控
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - social-media-network

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - social-media-network

  # 链路追踪
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
      - "14268:14268"
    networks:
      - social-media-network

volumes:
  postgres_data:
  mongo_data:
  grafana_data:

networks:
  social-media-network:
    driver: bridge
```

## ☸️ Kubernetes部署文件

### 下载服务部署 (kubernetes/services/download-service.yaml)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: download-service
  namespace: social-media-hub
spec:
  replicas: 2
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
        image: social-media-hub/download-service:latest
        ports:
        - containerPort: 8001
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: redis-config
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: download-service
  namespace: social-media-hub
spec:
  selector:
    app: download-service
  ports:
  - port: 8001
    targetPort: 8001
  type: ClusterIP
```

## 🛠️ 开发工作流

### Makefile自动化
```makefile
# Makefile
.PHONY: build test deploy clean

# 构建所有服务
build:
	docker-compose build

# 启动开发环境
dev:
	docker-compose up -d

# 运行测试
test:
	docker-compose -f docker-compose.test.yml up --abort-on-container-exit

# 部署到生产环境
deploy:
	kubectl apply -f infrastructure/kubernetes/

# 清理环境
clean:
	docker-compose down -v
	docker system prune -f

# 查看日志
logs:
	docker-compose logs -f

# 重启服务
restart:
	docker-compose restart

# 数据库迁移
migrate:
	docker-compose exec download-service python manage.py migrate

# 进入服务容器
shell-download:
	docker-compose exec download-service bash

shell-video:
	docker-compose exec video-service bash
```

## 🔄 CI/CD流水线

### GitHub Actions (.github/workflows/build.yml)
```yaml
name: Build and Deploy

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Run tests
      run: |
        make test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to DockerHub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    
    - name: Build and push images
      run: |
        make build
        docker-compose push

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Kubernetes
      run: |
        kubectl config set-cluster k8s --server=${{ secrets.K8S_SERVER }}
        kubectl config set-credentials admin --token=${{ secrets.K8S_TOKEN }}
        kubectl config set-context default --cluster=k8s --user=admin
        kubectl config use-context default
        make deploy
```

## 🎯 学习路径建议

### 第一阶段：基础容器化
1. **Docker基础**：学习Dockerfile编写
2. **Docker Compose**：本地多服务编排
3. **服务拆分**：将现有功能拆分成独立服务

### 第二阶段：微服务通信
1. **REST API**：服务间HTTP通信
2. **消息队列**：异步任务处理(Redis/RabbitMQ)
3. **服务发现**：动态服务注册与发现

### 第三阶段：容器编排
1. **Kubernetes基础**：Pod、Service、Deployment
2. **配置管理**：ConfigMap、Secret
3. **自动扩缩容**：HPA、VPA

### 第四阶段：云原生工具
1. **监控**：Prometheus + Grafana
2. **日志**：ELK Stack
3. **链路追踪**：Jaeger
4. **服务网格**：Istio (可选)

## 🚀 开始实施

要开始这个练手项目，我建议：

1. **先从Docker化现有服务开始**
2. **逐步拆分成微服务**
3. **添加监控和日志**
4. **最后上Kubernetes**

这样你就能体验到完整的云原生技术栈了！想从哪一步开始？
