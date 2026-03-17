param(
    [Parameter(Mandatory=$true)]
    [string]$Account,
    
    [int]$MaxPosts = 10
)

Write-Host "🚀 启动下载任务: $Account (最多 $MaxPosts 个)" -ForegroundColor Green

# 启动下载任务
$response = Invoke-RestMethod -Uri "http://localhost:8080/download" -Method POST -ContentType "application/json" -Body (@{
    account = $Account
    max_posts = $MaxPosts
} | ConvertTo-Json)

Write-Host "✅ 任务已启动: $($response.message)" -ForegroundColor Green
Write-Host "📊 参数: 账号=$($response.account), 最大=$($response.max_posts)" -ForegroundColor Cyan
Write-Host "" 

# 等待1秒让任务开始
Start-Sleep -Seconds 1

Write-Host "📋 实时日志输出:" -ForegroundColor Yellow
$separator = "=" * 50
Write-Host $separator -ForegroundColor Yellow

# 实时跟踪Docker日志
docker-compose logs --follow --tail 0 downloader