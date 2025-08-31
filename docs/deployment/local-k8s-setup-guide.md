# 🏠 本地K8s集群搭建完全指南

## 🎯 本地K8s方案对比

### 1. 💻 **Minikube** (最推荐入门)
```bash
优点：
✅ 官方支持，最稳定
✅ 完整的K8s功能
✅ 支持多种驱动 (Docker/VirtualBox/Hyper-V)
✅ 插件生态丰富
✅ Windows原生支持

缺点：
❌ 单节点集群
❌ 资源消耗较大

适合：K8s入门学习，功能完整性测试
资源要求：4GB RAM，20GB存储
```

### 2. 🐳 **Kind** (Kubernetes in Docker)
```bash
优点：
✅ 轻量级，启动快
✅ 支持多节点集群
✅ CI/CD友好
✅ 配置灵活

缺点：
❌ 功能相对简单
❌ 网络配置复杂

适合：开发测试，CI/CD集成
资源要求：2GB RAM，10GB存储
```

### 3. 🚀 **k3s** (轻量级K8s)
```bash
优点：
✅ 极轻量 (<100MB)
✅ 生产级别
✅ 边缘计算友好
✅ 快速部署

缺点：
❌ Windows支持有限
❌ 功能裁剪

适合：资源受限环境，边缘计算
资源要求：1GB RAM，5GB存储
```

### 4. 🏢 **Docker Desktop K8s**
```bash
优点：
✅ 一键启用
✅ 与Docker集成好
✅ GUI管理

缺点：
❌ 功能有限
❌ 版本更新慢
❌ 需要Docker Desktop许可

适合：Docker用户，快速体验
资源要求：4GB RAM，15GB存储
```

## 🎯 推荐学习路径

### 阶段1：Minikube入门 (推荐)
```bash
为什么选择Minikube：
✅ 最接近真实K8s环境
✅ 学习曲线平缓
✅ 社区支持最好
✅ 文档最完善
✅ 功能最完整

学习周期：2-3周
```

### 阶段2：Kind进阶 (可选)
```bash
目标：多节点集群体验
学习重点：
- 集群网络
- 节点调度
- 高可用配置

学习周期：1-2周
```

## 🚀 Minikube完整安装指南

### 1. 环境准备
```powershell
# 检查系统要求
systeminfo | findstr /C:"Total Physical Memory"
# 确保至少4GB RAM

# 检查虚拟化支持
systeminfo | findstr /C:"Hyper-V"
```

### 2. 安装Docker Desktop
```powershell
# 下载并安装Docker Desktop
# https://www.docker.com/products/docker-desktop

# 启用Kubernetes (可选，我们用Minikube)
# 设置 -> Kubernetes -> Enable Kubernetes
```

### 3. 安装Minikube
```powershell
# 方法1：使用Chocolatey (推荐)
choco install minikube

# 方法2：直接下载
# https://github.com/kubernetes/minikube/releases
# 下载 minikube-windows-amd64.exe
# 重命名为 minikube.exe
# 放到 PATH 环境变量中
```

### 4. 安装kubectl
```powershell
# 方法1：使用Chocolatey
choco install kubernetes-cli

# 方法2：直接下载
# https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
```

### 5. 启动Minikube
```powershell
# 使用Docker驱动启动 (推荐)
minikube start --driver=docker --memory=4096 --cpus=2

# 如果有问题，使用Hyper-V驱动
minikube start --driver=hyperv --memory=4096 --cpus=2

# 验证安装
kubectl get nodes
kubectl get pods -A
```

## 🎯 Social Media Hub K8s化实战

### 1. 项目Dockerfile化
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建数据目录
RUN mkdir -p /app/data/downloads /app/data/merged /app/logs

# 暴露端口 (如果有Web界面)
EXPOSE 8080

# 启动命令
CMD ["python", "main.py", "--status"]
```

### 2. Kubernetes配置文件
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: social-media-hub

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: social-media-hub
data:
  accounts.json: |
    {
      "accounts": [
        {"username": "ai_vanvan", "enabled": true},
        {"username": "aigf8728", "enabled": true}
      ]
    }

---
# k8s/pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: video-storage
  namespace: social-media-hub
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi

---
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: social-media-hub
  namespace: social-media-hub
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
        imagePullPolicy: Never  # 使用本地镜像
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: video-storage
          mountPath: /app/data
        - name: config
          mountPath: /app/config
        env:
        - name: APP_ENV
          value: "kubernetes"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
      volumes:
      - name: video-storage
        persistentVolumeClaim:
          claimName: video-storage
      - name: config
        configMap:
          name: app-config

---
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: social-media-hub-service
  namespace: social-media-hub
spec:
  selector:
    app: social-media-hub
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP

---
# k8s/ingress.yaml (可选)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: social-media-hub-ingress
  namespace: social-media-hub
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: social-media-hub.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: social-media-hub-service
            port:
              number: 80
```

### 3. 部署脚本
```powershell
# deploy.ps1
# 构建Docker镜像
docker build -t social-media-hub:latest .

# 加载镜像到Minikube
minikube image load social-media-hub:latest

# 应用K8s配置
kubectl apply -f k8s/

# 检查部署状态
kubectl get all -n social-media-hub

# 查看Pod日志
kubectl logs -n social-media-hub deployment/social-media-hub

# 端口转发访问应用
kubectl port-forward -n social-media-hub service/social-media-hub-service 8080:80
```

## 🎓 学习计划

### Week 1: 环境搭建和基础概念
```bash
Day 1-2: 安装Minikube和kubectl
Day 3-4: 学习Pod, Service, Deployment概念
Day 5-7: 部署第一个应用到K8s
```

### Week 2: 核心对象深入
```bash
Day 1-2: ConfigMap和Secret管理
Day 3-4: PersistentVolume存储
Day 5-7: Ingress网络配置
```

### Week 3: Social Media Hub K8s化
```bash
Day 1-2: 创建Dockerfile
Day 3-4: 编写K8s YAML文件
Day 5-7: 完整部署和测试
```

### Week 4: 高级功能
```bash
Day 1-2: HPA自动扩缩容
Day 3-4: 健康检查和监控
Day 5-7: CI/CD集成
```

## 📊 资源和成本

### 硬件要求：
```bash
最低配置：
- CPU: 2核心
- RAM: 4GB
- 存储: 20GB

推荐配置：
- CPU: 4核心  
- RAM: 8GB
- 存储: 50GB
```

### 软件成本：
```bash
✅ 完全免费！
- Minikube: 免费开源
- Docker: 个人使用免费
- kubectl: 免费开源
- 所有K8s资源: 免费
```

### 学习成本：
```bash
时间投入：每天1-2小时
总周期：4周
技能收益：
- 掌握K8s核心概念
- 具备容器化部署能力
- 理解云原生架构
- 为简历添加K8s经验
```

## 🎯 进阶路径

### 本地K8s掌握后：
```bash
1. 多节点集群 (Kind)
   - 学习集群网络
   - 理解节点调度
   - 练习高可用部署

2. 云端K8s (TKE/EKS)
   - 体验托管服务
   - 学习生产级配置
   - 掌握云原生集成

3. 生产化实践
   - 监控告警 (Prometheus/Grafana)
   - 日志收集 (ELK Stack)
   - 服务网格 (Istio)
   - GitOps (ArgoCD)
```

## 🎉 总结

### 本地K8s的优势：
- ✅ **零成本**: 完全免费，随时练习
- ✅ **完全控制**: 可以随意实验，不怕搞坏
- ✅ **学习深度**: 深入理解K8s内部机制
- ✅ **快速迭代**: 本地测试，快速验证想法

### 最佳实践建议：
1. **先用Minikube学基础** (2-3周)
2. **然后用Kind学多节点** (1周)  
3. **最后上云学生产化** (2-3周)

这样的学习路径既节省成本，又能获得完整的K8s技能！🚀

想要开始吗？我可以帮你一步步安装配置！
