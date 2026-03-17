$body = @{
    account = "ai_vanvan"
    video_path = "videos/merged/ai_vanvan/test.mp4"
    title = "test123"
    description = "test video"
} | ConvertTo-Json

Write-Host "Sending upload request (English only):"
Write-Host $body

$response = Invoke-RestMethod -Uri "http://localhost:8080/api/uploader/upload" `
    -Method POST `
    -ContentType "application/json; charset=utf-8" `
    -Body ([System.Text.Encoding]::UTF8.GetBytes($body))

Write-Host "`nResponse:"
$response | ConvertTo-Json
