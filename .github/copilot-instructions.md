# GitHub Copilot 项目指令

## 项目概述
这是一个社交媒体内容管理系统，用于从 Instagram 下载视频并自动上传到 B站。

## 技术栈
- **后端**: Python 3.11, Flask
- **容器**: Docker Compose (8个微服务)
- **队列**: Redis
- **视频处理**: FFmpeg
- **浏览器自动化**: Selenium (Chrome)

## 服务架构
1. **api-gateway** (端口8080) - API 入口
2. **auth** - 认证服务（Instagram/B站）
3. **scanner** - 扫描新内容
4. **downloader** - 下载视频
5. **standardizer** - 视频标准化（分辨率、编码）
6. **merger** - 合并多个视频
7. **uploader** - 上传到B站
8. **redis** - 任务队列和缓存

## 常用命令
```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker logs social-media-hub-<service>-1 --tail 50

# 重启服务
docker-compose restart <service>

# 重新构建
docker-compose build --no-cache <service>

# 测试 API
curl -X POST http://localhost:8080/api/merger/merge \
  -H "Content-Type: application/json" \
  -d '{"account": "ai_vanvan", "limit": 15}'
```

## 关键约定
- 所有任务必须包含 `type` 字段（如 'merge', 'upload', 'download'）
- 账号名统一使用 `ai_vanvan`
- 视频存储在 `videos/downloads/<account>/<date>/`
- 合并视频输出到 `videos/merged/<account>/`

## 已知问题（需要在新 chat 中注意）
1. Instagram Session 容易过期 - 需要定期重新登录
2. B站 Chrome Profile 需要手动维护 cookies
3. Merger 任务必须包含 `type: 'merge'` 字段
4. Docker 构建时确保使用 `--no-cache` 以应用最新修改

## 代码修改注意事项
- 修改后务必重新构建 Docker 镜像
- API Gateway 的任务格式要与各服务消费端一致
- 视频文件路径使用绝对路径（容器内路径）
- 日志使用统一的 logger 格式

## 测试流程
1. 启动容器: `docker-compose up -d`
2. 检查容器状态: `docker ps`
3. 触发下载: `POST /api/downloader/download`
4. 触发合并: `POST /api/merger/merge`
5. 检查日志确认执行

