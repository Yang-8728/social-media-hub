# 云原生工作流示例 (PowerShell)

# 1. 查询当前编号
Write-Host "=== 1. 查询当前编号 ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "http://localhost:8080/api/biliup/counter"

# 2. 设置起始编号为 124
Write-Host "`n=== 2. 设置起始编号为 124 ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "http://localhost:8080/api/biliup/counter" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"value": 124}'

# 3. 模拟上传3个测试视频（会自动使用 #125, #126, #127）
Write-Host "`n=== 3. 上传测试视频 ===" -ForegroundColor Cyan

# 注意：这里只是发送上传任务到队列，实际视频文件需要存在
$testVideos = @(
    "/videos/ai_vanvan/test1.mp4",
    "/videos/ai_vanvan/test2.mp4",
    "/videos/ai_vanvan/test3.mp4"
)

foreach ($video in $testVideos) {
    Write-Host "`n上传: $video" -ForegroundColor Yellow
    Invoke-RestMethod -Uri "http://localhost:8080/api/biliup/upload" `
      -Method POST `
      -ContentType "application/json" `
      -Body (@{
          video_path = $video
          auto_number = $true
      } | ConvertTo-Json)
}

# 4. 查询当前编号（应该是 127）
Write-Host "`n=== 4. 上传后查询编号 ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "http://localhost:8080/api/biliup/counter"

# 5. 测试完成，删除B站视频后，回退计数器
Write-Host "`n=== 5. 回退计数器到 124 ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "http://localhost:8080/api/biliup/counter" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"value": 124}'

# 6. 验证
Write-Host "`n=== 6. 验证计数器已回退 ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "http://localhost:8080/api/biliup/counter"

Write-Host "`n✅ 完成！所有操作通过 HTTP API，无需 Python 脚本" -ForegroundColor Green
