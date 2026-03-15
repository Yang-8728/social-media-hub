# 启用 Docker Desktop Kubernetes - 详细步骤

## 当前状态
- ✅ kubectl 已安装 (v1.32.2)
- ❌ Kubernetes 集群未运行

## 启用步骤

### 1. 打开 Docker Desktop 设置

**方法 A**: 
- 右键点击 Windows 任务栏右下角的 Docker 图标 🐳
- 选择 `Settings...`

**方法 B**:
- 打开 Docker Desktop 应用
- 点击右上角 ⚙️ 齿轮图标

### 2. 启用 Kubernetes

1. 在左侧菜单中找到 `Kubernetes`
2. 勾选以下选项：
   - ✅ `Enable Kubernetes`
   - ✅ `Show system containers (advanced)` (可选，用于调试)
3. 点击右下角 `Apply & Restart` 按钮

### 3. 等待初始化（重要！）

**初次启用需要下载镜像，可能需要 5-10 分钟**

进度指示：
```
Installing Kubernetes...
Starting Kubernetes...
Kubernetes is starting...
```

完成标志：
- Docker Desktop 左下角显示：
  ```
  🐳 Docker Desktop is running
  ☸️  Kubernetes is running
  ```
- 两个图标都是 **绿色** ✅

### 4. 验证安装

启用成功后，在 PowerShell 执行：

```powershell
# 检查集群连接
kubectl cluster-info

# 预期输出：
# Kubernetes control plane is running at https://kubernetes.docker.internal:6443
# CoreDNS is running at https://kubernetes.docker.internal:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

# 检查节点
kubectl get nodes

# 预期输出：
# NAME             STATUS   ROLES           AGE   VERSION
# docker-desktop   Ready    control-plane   1m    v1.29.x

# 查看所有命名空间
kubectl get namespaces

# 预期输出：
# NAME              STATUS   AGE
# default           Active   1m
# kube-node-lease   Active   1m
# kube-public       Active   1m
# kube-system       Active   1m
```

如果输出正常，说明 Kubernetes 已成功启动！

---

## 常见问题

### Q1: 启用按钮灰色无法点击
**原因**: WSL 2 未启用或 Docker Engine 未运行

**解决**:
```powershell
# 检查 Docker Engine
docker ps

# 如果失败，重启 Docker Desktop
# 右键托盘图标 → Restart
```

### Q2: 一直卡在 "Starting Kubernetes..."
**原因**: 网络问题，无法下载 Kubernetes 镜像

**解决方案 1**: 等待更长时间（第一次可能需要 10-15 分钟）

**解决方案 2**: 配置镜像加速
1. Docker Desktop → Settings → Docker Engine
2. 添加镜像源：
```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://mirror.ccs.tencentyun.com"
  ]
}
```
3. Apply & Restart
4. 重新启用 Kubernetes

**解决方案 3**: 重置 Kubernetes
1. Docker Desktop → Settings → Kubernetes
2. 点击 `Reset Kubernetes Cluster...`
3. 确认重置
4. 重新启用

### Q3: 出现 "error: couldn't get current server API group list"
**原因**: Kubernetes 集群未启动或 kubeconfig 配置错误

**解决**:
```powershell
# 检查 kubeconfig
kubectl config view

# 切换到 docker-desktop context
kubectl config use-context docker-desktop

# 重新验证
kubectl cluster-info
```

---

## 资源配置建议

### Docker Desktop 资源设置

Settings → Resources → Advanced:

- **CPUs**: 4 核（最少 2 核）
- **Memory**: 8 GB（最少 4 GB）
- **Swap**: 2 GB
- **Disk image size**: 60 GB

**为什么需要更多资源？**
- Docker Compose: 8 个容器 + Redis
- Kubernetes: 额外需要控制面板（API Server、Scheduler、Controller Manager、etcd）
- 系统容器大约占用 2GB 内存

---

## 下一步

启用成功后，运行以下命令验证：

```powershell
# 1. 检查版本
kubectl version

# 2. 检查集群
kubectl cluster-info

# 3. 检查节点
kubectl get nodes

# 4. 创建测试 Pod
kubectl run test-pod --image=nginx --restart=Never

# 5. 查看 Pod
kubectl get pods

# 6. 删除测试 Pod
kubectl delete pod test-pod
```

全部成功后，告诉我，我会生成完整的 K8s 部署文件！

---

## 如果仍然无法启动

### 完全重置 Docker Desktop

1. 备份重要数据（容器、镜像、卷）
2. Docker Desktop → Troubleshoot → Reset to factory defaults
3. 重启电脑
4. 重新安装 Docker Desktop
5. 启用 WSL 2 backend
6. 启用 Kubernetes

### 替代方案：Minikube

如果 Docker Desktop K8s 无法启动，可以使用 Minikube：

```powershell
# 安装 Minikube
choco install minikube

# 启动集群
minikube start --driver=docker --cpus=4 --memory=8192

# 验证
kubectl get nodes
```

但推荐优先使用 Docker Desktop K8s，因为它和 Docker Compose 集成更好。
