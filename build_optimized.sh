#!/bin/bash
# 构建优化脚本 - 减少重复下载

echo "🏗️ 社交媒体自动化系统 - 优化构建"

# 检查是否存在基础镜像
if docker images | grep -q "social-media-base"; then
    echo "✅ 基础镜像已存在，跳过构建"
else
    echo "🔨 构建基础镜像（包含所有依赖）..."
    docker build -f Dockerfile.base -t social-media-base:latest .
    if [ $? -eq 0 ]; then
        echo "✅ 基础镜像构建完成"
    else
        echo "❌ 基础镜像构建失败"
        exit 1
    fi
fi

# 构建各个微服务
echo "🔨 构建微服务..."

services=("api-gateway" "auth" "downloader" "standardizer" "merger" "uploader")

for service in "${services[@]}"; do
    echo "🔧 构建 $service..."
    docker-compose build $service
    if [ $? -eq 0 ]; then
        echo "✅ $service 构建完成"
    else
        echo "❌ $service 构建失败"
    fi
done

echo "🚀 启动所有服务..."
docker-compose up -d

echo "📊 服务状态："
docker-compose ps