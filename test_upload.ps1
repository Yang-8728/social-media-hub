$body = @{
    account = "ai_vanvan"
    video_path = "videos/merged/ai_vanvan/ins海外离大谱#123.mp4"
    title = "ins海外离大谱#123"
    description = "Instagram搞笑视频合集 #123"
} | ConvertTo-Json

Write-Host "Sending upload request:"
Write-Host $body

$response = Invoke-RestMethod -Uri "http://localhost:8080/api/uploader/upload" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

Write-Host "`nResponse:"
$response | ConvertTo-Json
