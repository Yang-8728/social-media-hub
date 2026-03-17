#!/bin/bash
# AI VanVan 容器化系统启动脚本

echo "🐳 AI VanVan 容器化系统"
echo "======================="

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker"
    exit 1
fi

echo "✅ Docker 运行正常"

# 构建所有容器
echo "🔨 构建容器镜像..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ 容器构建失败"
    exit 1
fi

echo "✅ 容器构建完成"

# 启动所有服务
echo "🚀 启动所有服务..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ 服务启动失败"
    exit 1
fi

echo "✅ 所有服务启动成功"

# 等待服务就绪
echo "⏳ 等待服务就绪..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态:"
docker-compose ps

# 检查API Gateway是否响应
echo "🔍 检查API Gateway..."
if curl -f http://localhost:8080/ > /dev/null 2>&1; then
    echo "✅ API Gateway 运行正常"
else
    echo "⚠️ API Gateway 可能还在启动中..."
fi

echo ""
echo "🎉 系统启动完成！"
echo ""
echo "📋 可用的服务:"
echo "  - API Gateway: http://localhost:8080"
echo "  - Redis: localhost:6379"
echo ""
echo "📖 使用方法:"
echo "  python test_containers.py  # 运行测试"
echo "  docker-compose logs -f     # 查看日志"
echo "  docker-compose down        # 停止服务"
echo ""
echo "🚀 开始测试完整流水线:"
echo "  curl -X POST http://localhost:8080/pipeline -H 'Content-Type: application/json' -d '{\"account\":\"ai_vanvan\",\"max_posts\":5}'"