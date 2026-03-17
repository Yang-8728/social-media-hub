@echo off
echo 启动下载任务: %1 (最多 %2 个)

curl -X POST -H "Content-Type: application/json" -d "{\"account\": \"%1\", \"max_posts\": %2}" http://localhost:8080/download

echo.
echo 任务已启动，开始实时日志...
echo ==================================================

docker-compose logs --follow --tail 0 downloader