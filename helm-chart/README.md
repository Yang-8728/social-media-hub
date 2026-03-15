# Social Media Hub Helm Chart

Instagram 到 B站的视频自动化管理系统 Helm Chart。

## 快速开始

### 本地测试（Docker Desktop K8s）

```bash
# 安装
helm install social-media-hub ./helm-chart

# 查看状态
kubectl get pods -n social-media-hub

# 卸载
helm uninstall social-media-hub
```

### 部署到华为云 CCE

1. **修改 values.yaml**：
```yaml
global:
  imageRegistry: "swr.cn-north-4.myhuaweicloud.com/your-org/"
  
redis:
  persistence:
    storageClass: "csi-disk"
    hostPath: ""  # 清空 hostPath
    
apiGateway:
  service:
    type: LoadBalancer  # 改成 LoadBalancer
```

2. **推送镜像到 SWR**：
```bash
# 登录 SWR
docker login -u cn-north-4@<AK> -p <SK> swr.cn-north-4.myhuaweicloud.com

# 给镜像打标签
docker tag social-media-hub-api-gateway:latest swr.cn-north-4.myhuaweicloud.com/your-org/api-gateway:latest
docker tag social-media-hub-redis:latest swr.cn-north-4.myhuaweicloud.com/your-org/redis:7-alpine
# ... 其他服务

# 推送
docker push swr.cn-north-4.myhuaweicloud.com/your-org/api-gateway:latest
# ... 其他服务
```

3. **部署到 CCE**：
```bash
# 连接到 CCE 集群
kubectl config use-context cce-cluster

# 部署
helm install social-media-hub ./helm-chart
```

## 配置说明

### 镜像配置
- `global.imageRegistry`: 镜像仓库地址
- `global.imagePullPolicy`: 镜像拉取策略

### 服务配置
每个服务都支持：
- `enabled`: 是否启用
- `image.repository`: 镜像名称
- `image.tag`: 镜像标签
- `replicas`: 副本数

### 存储配置
- 本地环境使用 `hostPath`
- CCE 环境使用 `storageClass: csi-disk`

## 目录结构

```
helm-chart/
├── Chart.yaml              # Chart 元数据
├── values.yaml             # 默认配置
└── templates/              # K8s 资源模板
    ├── namespace.yaml
    ├── redis.yaml
    ├── api-gateway.yaml
    ├── scanner.yaml
    ├── downloader.yaml
    ├── standardizer.yaml
    ├── merger.yaml
    ├── uploader.yaml
    ├── auth.yaml
    └── biliup-uploader.yaml
```

## 升级

```bash
# 修改 values.yaml 后升级
helm upgrade social-media-hub ./helm-chart

# 回滚到上一个版本
helm rollback social-media-hub
```

## 故障排查

```bash
# 查看所有资源
helm list
kubectl get all -n social-media-hub

# 查看 Pod 日志
kubectl logs -n social-media-hub deployment/scanner

# 查看 Helm release 信息
helm status social-media-hub
```
