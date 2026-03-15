# 本地 Kubernetes 环境搭建指南

## 1. 启用 Docker Desktop Kubernetes

### Windows 步骤：

1. **打开 Docker Desktop**
   - 右键托盘图标 → Settings

2. **启用 Kubernetes**
   - 左侧菜单选择 `Kubernetes`
   - ✅ 勾选 `Enable Kubernetes`
   - ✅ 勾选 `Show system containers (advanced)`
   - 点击 `Apply & Restart`

3. **等待安装完成**（3-5分钟）
   - 左下角显示 `Kubernetes running` 绿色图标

4. **验证安装**
   ```powershell
   kubectl version --client
   kubectl cluster-info
   kubectl get nodes
   ```

   预期输出：
   ```
   NAME             STATUS   ROLES           AGE   VERSION
   docker-desktop   Ready    control-plane   1m    v1.29.x
   ```

---

## 2. 安装 kubectl（如果未自动安装）

Docker Desktop 通常自带 kubectl，如果没有：

```powershell
# 使用 Chocolatey 安装
choco install kubernetes-cli

# 或使用 Scoop
scoop install kubectl

# 验证
kubectl version --client
```

---

## 3. 本地 vs CCE 对比

| 特性 | 本地 Docker Desktop K8s | 华为云 CCE |
|------|------------------------|-----------|
| 节点数 | 1 (docker-desktop) | 多节点集群 |
| LoadBalancer | ❌ 不支持（用 NodePort 替代） | ✅ 自动分配 ELB |
| PersistentVolume | ✅ hostPath/local | ✅ 华为云盘 EVS |
| 网络 | localhost | 公网 IP |
| 资源限制 | 本地电脑资源 | 云端资源池 |

### 差异调整

**LoadBalancer 替代方案**：
```yaml
# CCE 生产环境
type: LoadBalancer

# 本地开发环境
type: NodePort  # 或直接 port-forward
```

---

## 4. 创建 Kubernetes 部署文件

### 目录结构
```
k8s/
├── namespace.yaml
├── redis/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── pvc.yaml
├── api-gateway/
│   ├── deployment.yaml
│   └── service.yaml
├── biliup-uploader/
│   ├── deployment.yaml
│   └── service.yaml
├── merger/
│   ├── deployment.yaml
│   └── service.yaml
└── ...其他服务
```

---

## 5. 快速部署命令

### 一键部署所有服务
```powershell
# 创建命名空间
kubectl apply -f k8s/namespace.yaml

# 部署 Redis（带持久化）
kubectl apply -f k8s/redis/

# 部署 API Gateway
kubectl apply -f k8s/api-gateway/

# 部署 Biliup Uploader
kubectl apply -f k8s/biliup-uploader/

# 部署其他微服务
kubectl apply -f k8s/merger/
kubectl apply -f k8s/downloader/
kubectl apply -f k8s/standardizer/
# ...
```

### 查看部署状态
```powershell
kubectl get all -n social-media-hub
kubectl get pvc -n social-media-hub
kubectl get pods -n social-media-hub -w  # 持续监控
```

---

## 6. 访问服务

### 方法 1: Port Forward（推荐本地开发）
```powershell
# 映射 API Gateway
kubectl port-forward svc/api-gateway 8080:8000 -n social-media-hub

# 在另一个终端测试
curl http://localhost:8080/api/biliup/counter
```

### 方法 2: NodePort
```powershell
# 查看分配的端口
kubectl get svc api-gateway -n social-media-hub

# 输出示例：
# NAME          TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
# api-gateway   NodePort   10.96.123.45   <none>        8000:30080/TCP   1m

# 访问 http://localhost:30080
```

### 方法 3: Ingress（可选，模拟生产环境）
```powershell
# 安装 Nginx Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.0/deploy/static/provider/cloud/deploy.yaml

# 创建 Ingress 规则
kubectl apply -f k8s/ingress.yaml

# 访问 http://localhost
```

---

## 7. 本地持久化存储

### 创建本地存储目录
```powershell
# 在项目根目录创建
mkdir k8s-data
mkdir k8s-data\redis
mkdir k8s-data\videos
```

### hostPath PVC（本地开发专用）
```yaml
# k8s/redis/pv-local.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis-pv-local
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "C:/Code/social-media-hub/k8s-data/redis"
    type: DirectoryOrCreate
```

---

## 8. 常用命令速查

### 部署管理
```powershell
# 应用配置
kubectl apply -f k8s/

# 删除部署
kubectl delete -f k8s/

# 重启 Pod
kubectl rollout restart deployment/api-gateway -n social-media-hub

# 查看日志
kubectl logs -f deployment/api-gateway -n social-media-hub
kubectl logs -f deployment/biliup-uploader -n social-media-hub
```

### 调试
```powershell
# 进入容器
kubectl exec -it deployment/api-gateway -n social-media-hub -- sh

# 查看资源使用
kubectl top pods -n social-media-hub
kubectl top nodes

# 查看详细信息
kubectl describe pod <pod-name> -n social-media-hub
```

### Redis 检查
```powershell
# 进入 Redis Pod
kubectl exec -it deployment/redis -n social-media-hub -- sh

# 连接 Redis
redis-cli

# 查看计数器
> GET ai_vanvan:video_counter
> LRANGE biliup:queue 0 -1
```

---

## 9. 测试完整流程

```powershell
# 1. 启动 port-forward
kubectl port-forward svc/api-gateway 8080:8000 -n social-media-hub

# 2. 在新终端测试 API（和 Docker Compose 完全一样）
Invoke-RestMethod -Uri "http://localhost:8080/api/biliup/counter"

# 3. 设置计数器
Invoke-RestMethod -Uri "http://localhost:8080/api/biliup/counter" `
  -Method POST -ContentType "application/json" `
  -Body '{"value": 124}'

# 4. 触发上传
Invoke-RestMethod -Uri "http://localhost:8080/api/biliup/upload" `
  -Method POST -ContentType "application/json" `
  -Body '{"video_path": "/videos/ai_vanvan/test.mp4", "auto_number": true}'

# 5. 查看日志
kubectl logs -f deployment/biliup-uploader -n social-media-hub
```

---

## 10. 清理环境

### 删除所有资源
```powershell
# 删除整个命名空间（包含所有资源）
kubectl delete namespace social-media-hub

# 或逐个删除
kubectl delete -f k8s/
```

### 禁用 Kubernetes
- Docker Desktop → Settings → Kubernetes
- ❌ 取消勾选 `Enable Kubernetes`
- Apply & Restart

---

## 11. 性能优化建议

### Docker Desktop 资源配置
- Settings → Resources
- **CPUs**: 4+
- **Memory**: 8GB+
- **Swap**: 2GB
- **Disk image size**: 60GB+

### Kubernetes 专用
```powershell
# 设置默认命名空间（避免每次 -n）
kubectl config set-context --current --namespace=social-media-hub

# 查看当前上下文
kubectl config current-context
```

---

## 12. 下一步

1. ✅ 启用 Docker Desktop Kubernetes
2. 📝 我将为你生成完整的 K8s YAML 文件
3. 🚀 一键部署到本地集群
4. 🧪 测试所有服务（和 Docker Compose 一样的体验）
5. ☁️ 迁移到华为云 CCE（只需改 LoadBalancer 类型）

现在就可以在 Docker Desktop 中启用 Kubernetes，启用后告诉我，我会生成所有 K8s 部署文件！
